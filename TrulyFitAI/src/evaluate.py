from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
import os
from mlflow.models import infer_signature
import pandas as pd

# from urlib.parse import urlparse
import mlflow

# from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from dotenv import load_dotenv
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.compose import make_column_selector, make_column_transformer
import numpy as np
from mlflow.tracking import MlflowClient
import mlflow.sklearn

# Environment variables .env file
load_dotenv()


# Connection Dagshub
os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_TRACKING_URI")
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")


# load data from the artifact folder version 1- before it was preprocessed
# we will run it through a preprocessin pipeline

data = pd.read_csv("../artifacts/ml_test_data.csv")
data.columns


# split into train test set
X_test = data.drop(columns="calories")
y_test = data.calories

# Set the MLflow tracking URI to your DagsHub repository
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Find the latest run (or the best run based on your criteria)
# This assumes you have already logged the models
runs_df = mlflow.search_runs(
    filter_string="",
    order_by=["start_time DESC"],
    max_results=1
)
if not runs_df.empty:
    RUN_ID = runs_df.iloc[0]["run_id"]
    print(f"Found best run with ID: {RUN_ID}")
else:
    raise ValueError("No MLflow runs found.")


client = MlflowClient()
artifacts = client.list_artifacts(RUN_ID)

# List artifacts using the mlflow.artifacts API
model_paths = []
for artifact in artifacts:
    if artifact.is_dir:
        # FIXED: use path= instead of artifact_path=
        sub_artifacts = client.list_artifacts(RUN_ID, path=artifact.path)
        if any(sa.path.endswith("MLmodel") for sa in sub_artifacts):
            model_paths.append(artifact.path)

# --- 3. Loop through models and evaluate ---
test_results = {}


with mlflow.start_run(run_name="Test Set Evaluation"):
    # Log the ID of the training run for traceability
    mlflow.log_param("parent_training_run_id", RUN_ID)
    
    for model_path in model_paths:
        # Construct the model URI to load the pipeline from DagsHub
        model_uri = f"runs:/{RUN_ID}/{model_path}"
        
        print(f"Loading model from path: {model_path}...")
        loaded_pipeline = mlflow.sklearn.load_model(model_uri)
        
        print(f"Evaluating {model_path} on test set...")
        test_preds = loaded_pipeline.predict(X_test)
        
        # Calculate and log metrics on the test set
        test_metrics = {
            f"test_RMSE_{model_path}": np.sqrt(mean_squared_error(y_test, test_preds)),
            f"test_MAE_{model_path}": mean_absolute_error(y_test, test_preds),
            f"test_R2_{model_path}": r2_score(y_test, test_preds)
        }
        
        mlflow.log_metrics(test_metrics)
        test_results[model_path] = test_metrics

# --- 4. Print the results ---
test_results_df = pd.DataFrame(test_results)
print("\nTest Set Evaluation Results:")
print(test_results_df)



