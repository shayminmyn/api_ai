from flask import Flask, request, jsonify
from PIL import Image
from process import process_img,process_img_with_ref
import boto3, botocore

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
    if random is not None:
        process_img(id,img)
    elif styles is None:
        process_img(id,img)
    else:
        print(styles)
        process_img_with_ref(id,img, styles)
    
    return jsonify({'msg': 'success'})




@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({'msg': 'hello'})


s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

def upload_file_to_s3(file, bucket_name,img_name, acl="public-read"):

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            img_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type    
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], file.filename)


if __name__ == "__main__":
    app.run(host=app.config['MAIN_IP'], port=8000, debug=True)