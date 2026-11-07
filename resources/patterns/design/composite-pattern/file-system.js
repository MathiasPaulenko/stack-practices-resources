// Composite Pattern: file-system example.
// File and Folder share the FileSystemComponent contract, so getSize()
// works on either without the caller checking types.
// Run: node file-system.js

class FileSystemComponent {
  getSize() { throw new Error("Not implemented"); }
  display(indent = 0) { throw new Error("Not implemented"); }
}

class File extends FileSystemComponent {
  constructor(name, size) {
    super();
    this.name = name;
    this.size = size;
  }

  getSize() { return this.size; }

  display(indent = 0) {
    console.log("  ".repeat(indent) + `File ${this.name} (${this.size} bytes)`);
  }
}

class Folder extends FileSystemComponent {
  constructor(name) {
    super();
    this.name = name;
    this.children = [];
  }

  add(component) { this.children.push(component); }

  getSize() {
    return this.children.reduce((sum, c) => sum + c.getSize(), 0);
  }

  display(indent = 0) {
    console.log("  ".repeat(indent) + `Folder ${this.name}`);
    this.children.forEach(c => c.display(indent + 1));
  }
}

const root = new Folder("root");
root.add(new File("readme.txt", 100));

const src = new Folder("src");
src.add(new File("main.js", 500));
src.add(new File("utils.js", 300));
root.add(src);

root.display();
console.log(`Total size: ${root.getSize()} bytes`);
