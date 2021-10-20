from bitarray import bitarray
import numpy as np
import struct
import zlib
import decoder
import audio

def encode(src, dst, msg):
    #Wywolamy funkcję
    #encode(1,2,'abc')
    # żeby przesłać wiadomość abc od 1 do 2

    # Reprezentacja src,dst,msg na bitach
    # src, dst : int (rzutowanie na 6 bajtów)
    src = struct.pack('!LH', src//(2**15), src%(2**15))
    dst = struct.pack('!LH', dst//(2**15), dst%(2**15))
    #msg : bytes, str
    if isinstance(msg, str):
        msg = bytes(msg, 'utf8')

    #reprezentacja przez bitarray
    b = bitarray()
    b.frombytes(msg)

    # Skonstruować ramkę
    frame = dst + src + struct.pack("!H", len(msg)) + msg
    print(type(frame))
    print(type(zlib.crc32(frame)))
    crc32 = zlib.crc32(frame)
    crc32 = struct.pack("!L", crc32)
    frame = frame + crc32
    # crc32: potraktuj bity jako współczynniki, dopisz 32 zera na końcu. Podziel z resztą przez 100000100110000010001110110110111 i zwrócić resztę z dzielenia.
    frame = bitarray(frame)
    # Skonstruować ciąg bitów do nadania
    preamble = bitarray('10101010' * 7 + '10101011')
    bits = preamble + decoder.NRZI(decoder.B4B5(frame))

    return bits
    # w NRZI pierwszy bit reprezentujemy jako zmianę względem ostatniej jedynki w preambule.

    #Wyemitować
    #glosnik(bity, 0.1, 440, 880)


def decode(bits):
    bits = bits[64:]
    crc32 = bits[-32:]
    bits = bits[:-32]
    check = bitarray(zlib.crc32(bits))
    if check != crc32:
        print("ERROR")
        print(crc32)
        print(check)
    print(crc32)
    return bits

if __name__ == "__main__":
    print(decode(encode(1,2,'abc')))