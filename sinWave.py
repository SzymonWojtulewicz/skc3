import numpy as np
import pyaudio
import random


FREQ_1 = 440
FREQ_2 = 880
INTERVAL = 2
VOLUME = .5

FRAMERATE = 88000
SAMPLE_MAX = 2**15 - 1
CHANNELS = 1
SAMPLE_WIDTH = 2

# np.set_printoptions(precision=3)
# np.set_printoptions(suppress=True)


def gen_interval(freq):
    freq *= 2
    nsamples = FRAMERATE/freq
    temp = np.arange(nsamples)
    temp = (np.sin(temp * 2 * np.pi / nsamples)
            * SAMPLE_MAX*VOLUME).astype(np.int32)
    temp = np.tile(temp, int(INTERVAL*freq*2))
    return temp

def play_message(bits):
    a = gen_interval(FREQ_1)
    b = gen_interval(FREQ_2)

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pa.get_format_from_width(SAMPLE_WIDTH),
                     channels=CHANNELS,
                     rate=FRAMERATE,
                     output=True)

    stream.stop_stream()
    stream.close()

    pa.terminate()

if __name__ == "__main__":
    a = gen_interval(FREQ_1)
    b = gen_interval(FREQ_2)

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pa.get_format_from_width(SAMPLE_WIDTH),
                     channels=CHANNELS,
                     rate=FRAMERATE,
                     output=True)

    for i in range(20):
        stream.write(a)
        stream.write(b)

    for i in range(100):
        if random.randint(0, 1):
            stream.write(a)
        else:
            stream.write(b)

    # data = [0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1]

    # for d in data:
    #     if d == 0:
    #         stream.write(a)
    #     else:
    #         stream.write(b)

    stream.stop_stream()
    stream.close()

    pa.terminate()
