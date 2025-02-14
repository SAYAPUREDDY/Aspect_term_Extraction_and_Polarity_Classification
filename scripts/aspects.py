from collections import Counter
import ast  # To safely evaluate strings containing lists

import pandas as pd

csv_file = 'reviews_with_aspects_utf8_2024.csv'  # Replace with the actual CSV file name
reviews_data = pd.read_csv(csv_file)
# Flatten the 'aspects' column into a single list of all aspects
all_aspects = []
for aspects in reviews_data['aspects']:
    if isinstance(aspects, str):  # Ensure the data is a string
        aspect_list = ast.literal_eval(aspects)  # Convert string to list
        all_aspects.extend(aspect_list)

# Count the occurrences of each unique aspect
aspect_counts = Counter(all_aspects)

# Convert to a DataFrame for better readability
aspect_counts_df = pd.DataFrame(aspect_counts.items(), columns=['aspects', 'Count'])
aspect_counts_df = aspect_counts_df.sort_values(by='Count', ascending=False)

# Display the most repeated aspects
print(aspect_counts_df)  # Top 10 most repeated aspects

output_file_path = 'aspect_counts.txt'  # Specify the desired file path
aspect_counts_df.to_csv(output_file_path, index=False, sep='\t')

print(f"Aspect counts saved to {output_file_path}")
