import torch

class ScaleToTargetMegapixels:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "megapixels": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0, "step": 0.1})
            }
        }

    CATEGORY = "image"
    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("upscale", "downscale", "upscale_if_need", "downscale_if_need", )
    OUTPUT_NODE = True
    
    FUNCTION = "scale"

    def scale(self, image, megapixels):
        height, width = image.shape[1], image.shape[2]
        current_megapixels = (height * width) / 1_000_000
        
        if megapixels <= 0:
            raise ValueError("Megapixels must be greater than 0")
        
        upscale = (megapixels / current_megapixels) ** 0.5
        downscale = (current_megapixels / megapixels) ** 0.5
        
        upscale_if_need = upscale
        downscale_if_need = downscale
        
        if current_megapixels < megapixels:
            upscale_if_need = 1.0
            downscale_if_need = 1.0       
        
        
        text = [f"upscale: {upscale} downscale: {downscale} upscale_if_need: {upscale_if_need} downscale_if_need: {downscale_if_need}"]
        
        print(text)
        
        return {"ui": {"text": text}, "result": (upscale, downscale, upscale_if_need, downscale_if_need)}


NODE_CLASS_MAPPINGS = {"ScaleToTargetMegapixels": ScaleToTargetMegapixels}
