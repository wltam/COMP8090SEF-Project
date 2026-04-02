import trie

if __name__ == "__main__":
    trie1 = trie.Trie()

    # Insert
    print("="*30)
    print("Inserting words:")
    words = ["bit", "bite", "binary", "bool", "boolean",
         "data", "debug", "delete", "deletion"] #Words to insert
    
    # Visualize the Trie
    print("="*30)
    print("Generating Trie visualization...")
    trie1.visualize()