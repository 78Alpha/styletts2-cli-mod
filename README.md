[Original Repo](https://github.com/yl4579/StyleTTS2) - **CLI Tool** - [Streaming API](https://github.com/neuralVox/styletts2)

# Usage

## Join Audio CLI (Not personnaly used, part of original)

```bash
python join.py audio1.wav audio2.mp3 audio3.mp4 audio4.ogg output.mp3
```

## Inference CLI

Docs:
```
StyleTTS 2 CLI Inference
Usage: cli.py [OPTIONS] TEXT OUTPUT

options:
  -h, --help            show this help message and exit
  -f, --file            Use a file for text input (Script.txt), boolean
  -b, --batch           Every new line will save as an audio file, boolean
  -p PTHPATH, --pthpath PTHPATH Where the pth model is stored, path
  -t TEXT, --text TEXT  Text or file to use as text, string or path
  -a AUDIO, --audio AUDIO Audio file to use as a reference voice, path
  -v ALPHA, --alpha ALPHA Alpha for STTS2, sets the tiimbre or how closely to resemble the reference, float from 0.0 to 1.0
  -e BETA, --beta BETA Beta for STTS2, sets the prosidy, emotional variable, to resemble the reference, float from 0.0 to 1.0
  -s SCALE, --scale SCALE CFG, or classifier free guidance scale, how diverse it will be, or emotional, float
  -x, --denoiseonly Use resemble-enhance in denoise only mode, boolean
  -y LAMBD, --lambd LAMBD The denoise amount for resemble-enhance, float from 0.0 to 1.0
  -z NFE, --nfe NFE Quality setting for resemble-enahnce, no more than 128, but 128 is suggested.
```

Requirements:
```resemble-enahce
pip install resemble-enhance --upgrade
```
Inference:
```bash
python cli.py -t "Let's get this party started!" -a "/mnt/a/example.wav" -p "/mnt/a/Model_2nd_00049.pth" -b -x -y 0.5 -z 128
```

Inference from a file:
```bash
python cli.py -t ./Script.txt -a "/mnt/a/example.wav" -p "/mnt/a/Model_2nd_00049.pth" -f -b -x -y 0.5 -z 128
```

## License

GPL due to Phonemizer (soon to be permissively licensed as soon as I find a permissively-licensed Phonemizer replacement)
