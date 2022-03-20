import uuid

import boto3

AWS_REGION = 'ap-southeast-2'
BUCKET_NAME = "fpt-sba-images"
s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id="AKIA2Z5YR2RXSHCH67WC",
    aws_secret_access_key="32bFcB1CTQx/yAaXbJAxOVLausbZ0Xq3g7lIjoGW"
)


def put_object(file) -> str:
    file_key = str(uuid.uuid4()).replace('-', '')
    s3.upload_fileobj(file, BUCKET_NAME, file_key, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image'})
    return f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"




# Usage
# if __name__ == '__main__':
#     with open("ERDDiagram.png", "rb") as f:
#         print(put_object(f))
