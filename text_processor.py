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

            # Find all words with wildcards (*)
            wildcard_words = re.findall(r'\b\w*?\*+\w*?\b', text)

            for word in wildcard_words:
                matches = trie.find_all_matches_with_freq(word)
                if matches:
                    # Extract only the words
                    match_words = [m[0] for m in matches]
                    # Format into a single list string like ['word1','word2']
                    replacement = f"[{','.join(repr(w) for w in match_words)}]"
                    # Replace exact matches only
                    pattern_re = re.compile(rf"\b{re.escape(word)}\b")
                    text = pattern_re.sub(replacement, text)

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

            # Find all words with wildcards (*)
            wildcard_words = re.findall(r'\b\w*?\*+\w*?\b', text)

            for word in wildcard_words:
                best_match = trie.find_best_match(word)
                if best_match:
                    replacement = f"<{best_match}>"
                    # Replace exact matches only
                    pattern_re = re.compile(rf"\b{re.escape(word)}\b")
                    text = pattern_re.sub(replacement, text)

            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(text)

        except Exception as e:
            print(f"Error processing file: {e}")