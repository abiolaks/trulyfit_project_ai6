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
import mlflow.sklearn

# Environment variables .env file
load_dotenv()


# Connection Dagshub
os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_TRACKING_URI")
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")


# load data from the artifact folder version 1- before it was preprocessed
# we will run it through a preprocessin pipeline

data = pd.read_csv("../data/interim/test_set.csv")
data.columns


# split into train test set
X_test = data.drop(columns="calories")
y_test = data.calories