# SOFA Files Guide

## What are SOFA Files?

SOFA (Spatially Oriented Format for Acoustics) files contain Head-Related Transfer Functions (HRTFs) that describe how sound is perceived from different directions. These are used to create realistic 3D/spatial audio effects when listening with headphones.

## Included SOFA File

### irc_1003.sofa

**Type:** HRTF Database
**Source:** IRCAM (Institut de Recherche et Coordination Acoustique/Musique)
**Description:** General-purpose HRTF suitable for most users

**Characteristics:**
- Measured from average human head model
- Good for general spatial audio applications
- Works well for movies, games, and music
- Balanced frequency response

## Where to Find More SOFA Files

### Official Sources

1. **SOFA Conventions Website**
   - URL: https://www.sofaconventions.org/
   - Description: Official SOFA file repository
   - Contains various HRTF databases

2. **Club Fritz Database**
   - URL: https://www.sofaconventions.org/mediawiki/index.php/Files
   - Description: Free HRTF database
   - Multiple subjects and positions

3. **IRCAM LISTEN Database**
   - URL: http://recherche.ircam.fr/equipes/salles/listen/
   - Description: High-quality HRTF measurements
   - Research-grade data

4. **ARI Database (Austrian Academy of Sciences)**
   - URL: https://www.kfs.oeaw.ac.at/
   - Description: Comprehensive HRTF collection
   - Multiple subjects and dense spatial sampling

5. **SADIE Database**
   - URL: https://www.york.ac.uk/sadie-project/
   - Description: Spatial Audio for Domestic Interactive Entertainment
   - Well-documented database

## Choosing the Right SOFA File

### For General Use
- **irc_1003.sofa** (included): Good all-around choice
- **KEMAR SOFA files**: Industry-standard dummy head measurements

### For Movies
- Look for SOFA files with:
  - Wide frequency range (20Hz - 20kHz)
  - Dense spatial sampling
  - Smooth frequency response

### For Music
- Similar to movies but consider:
  - Natural timbre preservation
  - Minimal coloration
  - Good stereo imaging

### For Gaming
- Prioritize:
  - Fast transient response
  - Clear directional cues
  - Low latency processing

### For Immersive Experiences
- Choose SOFA files with:
  - Very dense spatial sampling (many measurement points)
  - Elevation information
  - Distance cues

## Testing Different SOFA Files

### Quick Test Script

Create `test_sofa.sh`:

```bash
#!/bin/bash

# Test different SOFA files on the same video
INPUT="test_video.mkv"
OUTPUT_DIR="sofa_tests"

mkdir -p "$OUTPUT_DIR"

for sofa in *.sofa; do
    echo "Testing: $sofa"
    python auto_sofalizer.py \
        "./$INPUT" \
        "$OUTPUT_DIR" \
        mkv \
        1 \
        --sofa "$sofa"
    
    # Rename output to include SOFA name
    mv "$OUTPUT_DIR/test_video(sofa).mkv" "$OUTPUT_DIR/test_video_${sofa%.sofa}.mkv"
done

echo "Test complete! Compare files in $OUTPUT_DIR"
```

### Subjective Testing Checklist

When testing SOFA files, evaluate:

- [ ] **Externalization**: Does audio sound "outside" your head?
- [ ] **Localization**: Can you identify sound direction?
- [ ] **Timbre**: Does audio sound natural?
- [ ] **Immersion**: Does it feel realistic?
- [ ] **Fatigue**: Can you listen for extended periods?
- [ ] **Elevation**: Can you perceive height differences?

## Creating Custom SOFA Files

### Commercial Solutions
1. **3Dio Free Space Pro II** - Binaural microphone
2. **Neumann KU 100** - Dummy head
3. **HEAD acoustics** - Professional HRTF measurement systems

### DIY Approaches
- Use in-ear microphones
- Record from multiple positions
- Process with SOFA tools (MATLAB/Python)
- Tools: SOFAtoolbox, pysofaconventions

### Software Tools

**Python:**
```bash
pip install pysofaconventions
```

**MATLAB:**
- Download SOFAtoolbox from sofaconventions.org
- Includes tools for creating/editing SOFA files

## SOFA File Specifications

### File Structure
```
SOFA File
├── Data (IR - Impulse Response)
├── SourcePosition (azimuth, elevation, distance)
├── ReceiverPosition (ear positions)
├── ListenerPosition
└── EmitterPosition
```

### Common Dimensions
- **Sampling Rate**: 44.1 kHz, 48 kHz, 96 kHz
- **Positions**: 50-2500+ measurement points
- **IR Length**: 256-8192 samples typical

## Validating SOFA Files

### Check SOFA File Information

Create `sofa_info.py`:

```python
#!/usr/bin/env python3
import sys

try:
    import sofar as sf
    
    if len(sys.argv) < 2:
        print("Usage: python sofa_info.py <sofa_file>")
        sys.exit(1)
    
    sofa_file = sys.argv[1]
    sofa = sf.read_sofa(sofa_file)
    
    print(f"SOFA File: {sofa_file}")
    print(f"Data Type: {sofa.GLOBAL_DataType}")
    print(f"Sampling Rate: {sofa.Data_SamplingRate} Hz")
    print(f"Measurements: {sofa.Data_IR.shape[0]}")
    print(f"Receivers: {sofa.Data_IR.shape[1]}")
    print(f"Samples: {sofa.Data_IR.shape[2]}")
    
except ImportError:
    print("Install pysofaconventions: pip install pysofaconventions")
```

### Using FFmpeg to Verify

```bash
# Test SOFA file with FFmpeg directly
ffmpeg -i test_audio.wav -af "sofalizer=sofa=test.sofa" -f null -

# If no errors, the SOFA file is valid
```

## Troubleshooting SOFA Files

### Issue: "Invalid SOFA file"
**Solution:**
- Check file is not corrupted (download again)
- Verify SOFA format version compatibility
- Use validation tools

### Issue: "No spatial effect perceived"
**Solution:**
- Ensure using headphones (not speakers!)
- Try different SOFA file
- Check source audio has sufficient spatial information
- Test with known binaural content

### Issue: "Audio sounds unnatural/muffled"
**Solution:**
- SOFA file may not match your ear anatomy
- Try different SOFA file from different database
- Check SOFA file sample rate matches audio
- Consider custom HRTF measurement

### Issue: "FFmpeg SOFA filter error"
**Solution:**
- Verify FFmpeg compiled with SOFA support:
  ```bash
  ffmpeg -filters | grep sofalizer
  ```
- Update FFmpeg if needed
- Check SOFA file path is correct

## SOFA File Recommendations

### Budget/Free Options
1. **IRC_1003** (included) - Excellent starting point
2. **KEMAR** - Industry standard
3. **MIT KEMAR** - Classic research HRTF

### Best for Movies
1. **SADIE Database** - Dense sampling, cinematic
2. **IRCAM LISTEN** - High quality, immersive

### Best for Music
1. **Club Fritz** - Natural timbre
2. **HUTUBS** - Multiple subjects to choose from

### Most Realistic
1. **Custom measured HRTFs** - Your own ears!
2. **Multi-subject averaged** - Good compromise

## Advanced Topics

### Interpolation
- Some SOFA files support interpolation
- FFmpeg sofalizer can interpolate between measurement points
- Higher density = better localization accuracy

### Distance Modeling
- Near-field vs far-field HRTFs
- Room acoustics integration
- Reverberation considerations

### Individual HRTFs
- Most accurate spatial audio
- Requires custom measurement
- Significantly improves localization

## Resources

### Documentation
- [SOFA Conventions Spec](https://www.sofaconventions.org/mediawiki/index.php/SOFA_conventions)
- [FFmpeg Sofalizer Filter](https://ffmpeg.org/ffmpeg-filters.html#sofalizer)
- [Spatial Audio Wikipedia](https://en.wikipedia.org/wiki/Spatial_audio)

### Research Papers
- "The SOFA File Format Specification" (AES Convention 2013)
- "Individualization of Head-Related Transfer Functions" (various)
- "Binaural Audio Rendering" (Handbook)

### Communities
- [r/spatialAudio](https://reddit.com/r/spatialaudio) - Reddit community
- [AES Forums](https://aes.org) - Audio Engineering Society
- [Hydrogen Audio](https://hydrogenaud.io) - Technical audio forum

## Contribution

Have experience with specific SOFA files? Found great sources?
Please contribute to this guide by submitting a pull request!

---

**Experiment with different SOFA files to find what works best for your ears! 🎧**

