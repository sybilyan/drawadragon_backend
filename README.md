# drawadragon_backend
backend for draw a dragon 

## 使用代码
  1. sh build_env.sh
  2. sh restart.sh
  
## API
python请求脚本示例可参见client.py

### http://dragon.aurobitai.com/dragon/upload POST

  1. 入参：<br>
  "Content-Type": "application/json"<br>
  "data": {<br>
    "color":"white",<br>
    "width":512,<br>
    "height":512, <br>
    "file_raw":file_raw_decoded,(图片转为base64格式)<br>
    "file_doodle":file_doodle_decoded,(图片转为base64格式)<br>
    "file_img_doodle":file_img_doodle_decoded(图片转为base64格式)<br>
    }<br>

  2. 出参<br>
  response: {<br>
    "charset":"utf-8",<br>
    "content":{"task_id":"20240113_183629_9cb03860b1ff11eea3b83fceaaad50e0",
           "wait_time":20},<br>
    "content_type":"application/json;charset=utf-8",<br>
    "reason":"success",<br>
    "status":200<br>
    }<br>

### http://dragon.aurobitai.com/dragon/getImg GET
  1. 入参：<br>
  "Content-Type": "application/json"<br>
  "data": {<br>
    "task_id":"20240113_183629_9cb03860b1ff11eea3b83fceaaad50e0",<br>
    }<br>

  2. 出参<br>
  成功会有两个结构<br>
   成功获取图片<br>
   {<br>
    "charset": "utf-8",<br>
    "content_type": "application/json;charset=utf-8",<br>
    "picture_list": [<br>
        "https://d22742htoga38q.cloudfront.net/dragon/20240115_132952_1c08cff0b36711ee9391ac50de795704_0.png",<br>
        "https://d22742htoga38q.cloudfront.net/dragon/20240115_132952_1c08cff0b36711ee9391ac50de795704_1.png",<br>
        "https://d22742htoga38q.cloudfront.net/dragon/20240115_132952_1c08cff0b36711ee9391ac50de795704_2.png",<br>
        "https://d22742htoga38q.cloudfront.net/dragon/20240115_132952_1c08cff0b36711ee9391ac50de795704_3.png"<br>
    ],
    "reason": "success",<br>
    "status": 200<br>
   }<br>

  仍需等待时间<br>
   {<br>
    "charset": "utf-8",<br>
    "content_type": "application/json;charset=utf-8",<br>
    "wait_time": 20,<br>
    "reason": "success",<br>
    "status": 201<br>
   }<br>

   失败结构<br>
   {<br>
    "charset": "utf-8",<br>
    "content_type": "application/json;charset=utf-8",<br>
    "reason": "current_task num wrong",<br>
    "status": 501<br>
   }<br>

   {<br>
    "charset": "utf-8",<br>
    "content_type": "application/json;charset=utf-8",<br>
    "reason": "current_task NOT FIND",<br>
    "status": 502<br>
   }<br>




