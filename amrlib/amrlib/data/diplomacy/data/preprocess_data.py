import spacy
import re

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def is_imperative(doc):
    sentences = list(doc.sents)
    if len(sentences) != 1:
        return False
    for token in doc:
        # Check if the first token is a verb and is the root of the sentence
        if token.head == token and token.pos_ == 'VERB' and token.dep_ == 'ROOT':
            # Ensure it's not a question
            if not doc[-1].text == "?":
                return True
    return False

def replace_imperative(text):
    doc = nlp(text)
    if is_imperative(doc):
      text = 'You ' + text
    return text

def is_interrogative(doc):
    # Check if the sentence ends with a question mark
    if doc[-1].text == "?":
        # Detect if it's a simple verb structure without auxiliary
        if len(doc) > 1 and (doc[0].pos_ == "VERB" or doc[0].text =='DMZ'):
            return "incomplete"
        return True
    return False

def complete_question(text):
    doc = nlp(text)
    completed_sentences = []
    for sent in doc.sents:
        interrogation_type = is_interrogative(sent)
        if interrogation_type == "incomplete":
            # Adding 'Do you want to' to the beginning of the sentence
            completed_sentences.append("Do you want to " + sent.text)
        elif interrogation_type:
            completed_sentences.append(sent.text)
        else:
            completed_sentences.append(sent.text)
    return " ".join(completed_sentences)

# Pronoun replacement function using spaCy
def replace_pronouns_spacy(text, speaker, listener):
    text = text.replace('’','\'')
    text = replace_imperative(text)
    text = complete_question(text)
    doc = nlp(text)
    new_text = []

    # Maps for replacing pronouns
    first_person = {
        "i": speaker,
        "me": speaker,
        "my": f"{speaker}'s",
        "mine": f"{speaker}'s",
        "we": f"{speaker} and {listener}",
        "us": f"{speaker} and {listener}",
        "our": f"{speaker}'s and {listener}'s",
        "ours": f"{speaker}'s and {listener}'s"
    }
    second_person = {
        "you": listener,
        "your": f"{listener}'s",
        "yours": f"{listener}'s",
        "yourself": listener}


    # Iterate over tokens in the text
    prev_text = ''

    for token in doc:
        # print(f'{token}: {token.tag_}')
        # print(prev_text)
        if token.tag_ in ["PRP", "PRP$"] and token.text.lower() in first_person:
            # Replace first person pronouns
            new_text.append(first_person[token.text.lower()])
        elif token.tag_ in ["PRP", "PRP$"] and token.text.lower() in second_person:
            # Replace second person pronouns
            new_text.append(second_person[token.text.lower()])
        else:
            # Add other words as they are
            mod_text = token.text
            if token.tag_ == 'VBP' and prev_text.lower() in ["i","you","we"] and token.text in ["\'re","are","am","\'m"]:
              mod_text = 'is'
            new_text.append(mod_text)
        prev_text = token.text

    new_text = " ".join(new_text)
    new_doc = nlp(new_text)
    new_text = correct_contractions(new_doc)
    new_text = clean_text(new_text)
    # Recreate the sentence
    return new_text

def correct_contractions(doc):
    corrected_sentence = []
    skip = False

    for i, token in enumerate(doc):
        if skip:
            skip = False
            continue

        # Check if current token is the start of a contraction
        if i + 1 < len(doc) and doc[i + 1].text == "n't":
            corrected_sentence.append(token.text + "n't")
            skip = True
        else:
            corrected_sentence.append(token.text)

    return ' '.join(corrected_sentence)

def clean_text(text):
    # Remove space before commas, periods, or apostrophes
    cleaned_text = re.sub(r'\s+([,.\'?:;])', r'\1', text)
    # Ensure one space after commas or periods if not followed by a space or end of string
    cleaned_text = re.sub(r'([,\.])(?=[^\s])', r'\1 ', cleaned_text)
    return cleaned_text

def extract_and_replace(line):
    # Extracts speaker and listener from the given line
    match = re.search(r'^(# ::snt )(\w+) send to (\w+) that (.+)$', line)
    if match:
        new_text = replace_pronouns_spacy(match.group(4), match.group(2), match.group(3))
        # Construct the new line with the extracted speaker and listener
        new_line = f"{match.group(1)}{match.group(2)} send to {match.group(3)} that {new_text}\n"
        return new_line, match.group(2), match.group(3)
    return line, None, None


# Example sentence
sentence = "Yeah, I can’t say I’ve tried it and it works, cause I’ve never tried it or seen it. But how I think it would work is (a) my Spring move looks like an attack on Austria, so it would not be surprising if you did not cover Munich. Then (b) you build two armies, which looks like we’re really at war and you’re going to eject me. Then we launch the attack in Spring. So there is really no part of this that would raise alarm bells with France.  All that said, I’ve literally never done it before, and it does involve risk for you, so I’m not offended or concerned if it’s just not for you. I’m happy to play more conventionally too. Up to you."
# Replace pronouns
transformed_sentence = replace_pronouns_spacy(sentence, 'Italy', 'Austria')
transformed_sentence

# Path to the original file
input_path = './test.txt'
output_path = './modified_test.txt'

# Reading the original file and writing the modified content to a new file
with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    speakers_listeners = []
    for line in infile:
        modified_line, speaker, listener = extract_and_replace(line)
        outfile.write(modified_line)
        if speaker and listener:
            speakers_listeners.append((speaker, listener))
