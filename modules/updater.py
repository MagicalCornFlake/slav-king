"""Module that ensures the program is updated to the latest version."""

import os
import shutil
import tempfile
import zipfile

import requests

from modules import gui, setup

REPOSITORY_TAGS_URL = "https://api.github.com/repos/kguzek/slav-king/tags"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}


def log(*args, first_step=False, last_step=False, prefix="Done"):
    """Macro for calling the builtin `print` function."""
    if not first_step:
        print(f"{prefix}!")
    print(*args, end=None if last_step else " ... ", flush=True)
    gui.update_label(" ".join(args))
    gui.increment_progressbar()


def get_current_version():
    """Retrieves the currently running project version."""
    with open("data/version.txt", "r", encoding="utf-8") as file:
        version = file.read()
    return version.strip()


def get_version_int(version: str):
    """Strips a version string of delimiters and returns an int."""
    return int(version.lstrip("v").replace(".", ""))


def is_later_version(first: str, second: str):
    """Checks whether `first` is a version string representing a later version than `second`."""
    try:
        return get_version_int(first) > get_version_int(second)
    except ValueError:
        return False


def get_repo_information():
    """Retrieves the latest data from the GitHub repository."""
    response = requests.get(REPOSITORY_TAGS_URL, timeout=10).json()
    return response[0]


def extract_archive(directory: str, archive_content: bytes, repo_version: str):
    """Extracts the given archive in a suitably-named zip file within the provided directory."""
    archive_name = f"slav-king-{repo_version}.zip"
    archive_path = os.path.join(directory, archive_name)
    log("Writing archive to", directory)
    with open(archive_path, "wb") as zip_file:
        zip_file.write(archive_content)
    log("Unzipping compressed objects")
    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(directory)
    log("Copying files to app directory")
    os.remove(archive_path)
    nested_directory_name = os.listdir(directory)[0]
    nested_directory = os.path.join(directory, nested_directory_name)
    shutil.copytree(nested_directory, os.getcwd(), dirs_exist_ok=True)


def download_latest_version(repo_info):
    """Fetches the latest tag zipball to a temporary folder and extracts it."""
    zipball_url = repo_info.get("zipball_url")
    log("Downloading latest version from", zipball_url, first_step=True)
    response = requests.get(zipball_url, headers=HEADERS, timeout=10)
    if response.status_code != 200:
        log(response.json(), last_step=True, prefix="Error")
        gui.show_popup(
            "Network error",
            (
                "Could not download the latest version from GitHub. "
                "Please download and extract it manually."
            ),
            popup_type="error",
        )
        return
    with tempfile.TemporaryDirectory() as directory:
        extract_archive(directory, response.content, repo_info.get("name"))
    log("Update complete.", last_step=True)


def ensure_latest_version():
    """Compares the latest version to the current version. Downloads updates as needed."""
    gui.create_progressbar()
    log("Checking for updates", first_step=True)
    try:
        repo_info = get_repo_information()
    except (
        requests.HTTPError,
        requests.ConnectionError,
        requests.exceptions.ReadTimeout,
    ) as network_error:
        error_message = "Could not connect to the network. Continuing in offline mode."
        log(
            error_message,
            last_step=True,
            prefix=network_error.__class__.__name__,
        )
        gui.show_popup("Network error", error_message, popup_type="warning")
        return
    latest_version = repo_info.get("name")
    current_version = get_current_version()
    if current_version == latest_version or is_later_version(
        current_version, latest_version
    ):
        gui.increment_progressbar(149.9)
        log("All up to date.", last_step=True)
        return
    log(
        "Newer version available:",
        current_version,
        "->",
        latest_version,
        last_step=True,
    )
    download_latest_version(repo_info)
    print("Restarting ...")
    gui.show_popup(
        "Restart required",
        f"Successfully updated to version {latest_version}. Press OK to restart.",
    )
    setup.restart_program()


if __name__ == "__main__":
    ensure_latest_version()
