import logging
from confluent_kafka import Producer


class KafkaHandler(logging.Handler):
    def __init__(self, topic, **kwargs):
        super().__init__()
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def emit(self, record):
        msg = self.format(record)
        self.producer.produce(self.topic, msg)
