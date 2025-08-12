import matplotlib.pyplot as plt
import networkx as nx
import re

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, syllables, word_id):
        node = self.root
        for i, syll in enumerate(syllables):
            if syll not in node.children:
                node.children[syll] = TrieNode()
            node = node.children[syll]
        node.is_end = True
        node.frequency += 1

    def get_edges(self):
        edges = []
        queue = [(self.root, "ROOT")]
        label_map = {"ROOT": self.root}
        id_counter = 1

        while queue:
            current_node, current_label = queue.pop(0)
            for syll, child in current_node.children.items():
                if current_label == "ROOT":
                    child_label = f"root{id_counter}_{syll}"
                else:
                    child_label = f"{current_label}_{syll}"

                edges.append((current_label, child_label, syll))
                label_map[child_label] = child
                queue.append((child, child_label))
                id_counter += 1

        return edges

    def visualize(self):
        edges = self.get_edges()
        G = nx.DiGraph()
        labels = {}
        for parent, child, syll in edges:
            G.add_edge(parent, child)
            labels[(parent, child)] = syll

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(12, 8))
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color='lightyellow',
            edge_color='gray',
            node_size=1200,  # Reduced node size
            font_size=8
        )
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='green')
        plt.title("Syllable-Based Trie Visualization")
        plt.tight_layout()
        plt.show()

def split_into_syllables(word):
    # Very simple syllable regex - still crude
    syllables = re.findall(r'[^aeiou]*[aeiou]+(?:[^aeiou]*$|[^aeiou](?=[^aeiou]))?', word, re.IGNORECASE)
    return [s.lower() for s in syllables if s]

def integrate_trie_visualizer():
    """Mini menu for syllable trie visualizer with text/file input options."""
    while True:
        print("\n" + "="*50)
        print("SYLLABLE TRIE VISUALIZER")
        print("="*50)
        print("1. Visualize text from input")
        print("2. Visualize text from file")
        print("3. Back to main menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            paragraph = input("\nEnter a sentence or paragraph to visualize as a syllable-based trie: ").strip()
            if not paragraph:
                print("No input provided. Try again.")
                continue
            
        elif choice == '2':
            filename = input("Enter filename to read from: ").strip()
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    paragraph = file.read()
                if not paragraph.strip():
                    print(f"File '{filename}' is empty. Try again.")
                    continue
                print(f"Read content from file '{filename}'.")
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found. Try again.")
                continue
            except Exception as e:
                print(f"Error reading file: {e}. Try again.")
                continue
            
        elif choice == '3':
            print("Returning to main menu.")
            break
        
        else:
            print("Invalid choice, please enter 1, 2 or 3.")
            continue
        
        # Process the paragraph text (from input or file)
        words = [word.strip(".,!?;:()[]{}\"'").lower() for word in paragraph.split()]
        trie = Trie()
        for i, word in enumerate(words):
            syllables = split_into_syllables(word)
            if syllables:
                trie.insert(syllables, i + 1)
        
        print(f"\nWords inserted as syllables: {[split_into_syllables(word) for word in words]}")
        trie.visualize()
