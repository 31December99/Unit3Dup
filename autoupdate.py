import os
import requests
import zipfile
from io import BytesIO


class MyGitReleaseDownloader:
    """
    Download the last repo release
    """

    def __init__(self, repo_url: str, destination_path: str):
        self.repo_url = repo_url
        self.api_url = f"https://api.github.com/repos/{self._extract_repo_owner_and_name()}/releases/latest"
        self.destination_path = destination_path

    def _extract_repo_owner_and_name(self):
        """
        Extract my name
        """
        return "/".join(self.repo_url.rstrip("/").split("/")[-2:])

    def download_latest_release(self):
        """
        Download the lastest release ( zip file) or update if necessary
        """
        response = requests.get(self.api_url)

        if response.status_code != 200:
            print(f"Error : {response.status_code} Please report it")
            return False

        # Get the url of the zip release
        latest_release = response.json()
        zip_url = latest_release['zipball_url']

        # Downloading..
        print(f"Download from {zip_url}...")
        zip_response = requests.get(zip_url)

        if zip_response.status_code == 200:
            # Decompress or update the repo
            self._unzip_and_update(zip_response.content)
        else:
            print(f"Download Error. Please report it {zip_response.status_code}")
            return False

        return True

    def _unzip_and_update(self, zip_content):
        """
        Zip file extraction
        """
        if not os.path.exists(self.destination_path):
            print(f"Create the Folder {self.destination_path}...")
            os.makedirs(self.destination_path)

        # Unzip...
        print(f"Estrazione e aggiornamento nella cartella {self.destination_path}...")

        with zipfile.ZipFile(BytesIO(zip_content)) as zip_file:
            # For each file or folder in zip file
            for file_info in zip_file.infolist():
                extracted_file_path = os.path.join(self.destination_path, file_info.filename)

                # Make folder if it does not exist
                if file_info.is_dir():
                    if not os.path.exists(extracted_file_path):
                        os.makedirs(extracted_file_path)
                else:
                    # Overwite the file only if it is different from the previous version
                    print(f"Aggiornamento del file: {extracted_file_path}")
                    with zip_file.open(file_info) as source, open(extracted_file_path, "wb") as target:
                        target.write(source.read())

        print(f"Finish {self.destination_path}")


if __name__ == "__main__":
    repo_url = "https://github.com/31December99/Unit3Dup"
    destination_path = os.path.join(os.getcwd(), "Unit3Dup")

    downloader = MyGitReleaseDownloader(repo_url, destination_path)
    downloader.download_latest_release()
