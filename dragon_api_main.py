import datetime
import json
import logging
import os
import traceback
from task.kafka_producer import TaskProducer
from task.mongo_connection import MongoConnection
import uuid

# from flask_cors import *
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from flask import Flask,request,jsonify
app = Flask(__name__)

# 上传的图片保存路径
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'img')

#设置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
#设置将日志输出到文件中，并且定义文件内容
fileinfo = logging.FileHandler(f"logs/AutoTest_log_{now}.log")
fileinfo.setLevel(logging.INFO) 
fileinfo.setFormatter(formatter)
#设置将日志输出到控制台
controlshow = logging.StreamHandler()
controlshow.setLevel(logging.INFO)
controlshow.setFormatter(formatter)


logger.addHandler(fileinfo)
logger.addHandler(controlshow)

task_id = now +"_"+ uuid.uuid1().hex
@app.route('/dragon/upload', methods=[ 'POST'])
def dragon_img2img():
    """
    test text to image feature
    """

    """
    todo:
    1、上传mongodb,json,生成id, 状态为 0-排队中 1-正在生成 2-已完成
    2、查询mongodb中状态未完成的有多少,计算时间
    3、发kafka任务
    4、返回id和计算时间  
    """
    count = 0
    try:
        params = request.form if request.form else request.json

        task_params_db ={
                "taskId": task_id,
                'dealStatus': 0, 
                "taskDetail": params
                }
        # logging.info(f'[Producer]: start. with task_param:{task_params_db}')
        
        # 连接mongodb并添加一条任务
        mongodb_collection_dragon = MongoConnection()
        mongodb_collection_dragon.add_one(task_params_db)
        logging.info(f'[ProduceDB] update status to 0, task id:{task_id}')

        # 查询有多少条任务在等待
        condition = {'status': 0}
        count = mongodb_collection_dragon.find_cond_count(condition)
        logging.info(f'[ProduceDB] current task count:{count}')
        
        task_params_kafka ={
                "taskId": task_id,
                "taskDetail": params
                }
        # 连接kafka 并添加一条任务
        # 发送消息
        task_params_kafka = json.dumps(task_params_kafka, ensure_ascii=False)
        task_consumer = TaskProducer()
        task_consumer.produce_one_task(task_params_kafka)
        logging.info(f"[ProduceKafka] add to kafka with task:{task_id}")

    except Exception as e:
        logger.error(f"[Error] image_task. {e}\n{traceback.format_exc()}")
    
    count_time = 20*(count+1)
    ret = {"task_id":task_id,
           "wait_time":count_time}
    return (jsonify(content_type='application/json;charset=utf-8',
                   reason='success',
                   charset='utf-8',
                   status='200',
                   content=ret))

# @app.route('/dragon/getImg', methods=[ 'GET'])
# def dragon_getImg():     
   

if __name__ == '__main__':
    # del_mask_pic()
    # test_img2img()

    app.run(host='0.0.0.0', port=5555)

    