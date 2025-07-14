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
                # Find all matches for the wildcard word
                matches = trie.find_all_matches(word)
                if matches:
                    # Format matches as a list
                    formatted_matches = [f"['{match[0]}']" for match in matches]
                    replacement = '|'.join(formatted_matches)
                    text = text.replace(word, replacement)
            
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
                # Find the best match for the wildcard word
                best_match = trie.find_best_match(word)
                if best_match:
                    # Format the best match with angle brackets
                    replacement = f"<{best_match[0]}>"
                    text = text.replace(word, replacement)
            
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(text)
                
        except Exception as e:
            print(f"Error processing file: {e}")