import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import pickle

from src.exceptions import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")  # Saving as preprocessor.pkl

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        '''
        This function creates the full preprocessing object (pipeline) for data transformation.
        '''
        try:
            # Defining numerical columns for preprocessing
            numerical_columns = ['temperature', 'exhaust_vacuum', 'amb_pressure', 'r_humidity']

            # Creating a pipeline for numerical features: Imputation + Scaling
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            logging.info(f"Numerical Columns: {numerical_columns}")

            # Combining all transformations in a ColumnTransformer
            preprocessor = ColumnTransformer(
                [("num_pipeline", num_pipeline, numerical_columns)]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data successfully.")

            logging.info("Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = "energy_production"
            numerical_columns = ['temperature', 'exhaust_vacuum', 'amb_pressure', 'r_humidity']

            # Splitting input and target features for train and test
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Applying the preprocessor to the data
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combining input and target features into final arrays
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saving the preprocessing object as preprocessor.pkl.")

            # Saving the preprocessing object (full pipeline)
            with open(self.data_transformation_config.preprocessor_obj_file_path, 'wb') as file_obj:
                pickle.dump(preprocessing_obj, file_obj)

            return train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path

        except Exception as e:
            raise CustomException(e, sys)