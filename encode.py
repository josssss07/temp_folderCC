import os
import shutil
import json
import random
import string
from pathlib import Path

BASE_DIR = Path("/tmp/secret_store")
MAPPING_FILE = BASE_DIR / ".mapping.json"

def random_name(length=12):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))

def char_to_bits(char):
    ascii_val = ord(char)
    return format(ascii_val, "08b")   # 8-bit binary string

def write_bit_file(folder, bit, index):
    """Write a file with deterministic size based on bit value"""
    # Use sequential numbering with leading zeros to preserve order
    filename = f"{index:04d}"
    filepath = folder / filename

    # Deterministic file sizes: 2 bytes for bit 0, 1 byte for bit 1
    if bit == "0":
        size = 2  # even
    else:
        size = 1  # odd

    with open(filepath, "wb") as f:
        f.write(b"\x00" * size)

def encode_message(message):
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    words = message.split()
    mapping = []  # List of dicts to preserve order

    for word_index, word in enumerate(words):
        # Create random folder name for each word
        random_folder_name = random_name(12)
        word_folder = BASE_DIR / random_folder_name
        word_folder.mkdir(exist_ok=True)
        
        # Store mapping with index to preserve word order
        mapping.append({
            "index": word_index,
            "folder": random_folder_name,
            "word": word
        })

        bit_index = 0
        for char in word:
            bits = char_to_bits(char)

            for bit in bits:
                write_bit_file(word_folder, bit, bit_index)
                bit_index += 1

    # Save mapping file
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f)

    print(f"Encoded message written to: {BASE_DIR}")

def cleanup():
    """Delete all folders and files in the secret store"""
    if BASE_DIR.exists():
        shutil.rmtree(BASE_DIR)
        print(f"Cleaned up: {BASE_DIR}")
    else:
        print(f"{BASE_DIR} does not exist")

if __name__ == "__main__":
    cleanup()
    secret = input("Enter secret message: ")
    encode_message(secret)