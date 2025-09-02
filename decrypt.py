#!/usr/bin/env python3

import gnupg


def decrypt(ciphertext):
    ciphertext = ciphertext.replace("|", "\n")

    gpg = gnupg.GPG()
    result = gpg.decrypt(ciphertext)

    if not result.ok:
        raise RuntimeError(f"GPG decryption failed: {result.stderr}")

    return str(result)
