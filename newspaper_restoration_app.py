# newspaper_restoration_app.py
# ST1507 CA2 - Newspaper Restoration App
# Shu Zhi and Ashley
# DAAA/2A/03


from trie import PrefixTrie
from text_processor import TextProcessor
import os

class NewspaperRestorationApp:
    def __init__(self):
        self.trie = PrefixTrie()
        self.text_processor = TextProcessor()
        
    def display_main_menu(self):
        print("\n" + "*"*65)
        print("* ST1507 DSAA: Predictive Text Editor (using tries)             *")
        print("*"+"-"*63 + "*")
        print("*" + " "*63 + "*")
        print("*  - Done by: Yang Shu Zhi (2435356) & Ashley Yong (2435781)    *")
        print("*  - Class: DAAA/2A/03                                          *")
        print("*" + " "*63 + "*")
        print("*"*65)
        print("\n\n")
        print("Please select your choice ('1','2','3','4','5','6','7'):")
        print("    1. Construct/Edit Trie")
        print("    2. Predict/Restore Text")
        print("    "+"-"*52)
        print("    3. Extra Feature One (Yang Shu Zhi)")
        print("    4. Extra Feature Two (Yang Shu Zhi)")
        print("    "+"-"*52)
        print("    5. Extra Feature Three (Ashley Yong Lok Xi)")
        print("    6. Extra Feature Four (Ashley Yong Lok Xi)")
        print("    "+"-"*52)
        print("    7. Exit")
        
    def construct_edit_trie_menu(self):
        print("\n" + "-"*60)
        print("Construct/Edit Trie Commands:")
        print("    '+','-','?','#','@','~','=','!','\\'")
        print("-"*60)
        print("    +sunshine       (add a keyword)")
        print("    -moonlight      (delete a keyword)")
        print("    ?rainbow        (find a keyword)")
        print("    #               (display Trie)")
        print("    @               (write Trie to file)")
        print("    ~               (read keywords from file to make Trie)")
        print("    =               (write keywords from Trie to file)")
        print("    !               (print instructions)")
        print("    \\               (exit)")
        print("-"*60+"\n")
        
        while True:
            try:
                user_input = input(">").strip()
                
                # split user input into command [0] and keyword [1:] ONLY IF keyword is inputted
                command=user_input[0] 
                keyword=user_input[1:].strip().lower() if len(user_input) > 1 else None
                
                if command == "+":
                    keyword=keyword or input("Enter keyword to add: ").strip().lower()
                    if keyword:
                        self.trie.add_keyword(keyword)
                        print(f"Keyword '{keyword}' added to trie.")
                    else:
                        print("Invalid keyword.")
                        
                elif command == '-':
                    keyword =keyword or input("Enter keyword to delete: ").strip().lower()
                    if keyword:
                        if self.trie.delete_keyword(keyword):
                            print(f"Keyword '{keyword}' deleted from trie.")
                        else:
                            print(f"Warning: Keyword '{keyword}' not found in trie.")
                    else:
                        print("Invalid keyword.")
                        
                elif command == '?':
                    keyword = keyword or input("Enter keyword to search: ").strip().lower()
                    if keyword:
                        if self.trie.search_keyword(keyword):
                            print(f"Keyword '{keyword}' found in trie.")
                        else:
                            print(f"Keyword '{keyword}' not found in trie.")
                    else:
                        print("Invalid keyword.")
                        
                elif command == '#':
                    print("\nCurrent Trie:")
                    self.trie.display_trie()
                    
                elif command == '@':
                    filename = input("Enter filename to write trie: ").strip()
                    if filename:
                        self.trie.write_trie_to_file(filename)
                        print(f"Trie written to file '{filename}'.")
                    else:
                        print("Invalid filename.")
                        
                elif command == '~':
                    filename = input("Enter filename to read keywords: ").strip()
                    if filename and os.path.exists(filename):
                        self.trie.read_keywords_from_file(filename)
                        print(f"Keywords loaded from file '{filename}'.")
                    else:
                        print("File not found or invalid filename.")
                        
                elif command == '=':
                    filename = input("Enter filename to write keywords: ").strip()
                    if filename:
                        self.trie.write_keywords_to_file(filename)
                        print(f"Keywords written to file '{filename}'.")
                    else:
                        print("Invalid filename.")
                        
                elif command == '!':
                    self.construct_edit_trie_menu()
                    
                elif command == '\\':
                    print("Exiting Construct/Edit Trie Command Prompt.")
                    break
                    
                else:
                    print("Invalid command. Use '!' to see available commands.")
                    
            except KeyboardInterrupt:
                print("\nExiting Construct/Edit Trie Command Prompt.")
                break
            except Exception as e:
                print(f"Error: {e}")
                
    def predict_restore_text_menu(self):
        print("-" * 63)
        print("\nPredict/Restore Text Commands:")
        print("'~', '#', '$', '&', '@', '!', '\'")
        print("-" * 63)
        print("~ : Read keywords from a file to make a new prefix trie")
        print("# : Display the current prefix trie on the screen")
        print("$ : List all possible matching keywords")
        print("? : Restore a word using the best keyword match")
        print("& : Restore a text using all matching keywords")
        print("@ : Restore a text using the best keyword matches")
        print("! : Print instructions for various commands")
        print("\\ : Exit and return to main menu")
        
        while True:
            try:
                command = input("\nEnter command: ").strip()
                
                if command == '~':
                    filename = input("Enter filename to read keywords: ").strip()
                    if filename and os.path.exists(filename):
                        self.trie.read_keywords_from_file(filename)
                        print(f"Keywords loaded from file '{filename}'.")
                    else:
                        print("File not found or invalid filename.")
                        
                elif command == '#':
                    print("\nCurrent Trie:")
                    self.trie.display_trie()
                    
                elif command == '$':
                    pattern = input("Enter pattern with wildcards (*): ").strip().lower()
                    if pattern:
                        matches = self.trie.find_all_matches(pattern)
                        if matches:
                            print(f"Matching keywords: {matches}")
                        else:
                            print("No matches found.")
                    else:
                        print("Invalid pattern.")
                        
                elif command == '?':
                    pattern = input("Enter pattern with wildcards (*): ").strip().lower()
                    if pattern:
                        best_match = self.trie.find_best_match(pattern)
                        if best_match:
                            print(f"Best match: {best_match}")
                        else:
                            print("No match found.")
                    else:
                        print("Invalid pattern.")
                        
                elif command == '&':
                    filename = input("Enter filename to restore (with all matches): ").strip()
                    if filename and os.path.exists(filename):
                        output_file = input("Enter output filename: ").strip()
                        if output_file:
                            self.text_processor.restore_text_all_matches(filename, output_file, self.trie)
                            print(f"Text restored with all matches and saved to '{output_file}'.")
                        else:
                            print("Invalid output filename.")
                    else:
                        print("File not found or invalid filename.")
                        
                elif command == '@':
                    filename = input("Enter filename to restore (with best matches): ").strip()
                    if filename and os.path.exists(filename):
                        output_file = input("Enter output filename: ").strip()
                        if output_file:
                            self.text_processor.restore_text_best_matches(filename, output_file, self.trie)
                            print(f"Text restored with best matches and saved to '{output_file}'.")
                        else:
                            print("Invalid output filename.")
                    else:
                        print("File not found or invalid filename.")
                        
                elif command == '!':
                    self.predict_restore_text_menu()
                    
                elif command == '\\':
                    print("Exiting Predict/Restore Text Command Prompt.")
                    break
                    
                else:
                    print("Invalid command. Use '!' to see available commands.")
                    
            except KeyboardInterrupt:
                print("\nExiting Predict/Restore Text Command Prompt.")
                break
            except Exception as e:
                print(f"Error: {e}")
                
    def run(self):
        while True:
            try:
                self.display_main_menu()
                choice = input("Enter choice: ").strip()
                
                if choice == '1':
                    self.construct_edit_trie_menu()
                elif choice == '2':
                    self.predict_restore_text_menu()
                elif choice == '3':
                    print("Additional Feature 1 - Not implemented yet")
                elif choice == '4':
                    print("Additional Feature 2 - Not implemented yet")
                elif choice == '5':
                    print("Additional Feature 3 - Not implemented yet")
                elif choice == '6':
                    print("Additional Feature 4 - Not implemented yet")
                elif choice == '7':
                    print("Thank you for using the Newspaper Restoration Application!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")
                    
            except KeyboardInterrupt:
                print("\nThank you for using the Newspaper Restoration Application!")
                break
            except Exception as e:
                print(f"Error: {e}")