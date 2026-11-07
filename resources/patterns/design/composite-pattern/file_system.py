"""Composite Pattern: file-system example.

File and Folder share the FileSystemComponent interface, so get_size()
and display() work on either without the caller checking types.

Run: python file_system.py
"""
from abc import ABC, abstractmethod


class FileSystemComponent(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0):
        pass


class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size

    def display(self, indent: int = 0):
        print("  " * indent + f"File {self.name} ({self.size} bytes)")


class Folder(FileSystemComponent):
    def __init__(self, name: str):
        self.name = name
        self.children: list[FileSystemComponent] = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def display(self, indent: int = 0):
        print("  " * indent + f"Folder {self.name}")
        for child in self.children:
            child.display(indent + 1)


if __name__ == "__main__":
    root = Folder("root")
    root.add(File("readme.txt", 100))

    src = Folder("src")
    src.add(File("main.py", 500))
    src.add(File("utils.py", 300))
    root.add(src)

    root.display()
    print(f"Total size: {root.get_size()} bytes")
