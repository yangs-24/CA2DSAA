# confidence_restorer.py
# Custom Feature: Restore Word with Confidence Score
# Contributor: Shu Zhi Yang
# DAAA/2A/03

from trie import PrefixTrie
from text_processor import TextProcessor

class ConfidenceRestorer:
    def __init__(self):
        self.trie = PrefixTrie()
        self.text_processor = TextProcessor()
    
    def restore_with_confidence(self, word_with_wildcards):
        """
        Restore a wildcard word using matches from the trie and show confidence scores.
        """
        matches = self.trie.find_all_matches(word_with_wildcards)
        if not matches:
            print(f"No matches found for '{word_with_wildcards}'.")
            return

        # Calculate total frequency
        total_frequency = 0
        word_frequencies = []
        for word in matches:
            node = self.trie.root
            for char in word:
                if char in node.children:
                    node = node.children[char]
                else:
                    node = None
                    break
            if node and node.is_terminal:
                word_frequencies.append((word, node.frequency))
                total_frequency += node.frequency

        if total_frequency == 0:
            print("Cannot calculate confidence scores due to zero total frequency.")
            return

        print(f"Restoring: {word_with_wildcards}")
        print("Possible Matches with Confidence Scores:")
        for word, freq in word_frequencies:
            confidence = (freq / total_frequency) * 100
            print(f" - {word} ({confidence:.2f}%)")

    def restore_confidence_menu(self):
        """
        Display the menu for restoring words with confidence scores.
        """
        print("\nConfidence Restorer Menu:")
        print("1. Restore Word with Wildcards")
        print("2. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            word_with_wildcards = input("Enter the word with wildcards (e.g., 'c_t'): ")
            self.restore_with_confidence(word_with_wildcards)
        elif choice == '2':
            print("Exiting Confidence Restorer.")
        else:
            print("Invalid choice, please try again.")