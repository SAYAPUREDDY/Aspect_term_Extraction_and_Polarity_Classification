import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox

file_path = 'updated_reviews_2024.csv'
data = pd.read_csv(file_path)

data['aspects'] = data['aspects'].apply(literal_eval)
data['sentiments'] = data['sentiments'].apply(literal_eval)

selected_aspects = ['staff', 'saleswoman', 'quality', 'clothing', 'store', 'place', 'parking', 'nice', 'good', 'cheap', 'collection', 'customer care', 'friendly', 'price']

store_aspect_sentiment = defaultdict(lambda: defaultdict(list))

for _, row in data.iterrows():
    store = row['placeId']
    aspects = [aspect for aspect in row['aspects'] if aspect in selected_aspects]
    sentiments = row['sentiments'][:len(aspects)]

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

# Visualization setup
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
    # plt.savefig('area_vs_sentiment.png')
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
    # plt.savefig('data/aspect_vs_sentiment.png')
    # plt.show()

def visualize_area_vs_aspect():
    area_aspect = data.groupby('city')['aspects'].apply(lambda x: sum(x, []))
    aspect_counts = area_aspect.apply(lambda x: pd.Series(dict(pd.Series([aspect for aspect in x if aspect in selected_aspects]).value_counts())))
    sns.heatmap(aspect_counts.fillna(0), annot=False, cmap='Blues', cbar=True, linewidths=.5)
    plt.title('Area vs Selected Aspects')
    plt.ylabel('Area')
    plt.xlabel('Aspect')
    plt.tight_layout()
    # plt.savefig('data/area_vs_aspect.png')
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
    # plt.savefig('/mnt/data/area_vs_aspect_sentiment.png')
    # plt.show()

# GUI for user interaction
def show_aspects_by_store():
    def fetch_results():
        store_input = store_entry.get()
        if store_input in store_aspect_sentiment:
            aspects_data = store_aspect_sentiment[store_input]
            result = []
            for aspect, sentiments in aspects_data.items():
                if aspect in selected_aspects:
                    positive = sentiments.count('Positive')
                    negative = sentiments.count('Negative')
                    neutral = sentiments.count('Neutral')
                    result.append(f"Aspect: {aspect}, Positive: {positive}, Negative: {negative}, Neutral: {neutral}")
            if result:
                result_text.set("\n".join(result))
            else:
                result_text.set("No relevant aspects found for this store.")
        else:
            messagebox.showerror("Error", "Store not found in the data.")

    # GUI setup
    root = tk.Tk()
    root.title("Store Aspect Sentiment Analysis")

    tk.Label(root, text="Enter Store Address/ID:").grid(row=0, column=0, padx=10, pady=10)
    store_entry = ttk.Entry(root, width=40)
    store_entry.grid(row=0, column=1, padx=10, pady=10)

    fetch_button = ttk.Button(root, text="Fetch Sentiment Data", command=fetch_results)
    fetch_button.grid(row=1, column=0, columnspan=2, pady=10)

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT, wraplength=400, anchor="w")
    result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

# Call visualization functions
# visualize_area_vs_sentiment()
# visualize_aspect_vs_sentiment()
# visualize_area_vs_aspect()
# visualize_area_vs_aspect_sentiment()

# Launch GUI
show_aspects_by_store()

print("Visualizations and GUI complete.")
