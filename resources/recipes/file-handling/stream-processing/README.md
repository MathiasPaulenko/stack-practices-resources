# Process Large Files with Streams — Code Examples

Companion code for [Process Large Files with Streams](https://stackpractices.com/recipes/stream-processing/) on StackPractices.

## Files

| File | Description |
|---|---|
| `python_reader.py` | Minimal line-by-line CSV reader with `open()` (Python) |
| `nodejs_reader.js` | Minimal read stream with `data` events (Node.js) |
| `FileProcessor.java` | Minimal `BufferedReader` line processor (Java) |
| `etl_pipeline.py` | CSV → JSONL ETL pipeline with progress tracking and atomic rename |
| `process_large_file.js` | `pipeline()` + `Transform` with backpressure handling (Node.js) |
| `ParallelStreamProcessor.java` | Batched parallel processing with a thread pool (Java) |
| `fifo_pipeline.sh` | Named-pipe (FIFO) streaming between processes (Bash) |

Every example reads a chunk at a time, so memory stays flat regardless of file size. Outputs are written to a `.tmp` file and renamed atomically to avoid corrupting data on failure.
