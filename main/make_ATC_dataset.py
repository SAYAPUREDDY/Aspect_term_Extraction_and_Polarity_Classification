"""
This script will take the file with only reviews and split them into train/test and valid and will provide the following results:

- train.csv: 70% of the original data
- valid.csv: 15% of the original data
- test.csv: 15% of the original data

- train.csv.apc: Train data converted to apc format
- test.csv.apc: Test data converted to apc format
- valid.csv.apc: Valid data converted to apc format

- train.csv.atepc: Train data converted to atepc format
- test.csv.atepc: Test data converted to atepc format
- valid.csv.atepc: valid data converted to atepc format

"""

# import pandas as pd
# from sklearn.model_selection import train_test_split
from pyabsa import make_ABSA_dataset

# df = pd.read_csv("C:/Users/91965/SSST/Google_Review_Analysis/New folder/NKD_REVIEWS_CLEANED_only_reviews_utf8.csv")

# train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)  # 70% train, 30% temp
# valid_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)  # 15% validation, 15% test

# train_df.to_csv('segmented_data/train.csv', index=False)
# valid_df.to_csv('segmented_data/valid.csv', index=False)
# test_df.to_csv('segmented_data/test.csv', index=False)

make_ABSA_dataset(dataset_name_or_path="segmented_data/train.csv", checkpoint='english')

make_ABSA_dataset(dataset_name_or_path='segmented_data/valid.csv', checkpoint='english')

make_ABSA_dataset(dataset_name_or_path='segmented_data/test.csv', checkpoint='english')
