import trie

if __name__ == "__main__":
    trie1 = trie.Trie()

    # Insert
    print("="*30)
    print("Inserting words:")
    words = ["met", "metro", "metric", "metropolitan"] #Words to insert
    for word in words:
        trie1.insert(word)
        print(f"Inserted: {word}")
    print("Insertion complete.\n")

    # Search
    print("="*30)
    print("Searching for words:")
    print(f"trie1.search('metro'): {trie1.search('metro')}")        # True
    print(f"trie1.search('metrop'): {trie1.search('metrop')}")       # False

    # Prefix search
    print("="*30)
    print("Prefix search:")
    print(f"trie1.starts_with('metr'): {trie1.starts_with('metr')}")    # True
    print(f"trie1.starts_with('xyz'): {trie1.starts_with('xyz')}")     # False

    # Delete
    print("="*30)
    print(f"Deleting word: metro {trie1.delete('metro')}")  # True
    
    print(f"trie1.search('metro'): {trie1.search('metro')}")        # False
    print(f"trie1.search('metropolitan'): {trie1.search('metropolitan')}") # True
