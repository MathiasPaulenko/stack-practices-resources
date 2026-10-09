import java.io.*;
import java.nio.file.*;
import java.util.zip.*;
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Stream;

/**
 * Batch archive utilities for Java (JDK 11+, java.util.zip only).
 */
public class BatchCompressor {

    /** GZIP a single file. */
    public static void gzipFile(Path src, Path dest, int bufferSize) throws IOException {
        try (InputStream fis = Files.newInputStream(src);
             OutputStream fos = Files.newOutputStream(dest);
             GZIPOutputStream gzos = new GZIPOutputStream(fos, bufferSize)) {
            fis.transferTo(gzos);
        }
    }

    /** ZIP multiple files with streaming. */
    public static int zipFiles(List<Path> sources, Path destZip) throws IOException {
        int count = 0;
        try (OutputStream fos = Files.newOutputStream(destZip);
             ZipOutputStream zos = new ZipOutputStream(fos)) {
            for (Path src : sources) {
                zos.putNextEntry(new ZipEntry(src.getFileName().toString()));
                try (InputStream fis = Files.newInputStream(src)) {
                    fis.transferTo(zos);
                }
                zos.closeEntry();
                count++;
            }
        }
        return count;
    }

    /** Extract ZIP with zip-slip protection (Path.startsWith is component-wise). */
    public static int extractZipSafe(Path zipPath, Path destDir) throws IOException {
        Files.createDirectories(destDir);
        int count = 0;
        try (InputStream fis = Files.newInputStream(zipPath);
             ZipInputStream zis = new ZipInputStream(fis)) {
            ZipEntry entry;
            while ((entry = zis.getNextEntry()) != null) {
                Path destFile = destDir.resolve(entry.getName()).normalize();
                if (!destFile.startsWith(destDir)) {
                    throw new IOException("Unsafe zip entry: " + entry.getName());
                }
                if (entry.isDirectory()) {
                    Files.createDirectories(destFile);
                } else {
                    Files.createDirectories(destFile.getParent());
                    Files.copy(zis, destFile, StandardCopyOption.REPLACE_EXISTING);
                }
                count++;
            }
        }
        return count;
    }

    /** Compress all files in a directory. */
    public static int compressDirectory(Path srcDir, Path destZip) throws IOException {
        List<Path> files = new ArrayList<>();
        try (Stream<Path> stream = Files.walk(srcDir)) {
            stream.filter(Files::isRegularFile).forEach(files::add);
        }
        return zipFiles(files, destZip);
    }
}
