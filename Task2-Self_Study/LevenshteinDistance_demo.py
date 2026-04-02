import LevenshteinDistance

levenshtein_distance = LevenshteinDistance.levenshtein_distance
visualize_dp_matrix = LevenshteinDistance.visualize_dp_matrix

def test_levenshtein_distance(source_str: str, target_str: str) -> None:
    """Test the levenshtein_distance function."""
    print(f"\nTesting Levenshtein Distance between '{source_str}' and '{target_str}':")
    distance = levenshtein_distance(source_str, target_str)
    print(f"Computed Distance: {distance}")
    

if __name__ == "__main__":
    print("Levenshtein Distance Demo")
    print("Test Cases 1:")
    test_levenshtein_distance("metric", "metro")
    visualize_dp_matrix("metric", "metro")

    print("\nTest Cases 2:")
    test_levenshtein_distance("hello", "world")
    visualize_dp_matrix("hello", "world")

    print("\nTest Cases 3:")
    test_levenshtein_distance("final", "answer")
    visualize_dp_matrix("final", "answer")