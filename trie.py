# trie.py
# Prefix Trie Implementation for ST1507 CA2
# Shu Zhi and Ashley
# DAAA/2A/03

import re
from collections import defaultdict

class TrieNode:
    """
    Node class for the prefix trie data structure.
    Each node represents a character and can be marked as terminal (end of word).
    """
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_terminal = False  # Marks if this node represents end of a word
        self.frequency = 0  # Frequency of the word ending at this node
        self.word = ""  # The complete word ending at this node
        
    def __str__(self):
        return f"Node(terminal={self.is_terminal}, freq={self.frequency}, word='{self.word}')"

class PrefixTrie:
    """
    Prefix Trie implementation for storing and searching words efficiently.
    Supports adding, deleting, searching, and pattern matching with wildcards.
    """
    def __init__(self):
        self.root = TrieNode()
        self.size = 0  # Number of words in the trie
        
    def add_keyword(self, word, frequency=1):
        """
        Add a word to the trie with given frequency.
        If word already exists, increment its frequency.
        Time Complexity: O(m) where m is the length of the word
        """
        if not word:
            return
            
        word = word.lower().strip()
        node = self.root
        
        # Traverse/create nodes for each character
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            
        # Mark the end of word and update frequency
        if not node.is_terminal:
            self.size += 1
            node.is_terminal = True
            node.word = word
            node.frequency = frequency
        else:
            node.frequency += frequency
            
    def search_keyword(self, word):
        """
        Search for a word in the trie.
        Returns True if word exists, False otherwise.
        Time Complexity: O(m) where m is the length of the word
        """
        if not word:
            return False
            
        word = word.lower().strip()
        node = self.root
        
        # Traverse the trie following the word
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
            
        return node.is_terminal
        
    def delete_keyword(self, word):
        """
        Delete a word from the trie.
        Returns True if word was deleted, False if word doesn't exist.
        Time Complexity: O(m) where m is the length of the word
        """
        if not word:
            return False

        word = word.lower().strip()

        def _delete_recursive(node, word, index):
            if index == len(word):
                if not node.is_terminal:
                    return False, False  # word doesn't exist

                # Unmark this node as a terminal
                node.is_terminal = False
                node.frequency = 0
                node.word = ""
                self.size -= 1

                # deleted = True, should_delete_node = (no children)
                return True, len(node.children) == 0

            char = word[index]
            if char not in node.children:
                return False, False  # word doesn't exist

            deleted, should_delete_child = _delete_recursive(node.children[char], word, index + 1)

            if should_delete_child:
                del node.children[char]

            # deleted remains True if we actually removed the word somewhere down the chain
            return deleted, not node.is_terminal and len(node.children) == 0

        deleted, _ = _delete_recursive(self.root, word, 0)
        return deleted
        
    def find_all_matches_with_freq(self, pattern):
        if not pattern:
            return []

        pattern = pattern.lower().strip()
        matches = []

        def _find_matches(node, pattern_index, current_word):
            if pattern_index == len(pattern):
                if node.is_terminal:
                    matches.append((node.word, node.frequency))
                return

            char = pattern[pattern_index]

            if char == '*':
                for child_char, child_node in node.children.items():
                    _find_matches(child_node, pattern_index + 1, current_word + child_char)
            else:
                if char in node.children:
                    _find_matches(node.children[char], pattern_index + 1, current_word + char)

        _find_matches(self.root, 0, "")

        # Sort by frequency (descending), then alphabetically
        matches.sort(key=lambda x: (-x[1], x[0]))
        return matches

        
    def find_best_match(self, pattern):
        """
        Find the best matching word for a pattern with wildcards (*).
        Returns the word with highest frequency, or None if no match.
        Time Complexity: O(n) where n is the number of nodes in the trie
        """
        matches = self.find_all_matches_with_freq(pattern)
        if matches:
            # Return only the word (first element of the tuple), not the frequency
            return matches[0][0]
        return None
        
    def get_all_words(self):
        """
        Get all words in the trie with their frequencies.
        Returns a list of tuples (word, frequency) sorted by frequency.
        Time Complexity: O(n) where n is the number of nodes in the trie
        """
        words = []
        
        def _collect_words(node, current_word):
            if node.is_terminal:
                words.append((node.word, node.frequency))
                
            for char, child_node in node.children.items():
                _collect_words(child_node, current_word + char)
                
        _collect_words(self.root, "")
        
        # Sort by frequency (descending) then alphabetically
        words.sort(key=lambda x: (-x[1], x[0]))
        return words
        
    def display_trie(self):
        """
        Display the trie structure in a readable format.
        Shows the hierarchical structure with terminal nodes marked.
        """
        if self.size == 0:
            print("[]")
            return
            
        def _display_node(node, prefix="", is_last=True):
            if node.is_terminal:
                print(f"{prefix}{'└── ' if is_last else '├── '}{node.word}* ({node.frequency})")
            
            children = list(node.children.items())
            for i, (char, child_node) in enumerate(children):
                is_last_child = i == len(children) - 1
                next_prefix = prefix + ("    " if is_last else "│   ")
                
                if child_node.is_terminal:
                    _display_node(child_node, next_prefix, is_last_child)
                else:
                    print(f"{next_prefix}{'└── ' if is_last_child else '├── '}{char}")
                    _display_node(child_node, next_prefix + ("    " if is_last_child else "│   "), True)
                    
        print("Trie Structure:")
        _display_node(self.root)
        print(f"\nTotal words: {self.size}")
        
    def read_keywords_from_file(self, filename):
        """
        Read keywords from a file and build the trie.
        File format: word,frequency (one per line)
        Clears existing trie before loading new data.
        """
        try:
            self.root = TrieNode()
            self.size = 0
            
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        if ',' in line:
                            parts = line.split(',')
                            word = parts[0].strip()
                            frequency = int(parts[1].strip()) if len(parts) > 1 else 1
                        else:
                            word = line
                            frequency = 1
                            
                        if word:
                            self.add_keyword(word, frequency)
                            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error reading file: {e}")
            
    def write_keywords_to_file(self, filename):
        """
        Write all keywords and their frequencies to a file.
        File format: word,frequency (one per line)
        """
        try:
            words = self.get_all_words()
            with open(filename, 'w', encoding='utf-8') as file:
                for word, frequency in words:
                    file.write(f"{word},{frequency}\n")
                    
        except Exception as e:
            print(f"Error writing file: {e}")
            
    def write_trie_to_file(self, filename):
        """
        Write the trie structure to a file in a readable format.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                if self.size == 0:
                    file.write("[]\n")
                    return
                    
                def _write_node(node, prefix="", is_last=True):
                    if node.is_terminal:
                        file.write(f"{prefix}{'└── ' if is_last else '├── '}{node.word}* ({node.frequency})\n")
                    
                    children = list(node.children.items())
                    for i, (char, child_node) in enumerate(children):
                        is_last_child = i == len(children) - 1
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        
                        if child_node.is_terminal:
                            _write_node(child_node, next_prefix, is_last_child)
                        else:
                            file.write(f"{next_prefix}{'└── ' if is_last_child else '├── '}{char}\n")
                            _write_node(child_node, next_prefix + ("    " if is_last_child else "│   "), True)
                            
                file.write("Trie Structure:\n")
                _write_node(self.root)
                file.write(f"\nTotal words: {self.size}\n")
                
        except Exception as e:
            print(f"Error writing trie to file: {e}")
    
    
            
    def __len__(self):
        """Return the number of words in the trie."""
        return self.size
        
    def __str__(self):
        """String representation of the trie."""
        return f"PrefixTrie(size={self.size})"
        
    def __repr__(self):
        """Detailed string representation of the trie."""
        return f"PrefixTrie(size={self.size}, words={[word for word, _ in self.get_all_words()[:10]]}{'...' if self.size > 10 else ''})"