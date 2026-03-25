# run_producer.py
from src.streaming.producer import LoanPerformanceProducer

if __name__ == "__main__":
    # Point it to the performance data we generated in Phase 1
    data_path = "data/raw/performance_data.csv"
    
    producer = LoanPerformanceProducer(topic='loan-performance')
    producer.stream_data(csv_file_path=data_path, speed_seconds=0.05)