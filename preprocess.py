import json


valid_data = []
with open('Grocery_and_Gourmet_Food.jsonl', "r") as f:
    data = f.readlines()
    print(len(data))
    for line in data:
        item = json.loads(line)
        if item["verified_purchase"] == True:
            valid_data.append(item)

print(len(valid_data))
with open('Grocery_and_Gourmet_Food_verified.json', "w") as f:
    for item in valid_data:
        f.write(json.dumps(item) + "\n")