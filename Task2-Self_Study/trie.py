try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Note: graphviz not installed. Visualization features will be unavailable.")


class TrieNode:
    """The node for the Trie data structure."""
    def __init__(self):
        self.children : dict[str, TrieNode] = {} # Dict: character -> TrieNode
        self.is_end : bool = False # marks if a complete word ends here

class Trie:
    def __init__(self):
        self.root = TrieNode() #set the root

    #INSERT
    def insert(self, word: str) -> None:
        """Insert a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  # create node if missing
            node = node.children[char]
        node.is_end = True # mark end of word

    # SEARCH
    def search(self, word: str) -> bool:
        """Return True if the exact word exists in the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False          # word not found
            node = node.children[char]
        if node.is_end:
            return True   # word found
        return False    # True only if word fully ends here


    #  DELETE - This only marks the end of word as False instead of removing the nodes.
    def delete(self, word: str) -> bool:
        """Delete a word from the Trie. 
        Returns True if deletion succeeded."""
        # Check if word exists first
        if not self.search(word):
            return False
        
        # Find the node where the word ends
        node = self.root
        for char in word:
            node = node.children[char]
        
        # Mark the end of word as False
        node.is_end = False
        
        return True

    # PREFIX SEARCH (similar to SEARCH but no need to check is_end)
    def starts_with(self, prefix: str) -> bool:
        """Return True if any stored word begins with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True                   # prefix path exists

    # VISUALIZATION
    def visualize(self, filename="trie"):
        """
        Visualize the Trie.
        Returns the Digraph object or None if graphviz is not available.
        """
        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz is not available.")
            return None
        
        dot = graphviz.Digraph(comment='Trie Structure')
        dot.attr(rankdir='TB')  # Top to Bottom https://graphviz.org/docs/attrs/rankdir/
        dot.attr('node', shape='circle')
        
        # Add nodes and edges recursively
        self._add_nodes_to_graph(self.root, dot, node_id='root', parent_id=None)
        
        # Render and view the graph
        try:
            output_path = dot.render(filename, format='png', cleanup=True)
            print(f"File saved to: {output_path}.png")
            return dot
        except Exception as e:
            print(f"Error rendering graph: {e}")
            return None
    
    def _add_nodes_to_graph(self, node, dot, node_id, parent_id=None, char_label=''):
        """Add nodes and edges recursively"""
        if node_id == 'root':
            label = 'root'
        else:
            label = char_label
        
        # Add styling for end-of-word nodes
        if node.is_end:
            dot.node(node_id, label=label, shape='doublecircle', style='filled', fillcolor='lightblue')
        else:
            dot.node(node_id, label=label)
        
        # Add edge from parent
        if parent_id is not None:
            dot.edge(parent_id, node_id)
        
        # add children
        for char, child in sorted(node.children.items()):
            child_id = f"{node_id}_{char}"
            self._add_nodes_to_graph(child, dot, node_id=child_id, parent_id=node_id, char_label=char)



