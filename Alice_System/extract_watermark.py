def extract_watermark(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        print("❌ File not found.")
        return

    print("✅ File loaded.")

    zero_width_chars = [c for c in content if c in ('\u200B', '\u200C')]

    if not zero_width_chars:
        print("❌ No watermark found.")
        return

    binary_string = ''.join('0' if c == '\u200B' else '1'
                            for c in zero_width_chars)

    chars = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    decoded_text = ''.join(chr(int(b, 2)) for b in chars)

    print("✅ Extracted Payload:")
    print(decoded_text)

    try:
        user_id, timestamp, signature = decoded_text.split("|")
        print("User ID:", user_id)
        print("Timestamp:", timestamp)
        print("Signature:", signature)
    except:
        print("⚠ Payload parsing failed.")


if __name__ == "__main__":
    print("=== Watermark Extraction Tool ===")
    file_name = input("Enter leaked file name: ").strip()
    extract_watermark(file_name)