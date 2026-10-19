"""
Task 3 - AES in CBC mode: text encryption + chunked file encryption.
Course: Information Security (Lab) - Week 06
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib
import os
import struct

CHUNK = 64 * 1024                      # 64 KB read size
BLOCK = AES.block_size                 # 16 bytes
MAGIC = b"AESCBC01"                    # 8-byte format tag
HEADER = len(MAGIC) + 8 + BLOCK        # magic + filesize + IV


# ----------------------------------------------------------------------
# 3.1  Text encryption
# ----------------------------------------------------------------------
def aes_encrypt_text(key, iv, text):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(text, BLOCK))


def aes_decrypt_text(key, iv, data):
    return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(data), BLOCK)


# ----------------------------------------------------------------------
# 3.2  File encryption (streaming, 64 KB chunks)
# ----------------------------------------------------------------------
def encrypt_file(in_path, out_path):
    """
    Container layout:  MAGIC(8) | ORIGINAL_SIZE(8, big endian) | IV(16) | CIPHERTEXT
    The key is NOT stored in the container - it is kept by the caller.
    One block of plaintext is always held back so that padding is applied
    exactly once, on the final block, at end of file.
    """
    key = get_random_bytes(16)
    iv = get_random_bytes(BLOCK)
    size = os.path.getsize(in_path)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
        fout.write(MAGIC)
        fout.write(struct.pack(">Q", size))
        fout.write(iv)

        buf = b""
        while True:
            chunk = fin.read(CHUNK)
            if not chunk:
                break
            buf += chunk
            if len(buf) > BLOCK:
                n = ((len(buf) - 1) // BLOCK) * BLOCK   # keep 1..16 bytes back
                fout.write(cipher.encrypt(buf[:n]))
                buf = buf[n:]
        fout.write(cipher.encrypt(pad(buf, BLOCK)))     # padded final block
    return key, iv, size


def decrypt_file(in_path, out_path, key):
    with open(in_path, "rb") as fin:
        if fin.read(len(MAGIC)) != MAGIC:
            raise ValueError("Not an AESCBC01 container")
        size = struct.unpack(">Q", fin.read(8))[0]
        iv = fin.read(BLOCK)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(out_path, "wb") as fout:
            buf = b""
            while True:
                chunk = fin.read(CHUNK)
                if not chunk:
                    break
                buf += chunk
                if len(buf) > BLOCK:
                    n = ((len(buf) - 1) // BLOCK) * BLOCK
                    fout.write(cipher.decrypt(buf[:n]))
                    buf = buf[n:]
            fout.write(unpad(cipher.decrypt(buf), BLOCK))

    if os.path.getsize(out_path) != size:
        raise ValueError("Restored size does not match stored header size")
    return size


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(CHUNK), b""):
            h.update(b)
    return h.hexdigest()


if __name__ == "__main__":
    print("=" * 68)
    print(" TASK 3.1 : AES-128 CBC TEXT ENCRYPTION")
    print("=" * 68)
    key = get_random_bytes(16)
    iv = get_random_bytes(BLOCK)
    msg = b"AES in CBC mode chains each block with the previous ciphertext."
    ct = aes_encrypt_text(key, iv, msg)

    print(f"Key (16 bytes) : {key.hex()}")
    print(f"IV  (16 bytes) : {iv.hex()}")
    print(f"Plaintext      : {msg.decode()}")
    print(f"Plain length   : {len(msg)} bytes")
    print(f"Ciphertext     : {ct.hex()}")
    print(f"Cipher length  : {len(ct)} bytes ({len(ct) // BLOCK} blocks)")
    print(f"Recovered      : {aes_decrypt_text(key, iv, ct).decode()}")
    print(f"Round-trip OK  : {aes_decrypt_text(key, iv, ct) == msg}")
    print()

    print("=" * 68)
    print(" TASK 3.2 : AES-128 CBC FILE ENCRYPTION (64 KB CHUNKS)")
    print("=" * 68)
    src, enc, dec = "sample_data.bin", "sample_data.enc", "sample_data.dec"
    with open(src, "wb") as f:
        f.write(os.urandom(300_000))          # 300 KB test payload

    k, iv, size = encrypt_file(src, enc)
    print(f"Source file     : {src}  ({size:,} bytes)")
    print(f"Container       : {enc}  ({os.path.getsize(enc):,} bytes)")
    print(f"  header        : {HEADER} bytes  (magic 8 + size 8 + IV 16)")
    print(f"  payload       : {os.path.getsize(enc) - HEADER:,} bytes")
    print(f"Session key     : {k.hex()}   (kept out of the container)")
    print(f"IV              : {iv.hex()}")
    print(f"Header layout   : MAGIC={MAGIC.decode()} | "
          f"SIZE={size} | IV={iv.hex()[:16]}...")
    print()

    restored = decrypt_file(enc, dec, k)
    print(f"Decrypted file  : {dec}  ({restored:,} bytes)")
    print(f"SHA-256 source  : {sha256(src)}")
    print(f"SHA-256 restored: {sha256(dec)}")
    print(f"Files identical : {sha256(src) == sha256(dec)}")
    print("=" * 68)

    for p in (src, enc, dec):
        os.remove(p)
