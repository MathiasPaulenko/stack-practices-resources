class VideoDecoder {
  decode(file) { return `Decoded ${file}`; }
}

class VideoEncoder {
  encode(stream, format, bitrateKbps) {
    return `Encoded to ${format} at ${bitrateKbps} kbps`;
  }
}

class BitRateCalculator {
  calculate(source) { return 1024; }
}

class AudioMixer {
  mix(stream) { return `Mixed ${stream}`; }
}

class VideoConverter {
  // Facade that hides the complexity of video conversion.
  constructor() {
    this.decoder = new VideoDecoder();
    this.encoder = new VideoEncoder();
    this.bitrate = new BitRateCalculator();
    this.audio = new AudioMixer();
  }

  convert(sourceFile, destinationFormat) {
    const decoded = this.decoder.decode(sourceFile);
    const rate = this.bitrate.calculate(decoded);
    const mixed = this.audio.mix(decoded);
    return this.encoder.encode(mixed, destinationFormat, rate);
  }
}

// Client code
const converter = new VideoConverter();
console.log(converter.convert('movie.mp4', 'avi'));
// Encoded to avi at 1024 kbps

// The subsystem stays reachable: callers can bypass the facade
// when they need fine-grained control.
console.log(new VideoEncoder().encode('raw frames', 'mkv', 2048));
