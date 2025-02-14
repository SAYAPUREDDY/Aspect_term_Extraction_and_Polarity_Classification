"""
This script performs aspect term extraction and polarity classification on a dataset of reviews using a pre-trained PyABSA model. 
It reads the reviews from a CSV file, processes each review to extract aspect terms and sentiments, and saves the results in a JSON file. 

Note: make sure to replace your checkpoints with the ones from the exsisting checkpoints.

returns: 

 results_atepc.json: A JSON file containing sentence,IOB,Tokens,Aspect,Position,Sentiment,Probs,Confidence.
 
"""
from pyabsa import available_checkpoints
from pyabsa import AspectTermExtraction as ATEPC
import pandas as pd
import json

results_dict = {}

data = pd.read_csv('data_for_analysis/NKD_REVIEWS_CLEANED_only_reviews_utf8.csv')
reviews = data['textTranslated']
print(len(reviews))

ckpts = available_checkpoints()

aspect_extractor = ATEPC.AspectExtractor(
    checkpoint="english" 
)

for i in range(10):  
    atepc_example = reviews[i]  
    try:
        result = aspect_extractor.predict(
            text=atepc_example,
            save_result=False,  
            print_result=True,
            ignore_error=True,  
            eval_batch_size=32,
        )
        
        results_dict[i] = result 
    except Exception as e:
        print(f"Error processing review {i}: {e}")


with open("results_atepc_10reviews.json", "w") as json_file:
    json.dump(results_dict, json_file)

print("Dictionary saved to results_atepc.json")





