import json


cleaned_data = []
with open('Grocery_and_Gourmet_Food_verified.json', "r") as f:
    data = f.readlines()
    for i, line in enumerate(data):
        item = json.loads(line)
        item.pop("verified_purchase")
        item.pop("title")
        item.pop("text")
        item.pop("images")
        item.pop("timestamp")
        item.pop("asin")
        cleaned_data.append(item)
        if i%100000 == 0:
            print(i)

with open('Grocery_and_Gourmet_Food_cleaned.json', "w") as f:
    for item in cleaned_data:
        f.write(json.dumps(item) + "\n")