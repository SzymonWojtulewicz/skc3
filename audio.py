#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import numpy
import pyaudio
import wave
import sys

CHUNK = 1024
CHANNELS = 1
SAMPLE_WIDTH = 2
SAMPLE_TYPE = numpy.dtype('<i2')
SAMPLE_MAX = 2**15 - 1
FRAMERATE = 44000

numpy.set_printoptions(threshold=sys.maxsize)

pa = pyaudio.PyAudio()


def wave_open(path):
    audio = wave.open(path, 'rb')
    return audio


def mic_open():
    audio = pa.open(
        input=True,
        channels=CHANNELS,
        rate=FRAMERATE,
        format=pa.get_format_from_width(SAMPLE_WIDTH),
    )
    return audio


def audio_read(audio, chunk=CHUNK):
    if isinstance(audio, wave.Wave_read):
        raw = audio.readframes(chunk)
    else:
        raw = audio.read(chunk)
    frames = numpy.frombuffer(raw, dtype=SAMPLE_TYPE).astype(numpy.float)
    frames /= SAMPLE_MAX
    frames.clip(-1, 1)
    return frames


def audio_close(audio):
    if isinstance(audio, wave.Wave_read):
        audio.close()
    else:
        audio.stop_stream()
        audio.close()


def audio_write(audio, writeToFile=False, filename="audio.wav"):

    if isinstance(audio, wave.Wave_read):
        nc = audio.getnchannels()
        sw = audio.getsampwidth()
        fr = audio.getframerate()
        raw = audio.readframes(audio.getnframes())
    else:
        nc = CHANNELS
        sw = SAMPLE_WIDTH
        fr = FRAMERATE
        raw = audio.read(CHUNK)

    if writeToFile:
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(nc)
        wave_file.setsampwidth(sw)
        wave_file.setframerate(fr)
        wave_file.writeframes(raw)
    else:
        stream = pa.open(
            format=pa.get_format_from_width(sw),
            channels=nc, rate=fr, output=True
        )
        stream.write(raw)


audio = None
if len(sys.argv) > 1:
    audio = wave_open(sys.argv[1])
else:
    audio = mic_open()

# print(audio_read(audio))
audio_write(audio)

audio_close(audio)
pa.terminate()
