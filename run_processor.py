# run_processor.py
from src.processing.stream_processor import SparkStreamProcessor

if __name__ == "__main__":
    processor = SparkStreamProcessor()
    processor.process_stream()