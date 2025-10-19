# Model training - base model
# tracking with mlflow
# Import the specific regression models from scikit-learn
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

data = pd.read_csv("./artifacts/ml_training_data.csv")
data.columns


# split into train test set
X_train = data.drop(columns="calories")
y_train = data.calories


# Preprocessing pipeline

# defining numerical and categorical columns

# preprocessing pipeline the numerical features that is all the features in the dataset
# defining pipeline
num_pipeline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
# pipeline for  the log transformation to handle skew features
log_pipeline = make_pipeline(
    SimpleImputer(strategy="median"),
    FunctionTransformer(np.log, feature_names_out="one-to-one"),
    StandardScaler(),
)


# building the preprocessing pipeline
preprocessing = make_column_transformer(
    (num_pipeline, make_column_selector(dtype_include=np.number)),
    (log_pipeline, make_column_selector(dtype_include=np.number)),
)


# Instantiate each model

models = {
    "RandomForest": RandomForestRegressor(random_state=42),
    "XGBoost": XGBRegressor(random_state=42, n_estimators=500, learning_rate=0.05),
    "LightGBM": LGBMRegressor(random_state=42, n_estimators=500, learning_rate=0.05),
    "LinearRegression": LinearRegression(),
    "Ridge_Model": Ridge(alpha=1.0, random_state=42),
    "Lasso_Model": Lasso(alpha=0.1, random_state=42),
    "Elastic_Net_Model": ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42),
    "KNN_Model": KNeighborsRegressor(n_neighbors=5),
    "SVM_Model": SVR(kernel="rbf"),
    "Decision_Tree": DecisionTreeRegressor(),
}


# training scipt
# tracking url
# os.environ['MLFLOW_TRACKING_URI']="https://dagshub.com/abiolaks/TrulyFitAI.mlflow"
# os.environ['MLFLOW_TRACKING_USERNAME']="abiolaks"
# os.environ["MLFLOW_TRACKING_PASSWORD"]="3d5376f582499caded3df9ed9ac74941da8b0128"

mlflow.set_tracking_uri("https://dagshub.com/abiolaks/TrulyFitAI.mlflow")
with mlflow.start_run():
    signature = infer_signature(X_train, y_train)
    pipelines = {}  # A dictionary to store the final pipelines
    results = {}

    # Capture a sample input for the model signature
    # This is a single row or a small batch from the training data
    input_example = X_train.iloc[[0]]

    for name, model in models.items():
        # Wrap the current model with TransformedTargetRegressor to handle the target (y) scaling
        # wrapped_model = TransformedTargetRegressor(
        # regressor=model,
        # transformer=StandardScaler()
        # )

        # Create the full pipeline: features are scaled, then the wrapped model is applied
        full_pipeline = make_pipeline(preprocessing, model)

        # Store the complete pipeline for the current model
        pipelines[name] = full_pipeline

        # Fit the complete pipeline
        print(f"Fitting {name}...")
        full_pipeline.fit(X_train, y_train)
        preds = full_pipeline.predict(X_train)

        ## Log metrics \
        # Create the dictionary of metrics
        metrics = {
            f"train_RMSE_{name}": np.sqrt(mean_squared_error(y_train, preds)),
            f"train_MAE_{name}": mean_absolute_error(y_train, preds),
            f"train_R2_{name}": r2_score(y_train, preds),
        }

        # Store metrics in the results dictionary for later
        results[name] = metrics

        # Log all metrics at once to MLflow with a single function call
        mlflow.log_metrics(metrics)

        # Log the trained pipeline model
        mlflow.sklearn.log_model(
            sk_model=full_pipeline, artifact_path=name, input_example=input_example
        )

    results_df = pd.DataFrame(results)
    print(results_df)

# Now you can use the `pipelines` dictionary to make predictions
# For example:
# predictions = pipelines['Linear Regression'].predict(X_test)
