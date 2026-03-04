import os
import requests
import zipfile

from flask import Flask, send_from_directory

app = Flask(__name__)

ZIP_URL = "https://gic-plateau.s3.ap-northeast-1.amazonaws.com/2023/13999_tokyo_udx-mlit_2023_3dtiles_mtv_1_sample-takeshiba_op.zip"

ZIP_PATH = "sample.zip"
EXTRACT_DIR = "tiles"


# ⭐ ZIPが無ければDL + 解凍
def prepare_data():

    if os.path.exists(EXTRACT_DIR + "/tileset.json"):
        return

    print("Downloading ZIP...")

    r = requests.get(ZIP_URL, stream=True)
    with open(ZIP_PATH, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("Extracting ZIP...")

    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    print("Ready")


@app.route("/")
def home():
    return "3D Tiles Server Running"


@app.route("/tiles/<path:path>")
def serve_tiles(path):
    prepare_data()
    return send_from_directory(EXTRACT_DIR, path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
