import json

with open("results_for_synthetic_reviews_atepc.json") as json_file:
    json_data = json.load(json_file)
    # print(json_data)

# print(json_data["0"]["aspect"])
print(json_data["8"]["aspect"])