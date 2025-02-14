import pandas as pd
from langdetect import detect
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize translator
translator = Translator()

# Language detection function
def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "unknown"

# Translation function
def translate_if_german(text):
    """
    Translates text to English if detected as German (language code: 'de').
    """
    if not text or text.strip() == "":  # Handle empty or whitespace-only reviews
        return text  # Return as-is for empty text
    
    lang = detect_language(text)
    if lang == "de":  # Check if the language is German
        try:
            translated_text = translator.translate(text, src='de', dest='en').text
            return translated_text
        except Exception as e:
            print(f"Error translating: {text[:50]}... - {e}")
            return text  # Return original if translation fails
    else:
        return text  # Return as-is if not German

# Processing function for batch application
def process_reviews(reviews, max_workers=10):
    """
    Processes a list of reviews: translates German reviews to English.
    Uses multithreading for efficiency.
    """
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks to the executor
        future_to_review = {executor.submit(translate_if_german, review): review for review in reviews}
        for future in as_completed(future_to_review):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error processing a review: {e}")
                results.append("[ERROR]")  # Mark errors for manual inspection
    return results

# Main workflow
def main(input_file, output_file):
    """
    Reads a dataset, translates German reviews to English, and saves the output.
    """
    # Load dataset
    print("Loading dataset...")
    data = pd.read_csv(input_file)
    
    # Check if 'text' column exists
    if 'text' not in data.columns:
        raise KeyError("'text' column not found in the dataset.")
    
    # Fill missing values in 'text' with empty strings
    data['text'] = data['text'].fillna("")
    
    # Process reviews in batches and replace German reviews in the same column
    print(f"Processing {len(data)} reviews...")
    data['text'] = process_reviews(data['text'], max_workers=10)
    
    # Save processed data
    print(f"Saving processed dataset to {output_file}...")
    data.to_csv(output_file, index=False)
    print("Processing complete.")

# Run script
if __name__ == "__main__":
    input_file = 'final_reviews_data - Copy.csv'  # Input file name
    output_file = 'processed_reviews.csv'  # Output file name
    main(input_file, output_file)

