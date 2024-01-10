"""Module that ensures the program is updated to the latest version."""

import os
import shutil
import sys
import tempfile
import zipfile

import requests

REPOSITORY_TAGS_URL = "https://api.github.com/repos/kguzek/slav-king/tags"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}


def log(*args, first_step=False, last_step=False, prefix="Done"):
    """Macro for calling the builtin `print` function."""
    if not first_step:
        print(f"{prefix}!")
    print(*args, end=None if last_step else " ... ", flush=True)


def get_current_version():
    """Retrieves the currently running project version."""
    with open("data/version.txt", "r", encoding="utf-8") as file:
        version = file.read()
    return version.strip()


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
    log("Downloading latest version", first_step=True)
    zipball_url = repo_info.get("zipball_url")
    log("Fetching from", zipball_url)
    response = requests.get(zipball_url, headers=HEADERS, timeout=10)
    if response.status_code != 200:
        log(response.json(), last_step=True, prefix="Error")
        return
    with tempfile.TemporaryDirectory() as directory:
        extract_archive(directory, response.content, repo_info.get("name"))
    log("Update complete.", last_step=True)


def ensure_latest_version():
    """Compares the latest version to the current version. Downloads updates as needed."""
    log("Checking for updates", first_step=True)
    try:
        repo_info = get_repo_information()
    except (requests.HTTPError, requests.ConnectionError) as network_error:
        log(
            "Could not connect to the network. Continuing in offline mode.",
            last_step=True,
            prefix=network_error.__class__.__name__,
        )
        return
    latest_version = repo_info.get("name")
    if get_current_version() == latest_version:
        log("All up to date.", last_step=True)
        return
    log("Newer version available:", latest_version, last_step=True)
    download_latest_version(repo_info)
    print("Restarting ...")
    os.execl(sys.executable, f'"{sys.executable}"', *sys.argv)


if __name__ == "__main__":
    ensure_latest_version()
