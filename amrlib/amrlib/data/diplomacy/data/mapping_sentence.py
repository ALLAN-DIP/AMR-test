import json
import re

with open("output_file.json", "r") as json_file:
    dictionary = json.load(json_file)

def replace_values_with_keys(sentence):
    for key, values in dictionary.items():
        for value in values:
            sentence = re.sub(r'\b' + re.escape(value) + r'\b', key, sentence)
    return sentence

with open("./test_cicero_original.txt", "r") as text_file:
    lines = text_file.readlines()

processed_lines = []
for line in lines:
    if line.startswith("# ::snt"):
        sentence = line.strip().split("# ::snt ")[1]
        processed_sentence = replace_values_with_keys(sentence)
        processed_lines.append("# ::snt " + processed_sentence + "\n")
    else:
        processed_lines.append(line)

with open("./test/test.txt", "w") as text_file:
    text_file.writelines(processed_lines)
