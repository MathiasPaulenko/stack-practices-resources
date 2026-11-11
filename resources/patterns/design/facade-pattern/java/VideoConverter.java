class VideoDecoder {
    String decode(String file) { return "Decoded " + file; }
}

class VideoEncoder {
    String encode(String stream, String format, int bitrateKbps) {
        return "Encoded to " + format + " at " + bitrateKbps + " kbps";
    }
}

class BitRateCalculator {
    int calculate(String source) { return 1024; }
}

class AudioMixer {
    String mix(String stream) { return "Mixed " + stream; }
}

public class VideoConverter {
    // Facade that hides the complexity of video conversion.
    private final VideoDecoder decoder = new VideoDecoder();
    private final VideoEncoder encoder = new VideoEncoder();
    private final BitRateCalculator bitrate = new BitRateCalculator();
    private final AudioMixer audio = new AudioMixer();

    public String convert(String sourceFile, String destinationFormat) {
        String decoded = decoder.decode(sourceFile);
        int rate = bitrate.calculate(decoded);
        String mixed = audio.mix(decoded);
        return encoder.encode(mixed, destinationFormat, rate);
    }

    public static void main(String[] args) {
        VideoConverter converter = new VideoConverter();
        System.out.println(converter.convert("movie.mp4", "avi"));
        // Encoded to avi at 1024 kbps

        // The subsystem stays reachable: callers can bypass the facade.
        System.out.println(new VideoEncoder().encode("raw frames", "mkv", 2048));
    }
}
