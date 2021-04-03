#!/usr/bin/env python3

from pyblake2 import blake2b

ellH = 64

def xor(l, r):
    return bytes([l^r for (l, r) in zip(l, r)])

def G(i, m, ellR):
    return b''.join([blake2b(person=b"UA_F4Jumble_G_" + bytes([i, j]), data=m).digest() for j in range((ellR+ellH-1)//ellH)])[:ellR]

def H(i, m, ellL):
    return blake2b(person=b"UA_F4Jumble_H_" + bytes([i, 0]), data=m, digest_size=ellL).digest()

def f4jumble(M):
    ellM = len(M)
    assert ellM >= 22
    ellL = min(ellH, ellM//2)
    ellR = ellM - ellL

    a = M[:ellL]
    b = M[ellL:]
    x = xor(b, G(0, a, ellR))
    y = xor(a, H(0, x, ellL))
    d = xor(x, G(1, y, ellR))
    c = xor(y, H(1, d, ellL))
    return c + d

def f4unjumble(M):
    ellM = len(M)
    assert ellM >= 22
    ellL = min(ellH, ellM//2)
    ellR = ellM - ellL

    c = M[:ellL]
    d = M[ellL:]
    y = xor(c, H(1, d, ellL))
    x = xor(d, G(1, y, ellR))
    a = xor(y, H(0, x, ellL))
    b = xor(x, G(0, a, ellR))
    return a + b


tv = b"From each according to their ability, to each according to their needs!"
tvout = "eafec69127bcc29af38edee03629758e671c32edeb09ce3c12b7151be771a8a7cdb3550a0138548e8d32541d7ee46d4960595b38c4249a01f2b051f7e67a5446ac0e5dedbd31d9"

#print(f4jumble(tv).hex())
assert f4jumble(tv).hex() == tvout
assert f4unjumble(f4jumble(tv)) == tv
