import string

ALPH = string.ascii_uppercase

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Decrypt with a given Caesar shift (encryption key)."""
    out = []
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            # subtract the shift to decrypt
            out.append(chr((ord(ch) - base - shift) % 26 + base))
        else:
            out.append(ch)
    return ''.join(out)

def brute_force(ciphertext: str):
    """Try all 26 shifts and print candidates."""
    for k in range(26):
        print(f"shift {k:2d}: {caesar_decrypt(ciphertext, k)}")

if __name__ == "__main__":
    ct = "XRPCTCRGNEI"
    print("Single known shift (15):", caesar_decrypt(ct, 15))  # -> ICANENCRYPT
    print("\nAll candidates:")
    brute_force(ct)

