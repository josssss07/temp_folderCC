# Temporary-File Covert Channel (02_temp_cc)

This workspace contains a simple covert-communication demo that encodes a message into **file sizes** inside a temporary directory, and then decodes it back.

- Encoder: `encode.py`
- Decoder: `decode.py`
- Storage location: `/tmp/secret_store`

## How it works (high level)

- The encoder splits the input message into **words** (whitespace-separated).
- For each word, it creates a randomly named folder under `/tmp/secret_store/`.
- Each character is converted to 8 bits (ASCII) and written out as one file per bit.
- Bit representation uses **file size parity**:
  - bit `0` → file size is **even** (2 bytes)
  - bit `1` → file size is **odd** (1 byte)
- The decoder walks those folders, reconstructs the bitstream in numeric filename order, and converts each 8-bit chunk back to characters.

