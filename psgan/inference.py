import torch
from PIL import Image

from .solver import Solver
from .preprocess import PreProcess


class Inference:
    
    def __init__(self, config, device="cpu", model_path="assets/models/G.pth"):
        
        self.device = device
        self.solver = Solver(config, device, inference=model_path)
        self.preprocess = PreProcess(config, device)

    def transfer(self, source: Image, reference: Image, with_face=False):
        
        source_input, face, crop_face = self.preprocess(source)
        reference_input, _, _ = self.preprocess(reference)
        if not (source_input and reference_input):
            if with_face:
                return None, None
            return

        for i in range(len(source_input)):
            source_input[i] = source_input[i].to(self.device)
       
        for i in range(len(reference_input)):
            reference_input[i] = reference_input[i].to(self.device)

        # print(source_input[0])
        result = self.solver.test(*source_input, *reference_input)

        # print(result)
        if with_face:
            return result, crop_face
        return result

    def check(self,img: Image):
        input, _, _ = self.preprocess(img)
        if not input:
            return False
        return True
