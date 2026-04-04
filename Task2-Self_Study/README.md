**Task 2 Self-study on a new data structure AND a new algorithm which are NOT covered in the course**

# Content

**5-minute introduction video** [https://youtu.be/WElNAKMI-bM](https://youtu.be/WElNAKMI-bM)


## Section 1 - Data Structure - Trie


### Introduction
A **Trie** is a tree-based data structure built specifically for string storage and retrieval. It gets its name from the word "retrieval", first introduced by Edward Fredkin in 1960. Rather than storing complete strings at each node, a Trie breaks every word down character by character, where each node represents a single letter and the path from the root to any node spells out a prefix or a complete word.

### Structure
- **TrieNode**: Each node contains:
  - `children`: A dictionary mapping characters to child TrieNodes
  - `is_end`: A boolean flag indicating if the node marks the end of a complete word
- **Trie**: The main structure with a root node and operations

### Features
- **Insert**: Add words to the trie
- **Search**: Check if a word exists in the trie
- **Prefix Search**: Check if any word starts with a given prefix
- **Delete**: Remove a word from the trie [Only remove the flag of end of word]
- **Visualize**: Generate a graphical representation of the trie using Graphviz [only available if graphviz is installed]

### How to Use

#### Prerequisites
```
pip install graphviz
```
Note: You may need to install Graphviz system package from https://graphviz.org/download/

#### Basic Usage

```python
from trie import Trie #import

# Create a new Trie
trie = Trie()

# Insert words
trie.insert("metro")
trie.insert("metropolitan")

# Search for words
print(trie.search("metro"))      # True
print(trie.search("metrop"))     # False

# Check prefix
print(trie.starts_with("metr"))  # True
print(trie.starts_with("xyz"))   # False

# Delete a word
trie.delete("metro")
print(trie.search("metro"))      # False

# Visualize the trie
trie.visualize()  # Saves as trie.png
```

### Test Cases

#### Test 1: Basic Operations
File: `trie_test1.py`


#### Test 2: Visualization
File: `trie_test2.py`

### Visualization Output
The `visualize()` method generates a PNG file showing:
- **Label**: Labeled as "root" or a single character
- **End-of-word nodes**: Double circle with light blue fill
- **Edges**: Show the path from root to each character

Example visualization shows the shared prefixes and branching structure of the trie.

![Trie Visualization](https://github.com/wltam/COMP8090SEF-Project/raw/main/Task2-Self_Study/trie.png)


## Section 2 - Algorithm - Levenshtein Distance

### Introduction
**Levenshtein Distance** measures how different two strings are. Specifically, it counts the minimum number of single-character edits required to transform one string into another, where an "edit" means one of three operations: insertion, deletion, or substitution. The concept was introduced by Soviet mathematician Vladimir Levenshtein in 1965, originally developed for error correction in binary codes.

### Allowed Operations
The algorithm considers three types of edits:
1. **Insertion**: Add a character
2. **Deletion**: Remove a character
3. **Substitution**: Replace one character with another

Each operation has a cost of 1. The Levenshtein Distance is the minimum total cost to transform the source string into the target string.

### Features
- **Standard Implementation**: Full DP matrix for educational understanding
- **Visualization**: Prints the complete DP matrix for tracing the algorithm

### How to Use

#### Basic Usage

```python
from LevenshteinDistance import levenshtein_distance, visualize_dp_matrix

# Calculate distance between two strings
distance = LevenshteinDistance.levenshtein_distance("metro", "metric")
print(f"Distance: {distance}")  # Output: 2

# Visualize the DP matrix
LevenshteinDistance.visualize_dp_matrix("metro", "metric")
```

### Test Cases

File: `LevenshteinDistance_demo.py`

- Calculate distances between various string pairs



