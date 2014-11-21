# -*- coding: utf-8 -*-
import urllib
from PIL import Image
import cStringIO

from flask import Flask, request, send_file, make_response

# http://image.space.rakuten.co.jp/lg01/94/0001321294/70/imge4ceefe9zikczj.jpeg

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

def serve_pil_image(pil_img):
    img_io = cStringIO.StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/lgtm", methods=["GET"])
def lgtm():
    y = request.args.get("y", default=0, type=int)
    lgtm = Image.open("img/lgtm.png")
    image_url = request.args.get("url")
    file = cStringIO.StringIO(urllib.urlopen(image_url).read())
    download_image = Image.open(file)

    width, height = download_image.size
    lgtm_width, lgtm_height = lgtm.size
    lgtm = lgtm.resize((width, int(lgtm_height*(float(width)/lgtm_width))))

    r, g, b, alpha = lgtm.split()
    risize_width, resize_height = lgtm.size
    download_image.paste(lgtm, (0, int((height-resize_height)*0.5)-y), mask=alpha)

    return serve_pil_image(download_image)


if __name__ == "__main__":
    app.run(debug=True)