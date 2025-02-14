import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Load the aggregated sentiment analysis data
result_df = pd.read_csv('C:/Users/91965/SSST/1.My_Git_Clones/Aspect_term_Extraction_and_Polarity_Classification/store_aspect_sentiment_analysis.csv')

# Load the original data with aspect and sentiment mappings
file_path = 'C:/Users/91965/SSST/1.My_Git_Clones/Aspect_term_Extraction_and_Polarity_Classification/reviews_with_aspects_utf8_2024.csv'
data = pd.read_csv(file_path)

# Load location mapping data with placeId, address, and city
location_address_mapping = pd.read_csv(file_path)  # Assuming the file has `placeId`, `address`, and `city` columns.

# Function to filter data by placeId
def get_store_data(store_id):
    return result_df[result_df['store'] == store_id]

def get_store_address(store_id):
    """Fetch the store address and city based on store ID."""
    address_row = location_address_mapping[location_address_mapping['placeId'] == store_id]
    if not address_row.empty:
        address = address_row.iloc[0]['address']
        city = address_row.iloc[0]['city']
        return f"{address}, {city}"
    return "Address not found"

def visualize_store_aspect_sentiments(store_id):
    store_data = get_store_data(store_id)
    if store_data.empty:
        st.write("No data found for the selected Store ID.")
        return

    # Plot aspect sentiments
    store_data = store_data[['aspect', 'positive_count', 'negative_count', 'neutral_count']]
    store_data.set_index('aspect', inplace=True)
    store_data.plot(kind='bar', stacked=True, figsize=(12, 7), color=['green', 'red', 'gray'])
    plt.title(f'Sentiment Analysis for Store ID: {store_id}')
    plt.ylabel('Count')
    plt.xlabel('Aspect')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

def visualize_area_vs_sentiment():
    """Visualize area vs sentiment counts."""
    aspect_sentiment_area = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for _, row in data.iterrows():
        area = row['city']
        for aspect, sentiment in zip(eval(row['aspects']), eval(row['sentiments'])):
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
    st.pyplot(plt)

def visualize_area_vs_aspect():
    """Visualize area vs aspect counts."""
    area_aspect = data.groupby('city')['aspects'].apply(lambda x: sum(eval(x), []))
    aspect_counts = area_aspect.apply(lambda x: pd.Series(dict(pd.Series(x).value_counts())))
    sns.heatmap(aspect_counts.fillna(0), annot=False, cmap='Blues', cbar=True, linewidths=.5)
    plt.title('Area vs Selected Aspects')
    plt.ylabel('Area')
    plt.xlabel('Aspect')
    plt.tight_layout()
    st.pyplot(plt)

def visualize_aspect_vs_sentiment():
    """Visualize aspect sentiment counts."""
    filtered_df = result_df[['aspect', 'positive_count', 'negative_count', 'neutral_count']]
    aspect_sentiment = filtered_df.groupby('aspect')[['positive_count', 'negative_count', 'neutral_count']].sum()
    aspect_sentiment.plot(kind='bar', stacked=True, figsize=(12, 7))
    plt.title('Selected Aspects vs Sentiment')
    plt.ylabel('Count')
    plt.xlabel('Aspect')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit GUI
st.title("Store Sentiment Analysis Dashboard")

# Store ID Input
store_id = st.text_input("Enter place ID (placeId):", "")

if store_id:
    # Fetch the address for the store ID
    address = get_store_address(store_id)

    # Display the address
    st.subheader(f"Sentiment Analysis for Store: {address}")

    # Show aspects categorized as Positive, Negative, and Neutral side by side
    store_data = get_store_data(store_id)
    if not store_data.empty:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("### Positive Aspects")
            positive_aspects = store_data[store_data['positive_count'] > 0][['aspect', 'positive_count']]
            st.write(positive_aspects)

        with col2:
            st.write("### Negative Aspects")
            negative_aspects = store_data[store_data['negative_count'] > 0][['aspect', 'negative_count']]
            st.write(negative_aspects)

        with col3:
            st.write("### Neutral Aspects")
            neutral_aspects = store_data[store_data['neutral_count'] > 0][['aspect', 'neutral_count']]
            st.write(neutral_aspects)

        # Graph selection for the store
        if st.checkbox("Show Aspect Sentiment Visualization for Store"):
            st.subheader("Aspect Sentiment Visualization")
            visualize_store_aspect_sentiments(store_id)
    else:
        st.write("No data available for this Store ID.")


# General Insights
st.subheader("General Insights")

# Graph selection for general insights
if st.checkbox("Show Area vs Sentiment Visualization"):
    visualize_area_vs_sentiment()

if st.checkbox("Show Area vs Aspects"):
    visualize_area_vs_aspect()

if st.checkbox("Show Aspect vs Sentiment"):
    visualize_aspect_vs_sentiment()

