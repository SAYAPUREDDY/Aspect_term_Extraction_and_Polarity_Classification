import pandas as pd
from ast import literal_eval
from collections import defaultdict

# Load the dataset
file_path = 'updated_reviews_2024.csv'
data = pd.read_csv(file_path)

# Parse aspects and sentiments columns
data['aspects'] = data['aspects'].apply(literal_eval)
data['sentiments'] = data['sentiments'].apply(literal_eval)

# Initialize a structure to store relationships
store_aspect_sentiment = defaultdict(lambda: defaultdict(list))

# Process each review
for _, row in data.iterrows():
    store = row['placeId']  # Unique identifier for the store
    aspects = row['aspects']
    sentiments = row['sentiments']

    # Map aspects to sentiments for the store
    for aspect, sentiment in zip(aspects, sentiments):
        store_aspect_sentiment[store][aspect].append(sentiment)

# Aggregate sentiments (e.g., count positives/negatives per aspect)
aggregated_data = {}
for store, aspects in store_aspect_sentiment.items():
    aggregated_data[store] = {
        aspect: {
            'Positive': sentiments.count('Positive'),
            'Negative': sentiments.count('Negative'),
            'Neutral': sentiments.count('Neutral') if 'Neutral' in sentiments else 0
        }
        for aspect, sentiments in aspects.items()
    }

# Convert aggregated data to a DataFrame for analysis
result_df = pd.DataFrame([
    {
        'store': store,
        'aspect': aspect,
        'positive_count': sentiments['Positive'],
        'negative_count': sentiments['Negative'],
        'neutral_count': sentiments['Neutral']
    }
    for store, aspects in aggregated_data.items()
    for aspect, sentiments in aspects.items()
])

# Save the results
result_df.to_csv('store_aspect_sentiment_analysis.csv', index=False)

print("Analysis complete. Results saved to 'store_aspect_sentiment_analysis.csv'.")
