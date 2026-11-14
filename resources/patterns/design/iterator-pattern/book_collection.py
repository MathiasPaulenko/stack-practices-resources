"""Iterator pattern — Python.

A BookCollection that speaks Python's iterator protocol via __iter__,
plus a reverse traversal helper. Run: python book_collection.py
"""


class BookCollection:
    def __init__(self):
        self._books = []

    def add(self, book: str):
        self._books.append(book)

    def __iter__(self):
        return iter(self._books)

    def reverse_iter(self):
        return reversed(self._books)


def main():
    collection = BookCollection()
    collection.add("Design Patterns")
    collection.add("Clean Code")
    collection.add("Refactoring")

    print("Forward:")
    for book in collection:
        print(f"  {book}")

    print("Reverse:")
    for book in collection.reverse_iter():
        print(f"  {book}")


if __name__ == "__main__":
    main()
