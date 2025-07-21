import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml
from src.logger.logging import logging
from src.exception.exception import customexception

# Load parameters
def load_params(params_path: str) -> dict:
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.info("Parameters loaded from %s", params_path)
        return params
    except Exception as e:
        logging.info("Exception occurred while loading params.yaml")
        raise customexception(e, sys)


# Basic cleaning (drop tweet_id, binary sentiment filter)
def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df.drop(columns=['tweet_id'], inplace=True)
        df = df[df['sentiment'].isin(['happiness', 'sadness'])]
        df['sentiment'] = df['sentiment'].replace({'sadness': 0, 'happiness': 1})
        logging.info("Data basic cleaning done with happiness/sadness filtering and encoding.")
        return df
    except Exception as e:
        logging.info("Exception during basic_cleaning in data_ingestion.")
        raise customexception(e, sys)


# Save data to raw directory
def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        logging.info(f"Train and test data saved at {raw_data_path}")
    except Exception as e:
        logging.info("Exception occurred during save_data in data_ingestion.")
        raise customexception(e, sys)


def main():
    try:
        params = load_params(params_path="params.yaml")
        ingestion_params = params['data_ingestion']

        source_url = ingestion_params['source_url']
        test_size = ingestion_params['test_size']
        random_state = ingestion_params['random_state']
        data_path = ingestion_params['data_path']

        # Read dataset
        df = pd.read_csv(source_url)
        logging.info("Data read successfully from %s", source_url)

        # Clean data
        df_cleaned = basic_cleaning(df)

        # Train-test split
        train_data, test_data = train_test_split(
            df_cleaned,
            test_size=test_size,
            random_state=random_state,
            stratify=df_cleaned['sentiment']
        )
        logging.info(f"Train-test split done with test_size={test_size}, random_state={random_state}")

        # Save to CSV
        save_data(train_data, test_data, data_path)

        logging.info("Data ingestion pipeline completed successfully.")

    except Exception as e:
        logging.info("Exception occurred in data_ingestion main function.")
        raise customexception(e, sys)


if __name__ == "__main__":
    main()
