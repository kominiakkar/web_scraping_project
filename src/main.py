from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import os
from zipfile import ZipFile
from urllib.parse import urljoin, urlparse
from functions import download_files, zip_downloaded, get_file_links

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    selected_extension = request.form.get("extension")
    output_dir = request.form["output_dir"]
    if selected_extension:
        zip_filename = request.form["zip_filename"] + ".zip"
        zip_downloaded(url, output_dir, zip_filename, selected_extension)
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
