import os
import json
from pathlib import Path

BASE_DIR = Path("/tmp/secret_store")
MAPPING_FILE = BASE_DIR / ".mapping.json"

def file_size_bit(filepath):
    size = os.path.getsize(filepath)
    return "0" if size % 2 == 0 else "1"

def bits_to_char(bits):
    return chr(int(bits, 2))

def decode_message():
    if not BASE_DIR.exists():
        print(f"Error: {BASE_DIR} does not exist. Run encode.py first.")
        return

    if not MAPPING_FILE.exists():
        print(f"Error: {MAPPING_FILE} does not exist. Invalid encoding.")
        return

    # Load mapping
    with open(MAPPING_FILE, "r") as f:
        mapping = json.load(f)

    # Sort by index to preserve original word order
    mapping = sorted(mapping, key=lambda x: x["index"])

    words = []

    for entry in mapping:
        random_folder_name = entry["folder"]
        folder = BASE_DIR / random_folder_name
        
        if not folder.is_dir():
            continue

        bitstream = ""

        # Sort files numerically (by the index in filename) to preserve order
        files = sorted(folder.iterdir(), key=lambda f: int(f.name))
        for file in files:
            bitstream += file_size_bit(file)

        # Convert bits back to characters (8 bits at a time)
        chars = []
        for i in range(0, len(bitstream), 8):
            byte = bitstream[i:i+8]
            if len(byte) == 8:
                chars.append(bits_to_char(byte))

        words.append("".join(chars))

    message = " ".join(words)
    print("Decoded message:")
    print(message)

if __name__ == "__main__":
    decode_message()