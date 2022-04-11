from PIL import Image
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from process import process_img, process_img_with_ref

app = Flask(__name__)

app.config.from_object('config.Config')
load_dotenv()


@app.route("/im_size", methods=["POST"])
def process_image():
    random = request.form.get('random')
    print(len(request.form))

    src = request.files.get('img', '')
    # Read the image via file.stream
    # img = Image.open(src.stream).convert("RGB")
    # process_img(id,img)
    return jsonify({'msg': 'success'})


@app.route("/makeup", methods=["POST"])
def process_makeup():
    src = request.files.get('img', '')
    random = request.form.get('random')
    styles = request.form.getlist('styles')

    img = Image.open(src.stream).convert("RGB")
    print("Processing")
    links = []
    try:
        if random is not None:
            links = process_img(img)
        elif styles is None:
            links = process_img(img)
        else:
            links = process_img_with_ref(img, styles)
    except:
        print("image error format")
        return jsonify({'msg': 'failed'})
    # if random is not None:
    #     links=process_img(img)
    # elif styles is None:
    #     links=process_img(img)
    # else:
    #     links=process_img_with_ref(img, styles)

    return jsonify({'msg': 'success', 'links': links})


@app.route("/make", methods=["POST"])
def process_make():
    bookingId = request.form.get('bookingId')
    src = request.files.get('img', '')
    # random = request.form.get('random')
    styles = request.form.getlist('styles')

    img = Image.open(src.stream).convert("RGB")
    links = []
    # try:
    # links=process_img_with_ref(img, styles)
    # except err:
    #     print(err)
    #     return jsonify({'msg': 'failed'})
    try:
        links = process_img_with_ref(bookingId, img, styles)
    except:
        return jsonify({'msg': 'failed'})
    # links = process_img_with_ref(bookingId, img, styles)

    return jsonify({'msg': 'success', 'links': links})


@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({'msg': 'hello'})


if __name__ == "__main__":
    app.run(host=app.config['MAIN_IP'], port=8000, debug=True)
