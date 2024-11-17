import json

# Read file into a string
with open('coverage.json', 'r') as f:
    json_string = f.read()

# Parse JSON string into a Python dictionary
json_object = json.loads(json_string)

# Now you can access and manipulate the data in the JSON object as a dictionary
# For example, you can access a specific key in the JSON object
key_value = json_object['totals']

for key, value in json_object['totals'].items():
    print(key, value)

coverage_value = json_object['totals']["percent_covered_display"]
print("coverage value is :"+coverage_value)


