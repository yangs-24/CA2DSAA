# manual_freq_editor.py
# Custom Feature: Manual Frequency Editor
# Contributor: Shu Zhi Yang
# DAAA/2A/03

from trie import PrefixTrie

class ManualFrequencyEditor:
    def __init__(self):
        self.trie = PrefixTrie()
    
    def edit_frequency(self, word, new_freq):
        """
        Edits the frequency of a word in the trie if it exists.
        """
        if not word:
            print("Word cannot be empty.")
            return False

        word = word.lower().strip()
        node = self.trie.root

        for char in word:
            if char not in node.children:
                print(f"'{word}' not found in trie.")
                return False
            node = node.children[char]

        if node.is_terminal:
            old_freq = node.frequency
            node.frequency = new_freq
            print(f"Frequency for '{word}' updated from {old_freq} to {new_freq}.")
            return True
        else:
            print(f"'{word}' is a prefix, not a complete word.")
            return False

    def manual_freq_menu(self):
        """
        Display the menu for manual frequency editing.
        """
        print("\nManual Frequency Editor Menu:")
        print("1. Edit Word Frequency")
        print("2. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            word = input("Enter the word to edit frequency: ")
            new_freq = input("Enter the new frequency: ")
            try:
                new_freq = int(new_freq)
                if self.edit_frequency(word, new_freq):
                    print(f"Frequency for '{word}' successfully updated.")
            except ValueError:
                print("Invalid frequency value. Please enter a number.")
        elif choice == '2':
            return
        else:
            print("Invalid choice. Please try again.")