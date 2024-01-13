import logging
import time
import traceback

from confluent_kafka import Producer
from task.mongo_connection import MongoConnection


kafka_url = "119.45.243.21:9092"     
kafka_topic = "dragon_task_test"       
kafka_group = "g_drago_task_test"

class KafkaProducerConnection:
    """
    Singleton class.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.producer = None

        return cls._instance


    def __del__(self):
        # self.producer.close()
        self.producer = None
        KafkaProducerConnection._instance = None
    


    def get_producer(self):
        # connect
        if self.producer is None:
            conf = {
                'bootstrap.servers': kafka_url
            }
            self.producer = Producer(conf)
            
        return self.producer


class TaskProducer():
    """
    Produce task and sent it to Kafka periodically.
    """

    def __init__(self) -> None:
        self.collection = None
        self.kfk_topic = kafka_topic


    def produce_one_task(self, task, flush=True):
        """
        Produce one task to kafka
        """
        # send to kafka
        # msg = bytes(task, encoding='utf-8')
        producer = KafkaProducerConnection().get_producer()
        producer.produce(self.kfk_topic, value= task)
        logging.info(f'[ProduceTask] send msg to Kafka success')

        if flush:
            producer.flush()
            logging.info(f'[ProduceTask] flush producer.')


    def run_test(self):
        """
        Produce task periodically.
        """
        try:
            logging.info('[Producer]: start.')
            self.collection = MongoConnection().get_table()

            logging.info('[DB] connection DONE.')
            self.producer = KafkaProducerConnection().get_producer()
            logging.info('[Kafka] connection DONE.')

            while True:

                try:
                    data_doc = self.collection.find(
                        {'status': 0}
                    )
                    
                    for doc in data_doc:
                        task_id = doc['taskId']
                        self.produce_one_task(task_id, flush=False)

                    # flush kafka producer
                    self.producer.flush()
                    
                except Exception as e:
                    logging.error(f"[Error] image_task. {e}\n{traceback.format_exc()}")

                time.sleep(10) #second


        finally:
            self.producer.close()


if __name__ == "__main__":

    task_consumer = TaskProducer()
    task_consumer.run()



