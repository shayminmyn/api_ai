class Config(object):
    GPU = True
    SAVED_MODEL_PATH = 'model'

    UPLOAD_DIR = 'static/image_upload/'
    CARTOON_DIR = 'static/cartoonize/'
    GPU = True

    MAIN_IP = '127.0.0.1'

    S3_BUCKET = "fpt-sba-images"
    S3_KEY = "AKIA2Z5YR2RXSHCH67WC"
    S3_SECRET = "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"
    S3_LOCATION = "http://{}.s3.amazonaws.com/".format(S3_BUCKET)

