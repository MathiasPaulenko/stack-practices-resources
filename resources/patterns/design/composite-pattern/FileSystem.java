// Composite Pattern: file-system example.
// Compile: javac FileSystem.java && java FileSystem
public class FileSystem {

    public interface FileSystemComponent {
        int getSize();
        void display(int indent);
    }

    public static class File implements FileSystemComponent {
        private final String name;
        private final int size;

        public File(String name, int size) {
            this.name = name;
            this.size = size;
        }

        public int getSize() { return size; }

        public void display(int indent) {
            System.out.println("  ".repeat(indent) + "File " + name + " (" + size + " bytes)");
        }
    }

    public static class Folder implements FileSystemComponent {
        private final String name;
        private final java.util.List<FileSystemComponent> children = new java.util.ArrayList<>();

        public Folder(String name) {
            this.name = name;
        }

        public void add(FileSystemComponent component) {
            children.add(component);
        }

        public int getSize() {
            return children.stream().mapToInt(FileSystemComponent::getSize).sum();
        }

        public void display(int indent) {
            System.out.println("  ".repeat(indent) + "Folder " + name);
            for (FileSystemComponent child : children) {
                child.display(indent + 1);
            }
        }
    }

    public static void main(String[] args) {
        Folder root = new Folder("root");
        root.add(new File("readme.txt", 100));

        Folder src = new Folder("src");
        src.add(new File("Main.java", 500));
        src.add(new File("Utils.java", 300));
        root.add(src);

        root.display(0);
        System.out.println("Total size: " + root.getSize() + " bytes");
    }
}
