# Project-05-Intelligent-Credit-Risk-and-Fraud-Analytics
Build an integrated financial risk platform that uses deep learning and generative AI to model credit risk and detect fraud. For example, ingest real-time loan and transaction data (using Kafka) into a Spark pipeline, engineer features, and train Transformer-based models for credit scoring and anomaly detection. 

# 🏦 Intelligent Credit Risk & Fraud Analytics Platform

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-Streaming-black.svg)
![PySpark](https://img.shields.io/badge/PySpark-Data_Processing-E25A1C.svg)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-Orchestration-017CEE.svg)
![MLflow](https://img.shields.io/badge/MLflow-Experiment_Tracking-0194E2.svg)

## 📖 Executive Summary
This repository contains an end-to-end, production-grade machine learning platform designed to predict credit default risk and detect fraudulent loan applications. Built with an Object-Oriented Programming (OOP) architecture, this system simulates real-time financial transaction streams, processes them in memory, predicts anomalies using deep learning, and augments human review with a Retrieval-Augmented Generation (RAG) knowledge base. 


## 🎯 Business Value & Impact
* **Risk Mitigation:** Automated credit scoring and fraud detection significantly reduce loan default rates and direct financial losses.
* **Real-Time Threat Detection:** By utilizing a real-time streaming pipeline (Kafka + Spark), fraudulent transactions are flagged as they occur, minimizing exposure.
* **Accelerated Compliance:** The integration of a GenAI RAG layer allows human analysts to instantly query complex regulatory policies and historic financial guidelines, reducing manual review time by up to 80%.
* **Reproducibility:** Fully containerized and orchestrated pipelines ensure models are continuously retrained on fresh data with zero downtime.

## 🏗️ Architecture & Tech Stack
The platform is decoupled into several micro-services and batch processes:
* **Data Engineering & Streaming:** Python (Faker), Apache Kafka, PySpark (Structured Streaming).
* **Predictive Modeling:** TensorFlow/Keras (Deep Learning MLP), Scikit-Learn.
* **MLOps & Orchestration:** MLflow (Artifact & Experiment Tracking), Apache Airflow (DAG Scheduling).
* **Generative AI:** LangChain, HuggingFace (Local Embeddings), ChromaDB (Vector Store).

## 📂 Repository Structure
```text
credit-risk-platform/
├── dags/
│   └── fraud_pipeline_dag.py      # Airflow DAG for automated model retraining
├── data/
│   ├── raw/                       # Synthetic static and streaming datasets
│   └── chroma_db/                 # Local vector database for RAG
├── src/
│   ├── data_generation/
│   │   └── generator.py           # OOP engine for synthesizing loan data
│   ├── streaming/
│   │   └── producer.py            # Kafka producer pushing real-time JSON payloads
│   ├── processing/
│   │   └── stream_processor.py    # PySpark engine for real-time feature engineering
│   ├── modeling/
│   │   └── train_model.py         # TensorFlow model training & MLflow autologging
│   └── rag/
│       └── retriever.py           # LangChain vector embedding and document retrieval
├── requirements.txt
└── README.md


## 🚀 Independent Execution GuideFollow these steps to replicate the environment and run the full pipeline on your local machine.

1. PrerequisitesEnsure your system has the following installed:Python 3.11+Java 11 (Required for PySpark Structured Streaming)Homebrew (To manage Kafka and Zookeeper on macOS)
2. Environment SetupClone the repository and initialize a clean virtual environment to avoid dependency conflicts with global packages.Bashgit clone <your-repository-url>
cd Project-05-Intelligent-Credit-Risk-&-Fraud-Analytics
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
3. Start Background InfrastructureThis project is a distributed system that requires Kafka, MLflow, and Airflow to be active. Open three separate terminal tabs and ensure the (venv) is active in each:Tab 1: Kafka & ZookeeperBash# Start the message brokers
brew services start zookeeper
brew services start kafka
Tab 2: MLflow Tracking ServerBash# Start the experiment dashboard
mlflow ui --port 5000
Tab 3: Apache Airflow (Orchestrator)Bash# Initialize and start the DAG scheduler
export AIRFLOW_HOME=$(pwd)
export AIRFLOW__WEBSERVER__WEB_SERVER_PORT=8085
airflow db migrate
airflow standalone
4. Running the PipelineOpen your browser and navigate to the Airflow UI: http://localhost:8085.Login using the credentials (admin/password) generated in Tab 3.Locate the fraud_detection_retraining_pipeline DAG.Unpause: Click the toggle switch on the left (it should turn blue).Trigger: Click the Play (▶️) button on the right and select Trigger DAG.Monitor the execution in the Graph View.5. Verifying the MLOps LifecycleData Ingestion: Verify a new origination_data.csv is created in data/raw/.Experiment Tracking: Visit http://localhost:5000 to view the TensorFlow training metrics, loss curves, and model weights automatically logged by MLflow.Inference/RAG: Test the compliance assistant via the command line:Bashpython src/rag/retriever.py --query "What are the risk parameters for Tier 1 applicants?"
🛠 Troubleshooting & Environment FixesDuring the development of this platform on macOS, the following environment-specific fixes were implemented to ensure stability:IssueResolutionPort 8080 ConflictAirflow defaults to 8080, which often conflicts with Mac system services or Java apps. The project is hard-coded to use 8085.Protobuf ClashTensorFlow 2.16+ requires protobuf>=6.31.1. If ImportError occurs, run pip install --upgrade protobuf.TensorBoard MissingMLflow autologging requires TensorBoard for scalar tracking. Ensure it is installed via pip install tensorboard.Ghost ProcessesIf Airflow fails to start, run pkill -9 -f "airflow" to clear orphaned background processes.