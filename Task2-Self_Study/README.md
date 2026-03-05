**Task 2 Self-study on a new data structure AND a new algorithm which are NOT covered in the course**

# Content

## Section 1 - Data Structure - Hash
### Purpose for Hash Table
A hash table is mainly used to store data in a way that lets you find, add, or remove items very quickly using a unique key. Instead of searching through a list one-by-one, it uses a hash function to convert the key into an index, which makes lookups, insertions, and deletions typically run in about O(1) average time. 

Because of this, hash tables are widely used for tasks like mapping IDs to records, quickly checking whether something exists (like detecting duplicates), counting frequencies (such as word counts), and implementing caches to reuse previously computed results efficiently.

### Common use case

1. **Storing user passwords**

For example, if Peter has the login password **12345** on website A, the password stored in the backend database is usually **hashed**, rather than saving the plain text **12345** directly. Therefore, even if a hacker breaks into the database, they still cannot infer what the original password was, which helps ensure data security. 

2. **File verification**

If we open the terminal and type `md5` filename, we will see that it generates a hash value. This can be used to verify whether two files are identical.
### Characteristic

1. **Fixed-length output**: No matter how long the original input is, the value produced by a hash algorithm is always a fixed length.
2. **One-way (irreversible)**: Data that has been hashed cannot be reversed to recover the original input.
3. **Avalanche effect**: Even if two inputs differ by only one word or one character, the resulting hash values will be vastly different.

## Section 2 - Algorithm - A* Algorithm

### Purpose for A* Algorithm
A* (A-star) is a pathfinding algorithm used to find the shortest or most efficient route between two points. 

### Common use case
It is widely used in applications such as GPS navigation, game AI, and robotics because it is both fast and accurate. Unlike simpler search algorithms that blindly explore all directions, A* uses a heuristic function to estimate the distance to the goal, allowing it to prioritize more promising paths and avoid wasting time on dead ends. This makes it one of the most popular and practical algorithms in computer science whenever an optimal path needs to be found efficiently.