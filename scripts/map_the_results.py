import json
import pandas as pd

# Load JSON data
with open('results_atepc.json', 'r') as f:
    data = json.load(f)

# Load CSV data
csv_file = 'NKD_6k_cleaned_reviews_utf8.csv'  # Replace with the actual CSV file name
reviews_df = pd.read_csv(csv_file)

# Initialize new columns
aspects_list = []
sentiments_list = []
confidence_list = []

# Process each review in the JSON data
for i in range(len(reviews_df)):
    review_data = data.get(str(i), None)
    if review_data:
        aspects = review_data.get('aspect', [])
        sentiments = review_data.get('sentiment', [])
        confidence = review_data.get('confidence', [])

        # Append extracted data to the lists
        aspects_list.append(aspects)
        sentiments_list.append(sentiments)
        confidence_list.append(confidence)
    else:
        # If no data for the review, append empty lists
        aspects_list.append([])
        sentiments_list.append([])
        confidence_list.append([])

# Add new columns to the DataFrame
reviews_df['aspects'] = aspects_list
reviews_df['sentiments'] = sentiments_list
reviews_df['confidence'] = confidence_list

# Save the updated DataFrame to a new CSV file
output_file = 'reviews_with_aspects_2024.csv'
reviews_df.to_csv(output_file, index=False)

print(f"Updated CSV file saved as {output_file}")
