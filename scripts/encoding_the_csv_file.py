import chardet

# Function to detect the file's encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

# Function to convert file to UTF-8
def convert_to_utf8(input_file, output_file):
    # Detect encoding of the input file
    encoding = detect_encoding(input_file)
    print(f"Detected encoding: {encoding}")

    # Read the file with detected encoding and save as UTF-8
    with open(input_file, 'r', encoding=encoding) as infile:
        content = infile.read()
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
    print(f"File converted to UTF-8 and saved as: {output_file}")

# Specify input and output file paths
input_file_path = 'reviews_with_aspects_2024.csv'  # Replace with the file you want to convert
output_file_path = 'reviews_with_aspects_utf8_2024.csv'  # The converted UTF-8 file

# Convert the file to UTF-8
convert_to_utf8(input_file_path, output_file_path)
