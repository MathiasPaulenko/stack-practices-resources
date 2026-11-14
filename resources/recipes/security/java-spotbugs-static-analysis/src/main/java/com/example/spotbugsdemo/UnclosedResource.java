package com.example.spotbugsdemo;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * Intentionally buggy: SpotBugs reports OBL_UNSATISFIED_OBLIGATION because
 * the reader is not closed on every path. Fix with try-with-resources.
 */
public class UnclosedResource {

    public String readFirstLine(String path) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(path));
        return reader.readLine();
    }
}
