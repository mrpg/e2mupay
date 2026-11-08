#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-gnupg",
# ]
#
# [tool.uv.sources]
# python-gnupg = { git = "https://github.com/vsajip/python-gnupg", rev = "d107c34b652680ed0df07f14b0837f2e587d1b1e" }
# ///

import json
import sys

import gnupg


def decrypt(ciphertext):
    """Decrypt a pipe-separated OpenPGP submission and return its JSON object."""
    ciphertext = ciphertext.replace("|", "\n")

    gpg = gnupg.GPG(encoding="utf-8")
    result = gpg.decrypt(ciphertext)

    if not result.ok:
        raise RuntimeError(f"GPG decryption failed: {result.stderr}")

    return json.loads(str(result))


if __name__ == "__main__":
    print(json.dumps(decrypt(sys.stdin.read()), ensure_ascii=False, indent=2))
