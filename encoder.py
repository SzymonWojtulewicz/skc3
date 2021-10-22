from bitarray import bitarray
from bitarray.util import int2ba
import numpy as np
import struct
import zlib
import coder
import audio
import sinWave


def encode(src, dst, msg):

    # convert to bytes
    src = struct.pack('!LH', src//(2**15), src % (2**15))
    dst = struct.pack('!LH', dst//(2**15), dst % (2**15))

    if isinstance(msg, str):
        msg = bytes(msg, 'utf8')

    # convert to bitarrays
    source = bitarray()
    source.frombytes(src)
    destination = bitarray()
    destination.frombytes(dst)
    messsage = bitarray()
    messsage.frombytes(msg)
    length = bitarray()
    length.frombytes(struct.pack("!H", len(messsage)))

    frame = source + destination + length + messsage

    # a control polynomial
    crc32 = zlib.crc32(frame)
    crc32 = struct.pack("!L", crc32)
    crc32B = bitarray()
    crc32B.frombytes(crc32)

    frame = frame + crc32B

    # add an encoding
    preamble = bitarray('10101010' * 7 + '10101011')
    bits = preamble + coder.NRZI(coder.B4B5(frame))

    sinWave.play_message(bits)

    return bits

    # Wyemitować
    # glosnik(bity, 0.1, 440, 880)


def decode(bits):

    # ommit first bits and decode
    bits = bits[64:]
    bits = coder.reB4B5(coder.reNRZI(bits))

    # assign parts to various properties
    crc32 = bits[-32:]
    source = bits[:48]
    destination = bits[48:96]
    length = bits[96:112]
    message = bits[112:-32]
    frame = bits[:-32]
    check = bits[-32:]

    # a control polynomial
    crc32 = zlib.crc32(frame)
    crc32 = struct.pack("!L", crc32)
    crc32B = bitarray()
    crc32B.frombytes(crc32)

    # check if the crc32 codes match
    if check != crc32B:
        raise ValueError("crc32 codes don't match")

    # change bitarrays to values
    src = struct.unpack('!LH', source)
    dst = struct.unpack('!LH', destination)
    src = src[0]*(2**15) + src[1] % (2**15)
    dst = dst[0]*(2**15) + dst[1] % (2**15)
    ln = struct.unpack("!H", length)[0]
    msg = bytes(message).decode('utf-8')

    return (src, dst, msg)


if __name__ == "__main__":
    # a = bitarray([0, 0, 1, 1, 0, 1, 1, 0, 1])
    # print(a)
    # print(coder.reB4B5(coder.reNRZI((coder.NRZI(coder.B4B5(a))))))
    # print(coder.reNRZI((coder.NRZI(a))))
    print(decode(encode(7349183274, 591049237, '')))
