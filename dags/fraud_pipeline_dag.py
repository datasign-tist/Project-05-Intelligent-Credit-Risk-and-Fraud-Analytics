import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Default settings
default_args = {
    'owner': 'data_scientist',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_fresh_data():
    """Task 1: Generate new synthetic data."""
    # 1. Add project root to path inside the function
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if PROJECT_ROOT not in sys.path:
        sys.path.append(PROJECT_ROOT)
        
    # 2. INLINE IMPORT: Only load the heavy modules when the task runs
    from src.data_generation.generator import LoanDataGenerator
    
    # 3. Use absolute paths to guarantee data goes to the right place
    raw_data_path = os.path.join(PROJECT_ROOT, "data", "raw")
    os.makedirs(raw_data_path, exist_ok=True)
    
    generator = LoanDataGenerator(num_loans=1000)
    generator.generate_and_save(raw_data_path=raw_data_path)

def retrain_fraud_model():
    """Task 2: Train the model on the newly generated data."""
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if PROJECT_ROOT not in sys.path:
        sys.path.append(PROJECT_ROOT)
        
    from src.modeling.train_model import FraudDetectionModel
    
    data_path = os.path.join(PROJECT_ROOT, "data", "raw", "origination_data.csv")
    pipeline = FraudDetectionModel(data_path=data_path)
    pipeline.train_and_evaluate(epochs=15, batch_size=32)

# Initialize the DAG
with DAG(
    'fraud_detection_retraining_pipeline',
    default_args=default_args,
    description='A scheduled pipeline to generate data and retrain the fraud model',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['credit_risk', 'mlops'],
) as dag:

    task_generate_data = PythonOperator(
        task_id='generate_synthetic_data',
        python_callable=generate_fresh_data,
    )

    task_train_model = PythonOperator(
        task_id='train_mlflow_model',
        python_callable=retrain_fraud_model,
    )

    task_generate_data >> task_train_model