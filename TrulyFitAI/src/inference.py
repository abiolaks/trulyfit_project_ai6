from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
import os
import subprocess
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




logged_model = 'runs:/4bc4b3ab71bc43fc96adb9211e65cd58/RandomForest'

# Load model as a PyFuncModel.
mlflow.pyfunc.get_model_dependencies(logged_model)
loaded_model = mlflow.pyfunc.load_model(logged_model)

# get dependences for model
deps_path = mlflow.pyfunc.get_model_dependencies(logged_model, format="pip")

# Install the dependencies from the file
subprocess.check_call(["pip", "install", "-r", deps_path])


data = [73.67, 56.154249847892025, 23.51, 23.77596057025652, 1.847020496810099]

batch_data_raw = [
    [52.62, 41.043628751488114, 20.3, 21.99994536015182, 1.838274420372482],
    [69.47, 49.409032892617006, 26.47, 28.877165837603265, 1.1872750827695409],
    [81.51, 60.636696765010285, 20.38, 25.60827289288397, 0.941602257391731]
]

# The column names from the error message
column_names = [
    'weight_(kg)',
    'lean_mass_kg',
    'bmi',
    'fat_percentage',
    'protein_per_kg'
]

# Convert the data into a DataFrame with named columns
#data_df = pd.DataFrame([data], columns=column_names)
data_df = pd.DataFrame(batch_data_raw, columns=column_names)

# Load your model (assuming it's already loaded in your script)
# loaded_model = mlflow.pyfunc.load_model(...)

# Predict with the correctly formatted DataFrame

predictions = loaded_model.predict(data_df)

print(np.round(predictions).astype(int))

# Predict on your data.
