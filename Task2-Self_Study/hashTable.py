import math

class HashTable:
    def __init__(self, size):
        self.size  = size
        self.table = [[] for _ in range(self.size)]

    def hash1(self, key):
        return key % self.size

    def hash2(self, key):
        num = (math.sqrt(5) - 1) / 2
        return math.floor(self.size * ((key * num) % 1))

    def set(self, key, value):
        index = self.hash2(key)
        self.table[index].append({"key": key, "value": value})

    def get(self, key):
        index = self.hash2(key)
        for item in self.table[index]:
            if item["key"] == key:  
                return item["value"]
        return None

    def print_all(self):
        for bucket in self.table:
            print(f"{bucket}")


my_hash_table = HashTable(6)
my_hash_table.set(123123,  "Peter")
my_hash_table.set(11455,  "Tom")
my_hash_table.set(1855,  "Smith")
my_hash_table.set(23434,  "Katrina")
my_hash_table.set(1245, "Wilson")

print(f"(GET value {my_hash_table.get(11455)})")
my_hash_table.print_all()
