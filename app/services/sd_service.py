import io
import re
from typing import Optional
import requests


def generate_image_by_lcm(data) -> Optional[str]:
    response = requests.post(
        "http://localhost:7860/sdapi/v1/img2img",
        json={
            "prompt": "(masterpiece, best quality), cute_shouhui_dragon, solo, dragon, <lora:dragon0117_epoch015_loss0.062:1>, <lora:LCM_lora_weights:1>",
            "negative_prompt": "(worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, (one-eyed:1.5), cross-eyed, ((monochrome)), ((grayscale)), watermark, blurry, mutated hands, text, wordage, (hands:1.5), (fingers:1.5), tooth",
            "mask": data["maskImage"],
            "resize_mode": 0,
            "mask_blur": 0.5,
            "inpainting_mask_invert": False,
            "inpainting_fill": 1,
            "inpaint_full_res": False,
            "inpaint_full_res_padding": 32,
            "sampler_name": "Euler a",
            "steps": 5,
            "width": data["size"]["width"],
            "height": data["size"]["height"],
            "batch_size": 1,
            "cfg_scale": 2,
            "denoising_strength": 0.9,
            "include_init_images": False,
            "init_images": [data["rawImage"]],
            "seed": -1,
            "override_settings": {
                "sd_model_checkpoint": "AnythingV5_v5PrtRE",
                "CLIP_stop_at_last_layers": 1,
                "sd_vae": "Automatic",
            },
            "override_settings_restore_afterwards": False,
            "alwayson_scripts": {
                "controlnet": {
                    "args": [
                        {
                            "input_image": data["mergedImage"],
                            "module": "depth_midas",
                            "model": "control_v11f1p_sd15_depth [cfd03158]",
                            "weight": 1,
                            "pixel_perfect": True,
                            "guidance_start": 0,
                            "guidance_end": 1,
                            "control_mode": 0,
                            "resize_mode": 1,
                            "threshold_a": 64,
                            "save_detected_map": True,
                        }
                    ]
                }
            },
        },
    )

    if response.status_code == 200:
        return response.json()["images"][0]

    return None
