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