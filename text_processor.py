# text_processor.py
# ST1507 CA2 - Text Processing for Newspaper Restoration
# Shu Zhi and Ashley
# DAAA/2A/03

import re

class TextProcessor:
    def __init__(self):
        pass

    def restore_text_all_matches(self, input_file, output_file, trie):
        """
        Restore text from input file using all possible matches from the trie
        and save the restored text to output file.
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as infile:
                text = infile.read()

            # Find all words with wildcards (*) - simple and effective pattern
            # This matches any sequence of letters and asterisks that contains at least one asterisk
            wildcard_words = re.findall(r'[a-zA-Z]*\*[a-zA-Z]*', text)
            # Remove empty matches and duplicates
            wildcard_words = list(set([w for w in wildcard_words if w and w != '*']))

            print(f"Found wildcard words: {wildcard_words}")  # Debug output

            for word in wildcard_words:
                matches = trie.find_all_matches_with_freq(word)
                if matches:
                    # Extract only the words from the (word, frequency) tuples
                    match_words = [match[0] for match in matches]
                    # Format into a single list string like ['word1','word2']
                    replacement = f"[{','.join(repr(w) for w in match_words)}]"
                    # Use word boundary regex to replace exact matches only
                    pattern_re = re.compile(rf"\b{re.escape(word)}\b")
                    text = pattern_re.sub(replacement, text)
                    print(f"Replaced '{word}' with {replacement}")  # Debug output
                else:
                    print(f"No matches found for '{word}'")  # Debug output

            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(text)

        except Exception as e:
            print(f"Error processing file: {e}")

    def restore_text_best_matches(self, input_file, output_file, trie):
        """
        Restore text from input file using best matches from the trie
        and save the restored text to output file.
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as infile:
                text = infile.read()

            # Find all words with wildcards (*) - improved pattern
            # This pattern captures any sequence containing asterisks and word characters
            wildcard_words = re.findall(r'\b[\w*]*\*[\w*]*\b', text)

            print(f"Found wildcard words: {wildcard_words}")  # Debug output

            for word in wildcard_words:
                best_match = trie.find_best_match(word)
                if best_match:
                    replacement = f"<{best_match}>"
                    # Use word boundary regex to replace exact matches only
                    pattern_re = re.compile(rf"\b{re.escape(word)}\b")
                    text = pattern_re.sub(replacement, text)
                    print(f"Replaced '{word}' with {replacement}")  # Debug output
                else:
                    print(f"No match found for '{word}'")  # Debug output

            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(text)

        except Exception as e:
            print(f"Error processing file: {e}")