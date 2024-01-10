# drawadragon_backend
backend for draw a dragon 

## 使用代码

  1. 本地运行SD起到7860端口后运行main.py

  2. python client.py可以模拟调用
  
## API

### /dragon/upload POST

  1. 入参：
  "Content-Type": "application/json"
  "data": {
    "color":"white",
    "width":512,
    "height":512, 
    "file_raw":file_raw_decoded,(图片转为base64格式)
    "file_doodle":file_doodle_decoded,(图片转为base64格式)
    "file_img_doodle":file_img_doodle_decoded(图片转为base64格式)
    }

  2. 出参
  response: {
    "charset":"utf-8",
    "content":{"picture":"xxx"},
    "content_type":"application/json;charset=utf-8",
    "reason":"success",
    "status":"200"
    }


