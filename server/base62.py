ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = 62
CODE_LEN = 9
CHAR_TO_VALUE = {c: i for i, c in enumerate(ALPHABET)}


def encode(ip: str, port: int):
    parts = ip.split(".")  # ["192", "168", "1", "42"]
    parts = [int(x) for x in parts]  # [192, 168, 1, 42]
    n = (parts[0] << 40) | (parts[1] << 32) | (parts[2] << 24) | (parts[3] << 16) | port

    chars = []
    for _ in range(CODE_LEN):
        chars.append(ALPHABET[n % BASE])
        n //= BASE

    return "".join(
        chars
    )  # ['i', 'k', 'X', '3', 'a', 'P', 'm', 'n', 'o'] -> "ikX3aPmno"


def decode(code: str) -> tuple[str, int]:
    n = 0
    base_power = 1
    for c in code:
        n += CHAR_TO_VALUE[c] * base_power
        base_power *= BASE

    port = n & 0xFFFF
    octet4 = (n >> 16) & 0xFF
    octet3 = (n >> 24) & 0xFF
    octet2 = (n >> 32) & 0xFF
    octet1 = (n >> 40) & 0xFF
    ip = f"{octet1}.{octet2}.{octet3}.{octet4}"
    return ip, port
