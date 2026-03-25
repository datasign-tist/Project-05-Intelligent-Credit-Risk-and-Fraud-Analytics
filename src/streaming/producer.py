import json
import time
import pandas as pd
from confluent_kafka import Producer

class LoanPerformanceProducer:
    def __init__(self, bootstrap_servers: str = 'localhost:9092', topic: str = 'loan-performance'):
        self.topic = topic
        self.conf = {'bootstrap.servers': bootstrap_servers}
        self.producer = Producer(self.conf)

    def delivery_report(self, err, msg):
        """Callback triggered upon message delivery to Kafka."""
        if err is not None:
            print(f"Message delivery failed: {err}")
            
        # Uncomment the line below if you want to see every single message confirmation, 
        # but it gets noisy!
        # else:
        #     print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def stream_data(self, csv_file_path: str, speed_seconds: float = 0.1):
        """Reads CSV and streams rows to Kafka as JSON."""
        df = pd.read_csv(csv_file_path)
        print(f"Starting to stream {len(df)} records to Kafka topic '{self.topic}'...")
        
        for _, row in df.iterrows():
            record = row.to_dict()
            json_record = json.dumps(record)
            
            # Produce the message to the topic
            self.producer.produce(
                self.topic, 
                value=json_record.encode('utf-8'), 
                callback=self.delivery_report
            )
            
            # Trigger callbacks to handle delivery reports
            self.producer.poll(0)
            
            # Simulate real-time streaming delay
            time.sleep(speed_seconds)
            
        # Wait for any outstanding messages to be delivered
        self.producer.flush()
        print("Streaming completed.")