import csv
from serpapi import GoogleSearch

csv_file = "place_ids_nkd_stores.csv"

with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Place ID", "Address", "Location"])

while True:
    location = input("Provide the location (or type 'exit' to stop): ").strip()
    if location.lower() == 'exit':
        print("Exiting...")
        break

    params = {
        "engine": "google_maps",
        "q": f"NKD stores in {location}",
        "api_key": "43f3aa987a9b666bc9b563e64a1670d54419aa48544f2f955e9b95170d8f10bb"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    stores = results.get("local_results", [])
    if not stores:
        print(f"No results found for {location}.")
    else:
        with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for store in stores:
                place_id = store.get("place_id", "N/A")
                address = store.get("address", "N/A")
                writer.writerow([place_id, address, location])

        print(f"Results for {location} saved to {csv_file}.")

