# trie.py
# Two Features by Shu Zhi
# Shu Zhi
# DAAA/2A/03

from trie import PrefixTrie
from text_processor import TextProcessor

class twoFeaturesSZ:
    def __init__(self):
        self.trie = PrefixTrie()
        self.text_processor = TextProcessor()

    def restore_with_confidence(self, word_with_wildcards):
        matches = self.get_matching_words(word_with_wildcards)
        if not matches:
            return None
        total_freq = sum(freq for word, freq in matches)
        matches.sort(key=lambda x: x[1], reverse=True)
        for word, freq in matches:
            confidence = (freq / total_freq) * 100
            print(f"{word} (Confidence: {confidence:.2f}%)")
        return matches[0][0]  # Return best match
    
    def manual_freq_editor(self, )