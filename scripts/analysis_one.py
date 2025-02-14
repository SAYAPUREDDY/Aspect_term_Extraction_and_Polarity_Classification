import pandas as pd
import ast
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('updated_reviews_2024.csv')

# Convert stringified lists in 'aspects', 'sentiments', and 'confidence' columns to actual lists
data['aspects'] = data['aspects'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
data['sentiments'] = data['sentiments'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
data['confidence'] = data['confidence'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

# Analyze relationships between aspects, sentiments, and locations
def analyze_aspects_sentiments(data):
    aspect_sentiment_data = []
    for idx, row in data.iterrows():
        place_id = row['placeId']
        city = row['city']
        for aspect, sentiment in zip(row['aspects'], row['sentiments']):
            aspect_sentiment_data.append({'placeId': place_id, 'city': city, 'aspect': aspect, 'sentiment': sentiment})
    return pd.DataFrame(aspect_sentiment_data)

# Generate a clean dataset for analysis
aspect_sentiment_df = analyze_aspects_sentiments(data)

# Aggregate sentiments by aspects and store locations
summary = aspect_sentiment_df.groupby(['city', 'aspect', 'sentiment']).size().reset_index(name='count')

# Visualization: Sentiment Distribution by Aspect
plt.figure(figsize=(12, 6))
aspect_counts = Counter([item for sublist in data['aspects'] for item in sublist])
aspects, counts = zip(*aspect_counts.most_common(10))
plt.bar(aspects, counts, color='skyblue')
plt.title('Top 10 Aspects Mentioned in Reviews')
plt.xlabel('Aspects')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()

# Visualization: Heatmap of Sentiments across Cities and Aspects
heatmap_data = summary.pivot_table(index='aspect', columns='city', values='count', aggfunc='sum', fill_value=0)
plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='coolwarm')
plt.title('Heatmap of Sentiments by Aspects and Cities')
plt.xlabel('City')
plt.ylabel('Aspect')
plt.show()

# Save the processed aspect-sentiment data for further use
aspect_sentiment_df.to_csv('/mnt/data/aspect_sentiment_analysis.csv', index=False)

print("Analysis complete! Results have been saved to 'aspect_sentiment_analysis.csv'.")
