# run_training.py
from src.modeling.train_model import FraudDetectionModel

if __name__ == "__main__":
    # Point to the origination data we generated in Phase 1
    data_path = "data/raw/origination_data.csv"
    
    pipeline = FraudDetectionModel(data_path=data_path)
    pipeline.train_and_evaluate(epochs=30, batch_size=16)