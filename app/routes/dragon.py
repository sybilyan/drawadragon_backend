from fastapi import APIRouter, Body, HTTPException, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketState

from app.services.socket_service import handle_websocket_client


dragon_router = APIRouter()


import datetime
import json
import logging
import os
import traceback
from app.task.kafka_producer import TaskProducer
from app.task.mongo_connection import MongoConnection
import uuid

# from flask_cors import *
os.environ["NLS_LANG"] = "SIMPLIFIED CHINESE_CHINA.UTF8"


# 上传的图片保存路径
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), "img")

# 设置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

# 设置将日志输出到文件中，并且定义文件内容
file_info = logging.FileHandler(f"logs/AutoTest_log_{now}.log")
file_info.setLevel(logging.INFO)
file_info.setFormatter(formatter)

# 设置将日志输出到控制台
control_show = logging.StreamHandler()
control_show.setLevel(logging.INFO)
control_show.setFormatter(formatter)


logger.addHandler(file_info)
logger.addHandler(control_show)

avg_time = 30


@dragon_router.post("/upload")
async def dragon_img2img(payload: dict = Body(...)):
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
    task_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    task_id = task_time + "_" + uuid.uuid1().hex
    count = 0

    try:
        params = payload

        task_params_db = {"taskId": task_id, "dealStatus": 0, "taskDetail": params}
        # logging.info(f'[Producer]: start. with task_param:{task_params_db}')

        # 连接mongodb并添加一条任务
        mongodb_collection_dragon = MongoConnection()
        mongodb_collection_dragon.add_one(task_params_db)
        logging.info(f"[ProduceDB] update status to 0, task id:{task_id}")

        # 查询有多少条任务在等待
        condition = {"status": 0}
        count = mongodb_collection_dragon.find_condition_count(condition)
        logging.info(f"[ProduceDB] current task count:{count}")

        task_params_kafka = {
            "taskId": task_id,
            # "taskDetail": params
        }
        # 连接kafka 并添加一条任务
        # 发送消息
        task_params_kafka = json.dumps(task_params_kafka, ensure_ascii=False)
        task_consumer = TaskProducer()
        task_consumer.produce_one_task(task_params_kafka)
        logging.info(f"[ProduceKafka] add to kafka with task:{task_id}")

    except Exception as e:
        logger.error(f"[Error] image_task. {e}\n{traceback.format_exc()}")

    count_time = avg_time * (count + 1)

    ret = {"task_id": task_id, "wait_time": count_time}
    return ret


@dragon_router.get("/getImg/{taskId}", status_code=200)
async def dragon_getImg(taskId: str = None):
    # 连接mongodb并添加一条任务
    mongodb_collection_dragon = MongoConnection()
    # 查询任务是否已完成
    try:
        condition = {"taskId": taskId}
        find_task_num = mongodb_collection_dragon.find_condition_count(condition)
        print(find_task_num)
    except Exception as e:
        logger.error(f"[getImg] ERROR, fail to load Mongodb:   {e}")
    if find_task_num > 1:
        logger.error(f"[Error] current_task has wrong count, taskId {taskId} ")
        raise HTTPException(status_code=501, detail="current_task num wrong")
    if find_task_num == 0:
        logger.error(f"[Error] current_task NOT FIND, taskId {taskId} ")
        raise HTTPException(status_code=502, detail="current_task NOT FIND")
    find_task = mongodb_collection_dragon.find_condition(condition)
    print(find_task)
    if find_task[0]["dealStatus"] != 2:
        # 查询有多少条任务在等待
        condition = {"status": 0}
        count = mongodb_collection_dragon.find_condition_count(condition)
        count_time = avg_time * (count + 1)
        return JSONResponse(status_code=201, content={"wait_time": count_time})

    else:
        pic_list = [
            "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/dragon/"
            + taskId
            + "_"
            + str(i)
            + ".png"
            for i in range(4)
        ]
        return pic_list


@dragon_router.websocket("/draw")
async def handle_redraw(client: WebSocket):
    """create a websocket connection to generate image by drawing at realtime

    Args:
        client (WebSocket): client websocket connection
    """
    await client.accept()

    try:
        await handle_websocket_client(client)

    except Exception as err:
        print(f"connection closed by error")

        # don't need close
        # if client.client_state != WebSocketState.DISCONNECTED:
        #     await client.close()
