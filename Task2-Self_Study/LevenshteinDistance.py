def levenshtein_distance(source_str: str, target_str: str) -> int:
    """
    Compute the Levenshtein Distance between two strings.
    Args:
        source_str: Source string
        target_str: Target string
    Returns:
        Min edit distance (int)
    """
    m : int = len(source_str)
    n : int = len(target_str)

    # Create a (m+1) x (n+1) matrix - Step 1 in Worked Example
    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming to/from empty string - Step 2 to 4 in Worked Example
    for i in range(m + 1):
        dp[i][0] = i  # Delete all chars from source_str
    for j in range(n + 1):
        dp[0][j] = j  # Insert all chars from target_str

    # Fill in the DP table - Step 5 to 8 in Worked Example
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source_str[i - 1] == target_str[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Deletion
                    dp[i][j - 1],      # Insertion
                    dp[i - 1][j - 1]   # Substitution
                )

    return dp[m][n]

def visualize_dp_matrix(source_str: str, target_str: str) -> None:
    """
    Visualize the full DP matrix.
    """
    m : int = len(source_str)
    n : int = len(target_str)

    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)] # dp matrix e.g. [[0,1,2,3], [1,0,1,2], [2,1,0,1], [3,2,1,0]]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source_str[i - 1] == target_str[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    col_width = 4
    # Print header
    print(f"\nLevenshtein Distance DP Matrix between '{source_str}' and '{target_str}':")
    print("=" * ((n+2) * col_width + 4))
    
    # Print top row (target_str characters) - align with columns
    header = " " * col_width + " ".join(f"{c:^{col_width}}" for c in [" "] + list(target_str)) + "< Target String" # width is {col_width} for spacing with ^ centered
    
    print(header)
    
    # Print each row with proper alignment
    for i, row in enumerate(dp): # row e.g. [0,1,2,3]
        if i == 0:
            label = " " * col_width  # Empty label for first row
        else:
            label = f"{source_str[i-1]:^{col_width}}"  # Character label
        row_values = " ".join(f"{v:^{col_width}}" for v in row) 
        print(f"{label}{row_values}")
    
    print(" ^ Source String")
    print("=" * ((n+2) * col_width + 4))
    print(f"Levenshtein Distance: {dp[m][n]}")

