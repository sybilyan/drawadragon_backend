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
    "status":"200"<br>
    }<br>

### http://dragon.aurobitai.com/dragon/getImg GET
  1. 入参：<br>
  "Content-Type": "application/json"<br>
  "data": {<br>
    "task_id":"20240113_183629_9cb03860b1ff11eea3b83fceaaad50e0",<br>
    }<br>

  2. 出参<br>
  会有两个结构<br>
   成功获取图片<br>
  {"status"："200",<br>
  "picture_list":["00.png","01.png","02.png","03.png"]<br>
  }<br>
  仍需等待时间<br>
  {"status"："201",<br>
  "wait_time":20<br>
  }<br>


  先做该接口还没做好，可以在等待时间后，尝试用 <br>
"https://d22742htoga38q.cloudfront.net/dragon/" + task_id + "_0.png"<br>
"https://d22742htoga38q.cloudfront.net/dragon/" + task_id + "_1.png"<br>
"https://d22742htoga38q.cloudfront.net/dragon/" + task_id + "_2.png"<br>
"https://d22742htoga38q.cloudfront.net/dragon/" + task_id + "_3.png"<br>
  获得图片进行展示，获得不了图片正常报错。
  正常get接口返回的地址也是这样拼完返回的。

