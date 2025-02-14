"""
The scripts to see the relationships between the aspects,store places and sentiments

"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
from collections import defaultdict

# Aspect mapping
aspect_mapping = {
    'staff': ['staff', 'employees', 'employee', 'workers', 'sellers', 'saleswoman', 'saleswomen', 'salespeople', 'sales staff', 'seller', 'salesperson', 'team', 'assistant', 'personel', 'she', 'lady', 'ladies', 'girls', 'woman', 'man'],
    'price': ['price', 'prices', 'priced', 'cost', 'price performance', 'price range', 'value for money', 'budget', 'cheap', 'expensive', 'discount', 'discounts', 'bargains', 'deal', 'deals', 'sale', 'sales'],
    'quality': ['quality', 'material quality', 'product quality', 'goods', 'items', 'clothing quality', 'material', 'materials', 'condition', 'durability'],
    'store': ['store', 'shop', 'shops', 'branch', 'location', 'place', 'shopping place', 'business', 'retail', 'establishment'],
    'parking': ['parking', 'parking spaces', 'parking space', 'parking lot', 'underground car', 'spaces', 'area'],
    'service': ['service', 'customer service', 'advice', 'help', 'assistance', 'consultation', 'recommendation', 'support', 'management'],
    'atmosphere': ['atmosphere', 'ambience', 'vibe', 'environment', 'decor', 'decoration', 'decorations', 'design', 'motifs', 'appearance'],
    'selection': ['selection', 'assortment', 'range', 'variety', 'options', 'choices', 'collection', 'stock'],
    'space': ['space', 'room', 'area', 'spacious', 'size', 'sizes', 'passageways', 'corridors', 'layout', 'floor'],
    'fashion': ['fashion', 'style', 'clothing', 'clothes', 'textiles', 'garments', 'outfits', 'wardrobe', 'attire'],
    # Add other mappings as necessary
}

# Reverse mapping for easy lookup
reverse_mapping = {synonym: key for key, synonyms in aspect_mapping.items() for synonym in synonyms}

# Load data
file_path = 'reviews_with_aspects_utf8_2024.csv'
data = pd.read_csv(file_path)

data['aspects'] = data['aspects'].apply(literal_eval)
data['sentiments'] = data['sentiments'].apply(literal_eval)

# Map aspects using the aspect_mapping
data['aspects'] = data['aspects'].apply(lambda aspects: [reverse_mapping.get(aspect.lower(), aspect) for aspect in aspects])

# Consolidate selected aspects
selected_aspects = list(aspect_mapping.keys())

store_aspect_sentiment = defaultdict(lambda: defaultdict(list))

for _, row in data.iterrows():
    store = row['placeId']
    aspects = [aspect for aspect in row['aspects'] if aspect in selected_aspects]
    sentiments = row['sentiments'][:len(aspects)]

    for aspect, sentiment in zip(aspects, sentiments):
        store_aspect_sentiment[store][aspect].append(sentiment)

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

result_df.to_csv('store_aspect_sentiment_analysis.csv', index=False)

def visualize_area_vs_sentiment():
    area_sentiment = data.groupby('city')['sentiments'].apply(lambda x: sum(x, []))
    sentiment_counts = area_sentiment.apply(lambda x: pd.Series({'Positive': x.count('Positive'),
                                                                 'Negative': x.count('Negative'),
                                                                 'Neutral': x.count('Neutral')}))
    sentiment_counts.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Area vs Sentiment')
    plt.ylabel('Count')
    plt.xlabel('Area')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('area_vs_sentiment.png')
    # plt.show()

def visualize_aspect_vs_sentiment():
    filtered_df = result_df[result_df['aspect'].isin(selected_aspects)]
    aspect_sentiment = filtered_df.groupby('aspect')[['positive_count', 'negative_count', 'neutral_count']].sum()
    aspect_sentiment.plot(kind='bar', stacked=True, figsize=(12, 7))
    plt.title('Selected Aspects vs Sentiment')
    plt.ylabel('Count')
    plt.xlabel('Aspect')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('aspect_vs_sentiment.png')
    # plt.show()

def visualize_area_vs_aspect():
    area_aspect = data.groupby('city')['aspects'].apply(lambda x: sum(x, []))
    aspect_counts = area_aspect.apply(lambda x: pd.Series(dict(pd.Series([aspect for aspect in x if aspect in selected_aspects]).value_counts())))
    sns.heatmap(aspect_counts.fillna(0), annot=False, cmap='Blues', cbar=True, linewidths=.5)
    plt.title('Area vs Selected Aspects')
    plt.ylabel('Area')
    plt.xlabel('Aspect')
    plt.tight_layout()
    plt.savefig('area_vs_aspect.png')
    # plt.show()

def visualize_area_vs_aspect_sentiment():
    aspect_sentiment_area = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for _, row in data.iterrows():
        area = row['city']
        for aspect, sentiment in zip(row['aspects'], row['sentiments']):
            if aspect in selected_aspects:
                aspect_sentiment_area[area][aspect][sentiment] += 1

    # Convert to DataFrame
    rows = []
    for area, aspects in aspect_sentiment_area.items():
        for aspect, sentiments in aspects.items():
            rows.append({
                'Area': area,
                'Aspect': aspect,
                'Positive': sentiments.get('Positive', 0),
                'Negative': sentiments.get('Negative', 0),
                'Neutral': sentiments.get('Neutral', 0)
            })
    detailed_df = pd.DataFrame(rows)

    # Pivot and plot
    pivot_table = detailed_df.pivot_table(index='Area', columns='Aspect', values=['Positive', 'Negative', 'Neutral'], aggfunc='sum', fill_value=0)
    sns.heatmap(pivot_table.fillna(0), annot=False, cmap='coolwarm', cbar=True, linewidths=.5)
    plt.title('Area vs Selected Aspects/Sentiment')
    plt.ylabel('Area')
    plt.xlabel('Aspect/Sentiment')
    plt.tight_layout()
    plt.savefig('area_vs_aspect_sentiment.png')
    # plt.show()

visualize_area_vs_sentiment()
visualize_aspect_vs_sentiment()
visualize_area_vs_aspect()
visualize_area_vs_aspect_sentiment()

print("Visualizations complete.")


