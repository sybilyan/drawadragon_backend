import requests, json, base64

# 将图片转为base64格式的才能进行上传
file_img_doodle = base64.b64encode(open(r"C:/Users/1/Downloads/testimg/weili_doodleImage.jpg", 'rb').read())
file_doodle = base64.b64encode(open(r"C:/Users/1/Downloads/testimg/20240110-180656.png", 'rb').read())
file_raw = base64.b64encode(open(r"C:/Users/1/Downloads/testimg/weili_rawImage.jpg", 'rb').read())
file_img_doodle_decoded = file_img_doodle.decode()
file_doodle_decoded = file_doodle.decode()
file_raw_decoded = file_raw.decode()

url = "http://127.0.0.1:5555/dragon/upload" # 输入服务器IP
url = "https://dragon.aurobitai.com/dragon/getImg/20240113_183629_9cb03860b1ff11eea3b83fceaaad50e0"
mydata = {
    "color":"white",
    "width":512,
    "height":512, 
    "file_raw":file_raw_decoded,
    "file_doodle":file_doodle_decoded,
    "file_img_doodle":file_img_doodle_decoded
    }
mydata = json.dumps(mydata)
headers={"Content-Type": "application/json"}

res = requests.post(url=url, headers=headers, data=mydata)
print("response:", res.text)  # 返回请求结果
