from genericpath import exists
from tempfile import TemporaryDirectory
from flask import Flask
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
import os
from zipfile import ZipFile
from genericpath import exists


def get_file_links(url, selected_extension):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    extension_links = []

    if selected_extension:
        if selected_extension.startswith("."):
            selected_extension = selected_extension.lower()
        all_links = [a.get("href") for a in soup.find_all("a")] and [
            img.get("src") for img in soup.find_all("img")
        ]

        for link in all_links:
            if link.endswith(selected_extension):
                extension_links.append(urljoin(url, link))
        print(all_links)
        print(selected_extension)
        print(extension_links)
    return extension_links


def download_files(url, selected_extension):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    temp_dir = "temp_dir"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_links = get_file_links(url, selected_extension)
    for index, file_link in enumerate(file_links, start=1):
        try:
            response = requests.get(file_link)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file {file_link}: {e}")
            continue
        filename = f"file{index}{selected_extension}"
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
    return temp_dir


def clean_temp_dir():
    temp_dir = "temp_dir"
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        os.remove(file_path)
    return None


def zip_downloaded(url, output_dir, zip_filename, selected_extension):
    temp_dir = download_files(url, selected_extension)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    zip_filepath = os.path.join(output_dir, zip_filename)

    try:
        with ZipFile(zip_filepath, "w") as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname=arcname)

        print(f"Zip file created: {zip_filepath}")
        clean_temp_dir()
        return zip_filepath
    except Exception as e:
        print(f"Error creating zip file: {e}")
        clean_temp_dir()
        return None
