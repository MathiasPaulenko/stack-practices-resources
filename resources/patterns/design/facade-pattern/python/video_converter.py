class VideoDecoder:
    def decode(self, file):
        return f"Decoded {file}"


class VideoEncoder:
    def encode(self, stream, format, bitrate_kbps):
        return f"Encoded to {format} at {bitrate_kbps} kbps"


class BitRateCalculator:
    def calculate(self, source):
        return 1024


class AudioMixer:
    def mix(self, stream):
        return f"Mixed audio for {stream}"


class VideoConverter:
    """Facade that hides the complexity of video conversion."""

    def __init__(self):
        self._decoder = VideoDecoder()
        self._encoder = VideoEncoder()
        self._bitrate = BitRateCalculator()
        self._audio = AudioMixer()

    def convert(self, source_file, destination_format):
        decoded = self._decoder.decode(source_file)
        bitrate = self._bitrate.calculate(decoded)
        mixed = self._audio.mix(decoded)
        return self._encoder.encode(mixed, destination_format, bitrate)


if __name__ == "__main__":
    converter = VideoConverter()
    print(converter.convert("movie.mp4", "avi"))
    # Encoded to avi at 1024 kbps

    # The subsystem stays reachable: callers can bypass the facade
    # when they need fine-grained control.
    print(VideoEncoder().encode("raw frames", "mkv", 2048))
