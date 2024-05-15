import json
with open('mapping_province.json', 'r') as file:
    dataset = json.load(file)

transformed_dataset = {}

for key, value in dataset.items():
    new_key = value[0]
    value.remove(new_key)
    value.insert(0, key)
    value.append(key.upper())
    value.append(key.capitalize())
    transformed_dataset[new_key] = value

output_file = 'output_file.json'
with open(output_file, 'w') as file:
    json.dump(transformed_dataset, file, indent=4)

print(f"Transformed dataset saved into '{output_file}'")
