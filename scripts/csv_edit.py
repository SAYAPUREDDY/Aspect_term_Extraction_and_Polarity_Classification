import pandas as pd

# Input file path
file_path = 'data/NKD_REVIEWS_DATA.csv'  # Replace with your actual file path

# Output file paths
reviews_file_path = 'NKD_REVIEWS_WITH_REVIEWS.csv'  # Rows with valid reviews
no_reviews_file_path = 'NKD_REVIEWS_WITHOUT_REVIEWS.csv'  # Rows without reviews

# Load the dataset (use 'latin1' encoding if 'utf-8' raises errors)
data = pd.read_csv(file_path, encoding='latin1')

# Split the dataset into two parts
reviews_data = data.dropna(subset=['textTranslated'])  # Rows with valid reviews
no_reviews_data = data[data['textTranslated'].isna()]  # Rows without reviews

# Save each part to separate CSV files
reviews_data.to_csv(reviews_file_path, index=False, encoding='utf-8')
no_reviews_data.to_csv(no_reviews_file_path, index=False, encoding='utf-8')

print(f"File with reviews saved as: {reviews_file_path}")
print(f"File without reviews saved as: {no_reviews_file_path}")









