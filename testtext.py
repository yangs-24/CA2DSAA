import re

def test_wildcard_detection():
    # Your actual text snippet
    text = """brought smiles o* the faces of the panel o* five judges, as well as brought *er the
final victory. Wel* done, Mary!"""
    
    print("Original text:")
    print(text)
    print("\n" + "="*50)
    
    # Try different patterns
    patterns = [
        r'\b\w*\*+\w*\b',  # Original
        r'\b[\w*]*\*[\w*]*\b',  # Your current
        r'\b\w*\*\w*\b|\b\*\w+\b|\b\w+\*\b',  # Alternative 1
        r'\b[a-zA-Z*]+\*[a-zA-Z*]*\b|\b\*[a-zA-Z]+\b',  # Alternative 2
        r'[a-zA-Z]*\*[a-zA-Z]*',  # Simple approach
    ]
    
    for i, pattern in enumerate(patterns, 1):
        matches = re.findall(pattern, text)
        print(f"Pattern {i}: {pattern}")
        print(f"Matches: {matches}")
        print()

# Run the test
test_wildcard_detection()

# Also test individual problem words
problem_words = ['o*', '*er', 'Wel*']
print("Testing individual problem words:")
print("="*40)

for word in problem_words:
    print(f"Testing '{word}':")
    for i, pattern in enumerate([r'\b\w*\*+\w*\b', r'[a-zA-Z]*\*[a-zA-Z]*'], 1):
        match = re.search(pattern, f" {word} ")  # Add spaces for word boundaries
        print(f"  Pattern {i}: {'MATCH' if match else 'NO MATCH'}")
    print()