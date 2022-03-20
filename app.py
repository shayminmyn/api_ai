from flask import Flask, request, jsonify
from PIL import Image
from process import process_img,process_img_with_ref
import json

app = Flask(__name__)


app.config.from_object('config.Config')

@app.route("/im_size", methods=["POST"])
def process_image():
    id = request.form.get('userId')
    src = request.files.get('img', '')
    # Read the image via file.stream
    img = Image.open(src.stream).convert("RGB")
    process_img(id,img)
    return jsonify({'msg': 'success'})

@app.route("/makeup", methods=["POST"])
def process_makeup():
    id = request.form.get('userId')
    src = request.files.get('img', '')
    random = request.form.get('random')
    styles = request.form.getlist('styles')
    
    img = Image.open(src.stream).convert("RGB")

    links=[]
    if random is not None:
        links=process_img(id,img)
    elif styles is None:
        links=process_img(id,img)
    else:
        links=process_img_with_ref(id,img, styles)
    
    return jsonify({'msg': 'success','links':links})

@app.route("/make", methods=["POST"])
def process_makeup():
    id = request.form.get('userId')
    src = request.files.get('img', '')
    # random = request.form.get('random')
    styles = request.form.getlist('styles')
    
    img = Image.open(src.stream).convert("RGB")

    links=[]
    
    links=process_img_with_ref(id,img, styles)
    
    return jsonify({'msg': 'success','links':links})




@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({'msg': 'hello'})




if __name__ == "__main__":
    app.run(host=app.config['MAIN_IP'], port=8000, debug=True)