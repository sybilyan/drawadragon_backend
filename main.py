import datetime
import os
from pojo.controlnet_fordragon import SDControlNet
from util.image_util import Image,ImageUtil
from pojo.img2img_fordragon import StableDiffusionImg2ImgVertex
from werkzeug.utils import secure_filename

# from flask_cors import *
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from flask import Flask,request,jsonify
app = Flask(__name__)

# 上传的图片保存路径
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'img')

@app.route('/dragon/upload', methods=[ 'POST'])
def dragon_img2img():
    """
    test text to image feature
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # 获取参数
    params = request.form if request.form else request.json
    inputData_raw = params.get("file_raw")
    inputData_doodle = params.get("file_doodle")
    inputData_img_doodle = params.get("file_img_doodle")
    color = params.get("color")
    width = params.get("width")
    height = params.get('height')

    # 上传文件夹如果不存在则创建
    if not os.path.exists(UPLOAD_PATH):
        os.mkdir(UPLOAD_PATH)

    # load image
    img_raw = ImageUtil.base64_to_image(inputData_raw)

    # load mask
    inputData_doodle = ImageUtil.base64_to_image(inputData_doodle)
    img_doodle = ImageUtil.invert_doodle(inputData_doodle, os.path.join(UPLOAD_PATH, now+"_test_doodle.jpg"))

    #load mask_image
    img_whole = ImageUtil.base64_to_image(inputData_img_doodle)

    #load color
    color_dragon = color+"_dragon"
    prompt = "(masterpiece, best quality), cute_shouhui_dragon, Baring head, solo," + color_dragon + ",(dragon head), eastern dragon, <lora:first_chance0.124:1>"
    negprompt = "(worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, ((monochrome)), ((grayscale)), watermark, bad legs, bad arms, blurry, cross-eyed, mutated hands, text, watermark, wordage, (hand:1.5)"

    ver_config = {
        "params": {
            "url": {
                "value": {
                    "value": "http://127.0.0.1:7860"
                }
            },
            "image": {
                "value": {
                    "value": img_raw
                }
            },
            "mask": {
                "value": {
                    "value": img_doodle
                }
            },
            "control_mask": {
                "value": {
                    "value": img_whole
                }
            },
            "denoising_strength": {
                "value": {
                    "value": 0.89
                }
            },
            "prompt": {
                "type": "string",
                "value": {
                    "connected": 1,
                    "value": [prompt, negprompt]
                }
            },
            "width": {
                "type": "int",
                "value": {
                    "connected": 0,
                    "value": width
                }
            },
            "height": {
                "type": "int",
                "value": {
                    "connected": 0,
                    "value": height
                }
            },
            "seed": {
                "type": "int",
                "value": {
                    "connected": 0,
                    "value": -1
                }
            },
            "batch_size": {
                "type": "int",
                "value": {
                    "connected": 0,
                    "value": 4
                }
            },
            "sd_model_checkpoint": {
                "type": "string",
                "value": {
                    "connected": 0,
                    "value": "AnythingV5_v5PrtRE"
                }
            },
            "plugin": {
                "value": {
                    "value": None
                }
            }

        }
    }

    ctrlnet= SDControlNet(ver_config)
    ctrlnet_out = ctrlnet.process()
    ver_config['params']['plugin']['value']['value'] = ctrlnet_out
    sd = StableDiffusionImg2ImgVertex(data = ver_config)
    output = sd.process()

    for index, img in enumerate(output):
        img.save(f'img/img2img{str(index)}.png')
        
    ret = {"picture":"xxx"}
    return jsonify(content_type='application/json;charset=utf-8',
                   reason='success',
                   charset='utf-8',
                   status='200',
                   content=ret)


if __name__ == '__main__':
    # del_mask_pic()
    # test_img2img()

    app.run(host='0.0.0.0', port=5555)