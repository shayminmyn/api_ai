import argparse
from pathlib import Path

from PIL import Image
from psgan import Inference
from fire import Fire
import numpy as np

import faceutils as futils
from psgan import PostProcess
from setup import setup_config, setup_argparser
from service.s3_service import put_object
import tempfile
import uuid
import requests
from io import BytesIO

def process_img(id,img):
    parser = setup_argparser()

    parser.add_argument(
        "--reference_dir",
        default="static/images/makeup",
        help="path to reference images")
    parser.add_argument(
        "--speed",
        action="store_true",
        help="test speed")
    parser.add_argument(
        "--device",
        default="cuda",
        help="device used for inference")
    parser.add_argument(
        "--model_path",
        default="model/1_1_G.pth",
        help="model for loading")

    args = parser.parse_args()
    config = setup_config(args)

    # Using the second cpu
    inference = Inference(
        config, args.device, args.model_path)
    postprocess = PostProcess(config)

    source = img
    reference_paths = list(Path(args.reference_dir).glob("*"))
    np.random.shuffle(reference_paths)
    index = 0
    links = []
    for reference_path in reference_paths:
        if not reference_path.is_file():
            print(reference_path, "is not a valid file.")
            continue

        reference = Image.open(reference_path).convert("RGB")

        # Transfer the psgan from reference to source.
        image, face = inference.transfer(source, reference, with_face=True)
        source_crop = source.crop(
            (face.left(), face.top(), face.right(), face.bottom()))
        image = postprocess(source_crop, image)
        img_name = str(uuid.uuid4())
        image.save(f"static/images/results/{img_name}_{id}_{reference_path.stem}.png")
        path = Path(f"static/images/results/{img_name}_{id}_{reference_path.stem}.png")
        with path.open("rb") as f:
            link = put_object(f)
            links.append(link)  
        index = index + 1
        if (index >= 5):
            break
        # if args.speed:
        #     import time
        #     start = time.time()
        #     for _ in range(1):
        #         inference.transfer(source, reference)
        #     print("Time cost for 1 images: ", time.time() - start)
    return links

def process_img_with_ref(id,img, styles):
    parser = setup_argparser()

    parser.add_argument(
        "--reference_dir",
        default="static/images/makeup",
        help="path to reference images")
    parser.add_argument(
        "--speed",
        action="store_true",
        help="test speed")
    parser.add_argument(
        "--device",
        default="cuda",
        help="device used for inference")
    parser.add_argument(
        "--model_path",
        default="model/1_1_G.pth",
        help="model for loading")

    args = parser.parse_args()
    config = setup_config(args)

    # Using the second cpu
    inference = Inference(
        config, args.device, args.model_path)
    postprocess = PostProcess(config)

    source = img
    temp = list(Path(args.reference_dir).glob("*"))
    reference_paths = []
    links=[]
    for x in temp:
        if x.stem in styles:
            print(x.stem)
            reference_paths.append(x)
    for reference_path in styles:
        response = requests.get(reference_path)
        reference = Image.open(BytesIO(response.content)).convert("RGB")

        # reference = Image.open(reference_path).convert("RGB")


        # reference = Image.open(reference_path).convert("RGB")

        # Transfer the psgan from reference to source.
        image, face = inference.transfer(source, reference, with_face=True)
        source_crop = source.crop(
            (face.left(), face.top(), face.right(), face.bottom()))
        image = postprocess(source_crop, image)
        img_name = str(uuid.uuid4())
        image.save(f"static/images/results/{img_name}_{id}_{reference_path.stem}.png")
        path = Path(f"static/images/results/{img_name}_{id}_{reference_path.stem}.png")
        with path.open("rb") as f:
            link = put_object(f)
            links.append(link)  
    return links