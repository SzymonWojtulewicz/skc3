from bitarray import bitarray

codes = {
    tuple([0, 0, 0, 0]): [1, 1, 1, 1, 0],
    tuple([0, 0, 0, 1]): [0, 1, 0, 0, 1],
    tuple([0, 0, 1, 0]): [1, 0, 1, 0, 0],
    tuple([0, 0, 1, 1]): [1, 0, 1, 0, 1],
    tuple([0, 1, 0, 0]): [0, 1, 0, 1, 0],
    tuple([0, 1, 0, 1]): [0, 1, 0, 1, 1],
    tuple([0, 1, 1, 0]): [0, 1, 1, 1, 0],
    tuple([0, 1, 1, 1]): [0, 1, 1, 1, 1],
    tuple([1, 0, 0, 0]): [1, 0, 0, 1, 0],
    tuple([1, 0, 0, 1]): [1, 0, 0, 1, 1],
    tuple([1, 0, 1, 0]): [1, 0, 1, 1, 0],
    tuple([1, 0, 1, 1]): [1, 0, 1, 1, 1],
    tuple([1, 1, 0, 0]): [1, 1, 0, 1, 0],
    tuple([1, 1, 0, 1]): [1, 1, 0, 1, 1],
    tuple([1, 1, 1, 0]): [1, 1, 1, 0, 0],
    tuple([1, 1, 1, 1]): [1, 1, 1, 0, 1]
}


def NRZI(a):
    out = bitarray()
    last = 1
    for b in a:
        if b == last:
            out.append(0)
        else:
            out.append(1)
        last = b
    return out


def B4B5(a):
    out = bitarray()

    a.extend([0]*((-len(a)) % 4))

    buffor = bitarray()
    for b in a:
        buffor.append(b)
        if len(buffor) == 4:
            out.extend(codes[tuple(buffor)])
            buffor = bitarray()

    return out


if __name__ == "__main__":
    a = bitarray([1, 0, 0, 1, 1, 1, 0, 0])
    print(a)
    print(NRZI(a))
    print(B4B5(a))
