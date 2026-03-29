import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import tensorflow as tf

tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)

import pandas as pd
import mlflow
import mlflow.tensorflow
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#import tensorflow as pd_tf # Aliased to avoid conflicts, standard is tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


class FraudDetectionModel:
    def __init__(self, data_path: str, experiment_name: str = "Fraud_Detection_Experiment"):
        self.data_path = data_path
        self.experiment_name = experiment_name
        self.scaler = StandardScaler()
        self.model = None
        
        # Set up MLflow
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        mlflow.set_experiment(self.experiment_name)
        

    def load_and_preprocess_data(self):
        """Loads data and preprocesses features for the neural network."""
        print("Loading and preprocessing data...")
        df = pd.read_csv(self.data_path)
        
        # Select features and target. 
        # For simplicity in this baseline, we use continuous numerical features.
        features = ['LoanAmount', 'AnnualIncome', 'CreditScore']
        X = df[features]
        y = df['IsFraud']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test

    def build_model(self, input_dim: int):
        """Defines the deep learning architecture."""
        model = Sequential([
            Dense(64, activation='relu', input_shape=(input_dim,)),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(1, activation='sigmoid') # Binary classification for Fraud
        ])
        
        model.compile(optimizer='adam',loss='binary_crossentropy',metrics=[
                                                                            tf.keras.metrics.AUC(name='auc'),
                                                                            tf.keras.metrics.Precision(name='precision'),
                                                                            tf.keras.metrics.Recall(name='recall')
                                                                          ])
        self.model = model
        return model

    def train_and_evaluate(self, epochs: int = 20, batch_size: int = 32):
        """Trains the model and logs everything to MLflow."""
        X_train, X_test, y_train, y_test = self.load_and_preprocess_data()
        self.build_model(input_dim=X_train.shape[1])
        
        print(f"Starting training under MLflow experiment: {self.experiment_name}")
        
        # Start MLflow run
        mlflow.tensorflow.autolog()

        with mlflow.start_run() as run:
            # Enable auto-logging for TensorFlow/Keras
            mlflow.tensorflow.autolog()
            
            # Log custom parameters manually if desired
            mlflow.log_param("epochs", epochs)
            mlflow.log_param("batch_size", batch_size)
            
            # Train the model
            history = self.model.fit(
                X_train, y_train,
                validation_data=(X_test, y_test),
                epochs=epochs,
                batch_size=batch_size,
                verbose=1
            )
            
            # Evaluate on test set
            results = self.model.evaluate(X_test, y_test, verbose=0)
            loss, accuracy, auc = results[0], results[1], results[2]
            
            print(f"\nModel Evaluation -> Loss: {loss:.4f}, Accuracy: {accuracy:.4f}, AUC: {auc:.4f}")
            
            # Log final metrics manually (autolog also captures step-by-step metrics)
            mlflow.log_metric("test_loss", loss)
            mlflow.log_metric("test_accuracy", accuracy)
            mlflow.log_metric("test_auc", auc)
            
            print(f"Run ID {run.info.run_id} successfully logged to MLflow.")