import logging
import os
from gridfs import GridFS
import pymongo


# db_url = 'mongodb://admin:AbcD%23123%2B%2B@43.135.80.90:27017/'
db_url = 'mongodb://aiyoh:85bff9ac-b381@1.13.102.143:27717/'
db_database = 'dragon'
db_task_table = 'dragon_task'

class MongoConnection:
    """
    Singleton class.
    Manage the connection to MongoDB.
    """
    _instance = None

    def __init__(self) -> None:
        self.connection = pymongo.MongoClient(db_url).get_database(db_database)
        self.collection = self.connection[db_task_table]


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.connection = None
            cls._instance.db = None

        return cls._instance


    def __del__(self):
        self.connection = None
        self.db = None
        MongoConnection._instance = None
    
    #以下两个方法有问题 getdb为none
    def get_db(self):
        # connect
        if self.db is None:
            if self.connection is None:
                self.connection = pymongo.MongoClient(db_url)
            self.db = self.connection[db_database]
            self.collection = self.db[db_task_table]
        return self.db
    
    def get_table(self):
        _db = self.get_db()
        return _db[db_task_table]
      
    def add_one(self, msg):
        # self.get_db()
        try:
            self.collection.insert_one(msg)
        except Exception as e:
            logging.error(f'[ProduceTaskAddDB] ERROR, fail to load Mongodb:   {e}')


    def find_condition(self,condition):
        try:
            return self.collection.find(condition)
        except Exception as e:
            logging.error(f'[ProduceTaskFind] ERROR, fail to load Mongodb:   {e}')


    def find_condition_count(self,condition):
        try:
            return self.collection.count_documents(condition)
        except Exception as e:
            logging.error(f'[ProduceTaskFindCount] ERROR, fail to load Mongodb:   {e}')


  
    
    def upload_file(self,file_name):
        """
        上传图片到MongoDB Gridfs
        :param data_host mongodb 服务器地址
        :param data_db: 数据库地址
        :param data_col:集合
        :param file_name: （图片）文件名称
        :return:
        """

        data_col = 'picture'
        gridfs_col = GridFS(self.connection, collection=data_col)
        filter_condition = {"filename": file_name}
    
        """本地图片上传到MongoDB Gridfs后删除本地文件"""
        with open("%s".decode('utf-8') % file_name, 'rb') as my_image:
            picture_data = my_image.read()
            file_grid = gridfs_col.put(data=picture_data, **filter_condition)  # 上传到gridfs
            logging.info(f'save mongodb gridfs:{file_grid}')
            my_image.close()
            os.remove("%s" % file_name) 
