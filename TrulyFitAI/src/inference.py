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




logged_model = 'runs:/4bc4b3ab71bc43fc96adb9211e65cd58/RandomForest'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on your data.
data = [73.67,56.154249847892025,23.51,23.77596057025652,1.847020496810099] # Code to load a data sample or samples
Anloaded_model.predict(data)