import os
import requests
from flask import Flask, send_file

app = Flask(__name__)

ZIP_URL = "https://gic-plateau.s3.ap-northeast-1.amazonaws.com/2023/13999_tokyo_udx-mlit_2023_3dtiles_mtv_1_sample-takeshiba_op.zip"
ZIP_PATH = "sample.zip"

if not os.path.exists(ZIP_PATH):
    print("Downloading ZIP...")
    r = requests.get(ZIP_URL, stream=True)
    with open(ZIP_PATH, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            f.write(chunk)
    print("Download complete")

@app.route("/")
def home():
    return "Server Running"

@app.route("/sample.zip")
def download_zip():
    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
