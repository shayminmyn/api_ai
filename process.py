import argparse
from pathlib import Path

from PIL import Image
from psgan import Inference
from fire import Fire
import numpy as np

import faceutils as futils
from psgan import PostProcess
from repositories.pbs_db_repo import insert_new_column
from setup import setup_config, setup_argparser
from service.s3_service import put_object
import tempfile
import uuid
import requests
from io import BytesIO

def process_img(img):
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
        image = inference.transfer(source, reference, with_face=False)
        # source_crop = source.crop(
        #     (face.left(), face.top(), face.right(), face.bottom()))
        # image = postprocess(source_crop, image)
        img_name = str(uuid.uuid4())
        image.save(f"static/images/results/{img_name}_{reference_path.stem}.png")
        path = Path(f"static/images/results/{img_name}_{reference_path.stem}.png")
        with path.open("rb") as f:
            link = put_object(f)
            links.append(link)  
        index = index + 1
        if (index >= 2):
            break
        # if args.speed:
        #     import time
        #     start = time.time()
        #     for _ in range(1):
        #         inference.transfer(source, reference)
        #     print("Time cost for 1 images: ", time.time() - start)
    return links

def check_img(img):
    parser = setup_argparser()
    parser.add_argument(
        "--device",
        default="cpu",
        help="device used for inference")
    parser.add_argument(
        "--model_path",
        default="model/1_1_G.pth",
        help="model for loading")

    args = parser.parse_args()
    config = setup_config(args)
    
    inference = Inference(
        config, args.device, args.model_path)
    return inference.check(img)

def process_img_with_ref(bookingid, img, styles):
    parser = setup_argparser()


    parser.add_argument(
        "--device",
        default="cpu",
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
    links=[]

    
    img_name = str(uuid.uuid4())
    img.save(f"static/images/results/{img_name}_source.png")
    pathSrouce = Path(f"static/images/results/{img_name}_source.png")
    linkSource = ''
    with pathSrouce.open("rb") as f:
        linkSource = put_object(f)

    for reference_path in styles:
        idStyle = reference_path.split('_')[0] #id cu??a style
        name = reference_path.split('_')[1] #name
        pathImg = reference_path.split('_')[2] 
        response = requests.get(pathImg)
        reference = Image.open(BytesIO(response.content)).convert("RGB")

        # reference = Image.open(reference_path).convert("RGB")


        # reference = Image.open(reference_path).convert("RGB")

        # Transfer the psgan from reference to source.
        image, face = inference.transfer(source, reference, with_face=True)
        source_crop = source.crop(
            (face.left(), face.top(), face.right(), face.bottom()))
        image = postprocess(source_crop, image)
        img_name = str(uuid.uuid4())
        image.save(f"static/images/results/{img_name}.png")
        path = Path(f"static/images/results/{img_name}.png")
        with path.open("rb") as f:
            link = put_object(f)
            item = dict()
            item["result"] = link
            item["refer"] = pathImg
            item['source'] = linkSource
            item['bookingId'] = bookingid
            item['idStyle'] = idStyle
            item["name"] = name
            links.append(item)
            
    return links