# Dictionary mappings for encryption
dict1 = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14,
    "P": 15,
    "Q": 16,
    "R": 17,
    "S": 18,
    "T": 19,
    "U": 20,
    "V": 21,
    "W": 22,
    "X": 23,
    "Y": 24,
    "Z": 25,
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": 23,
    "y": 24,
    "z": 25,
}

dict2 = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J",
    10: "K",
    11: "L",
    12: "M",
    13: "N",
    14: "O",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",
    21: "V",
    22: "W",
    23: "X",
    24: "Y",
    25: "Z",
}


def encrypt(message, shift):
    """
    Encrypt string while preserving numbers and case.

    Args:
        message (str): The message to encrypt
        shift (int): The number of positions to shift each letter

    Returns:
        str: The encrypted message with preserved numbers and spacing

    Example:
        >>> encrypt("Hello 123 World!", 3)
        'Khoor 123 Zruog!'
    """
    cipher = ""
    if message:
        for char in message:
            # Preserve numbers
            if char.isdigit():
                cipher += char
            # Preserve spaces and punctuation
            elif char not in dict1:
                cipher += char
            # Encrypt letters
            else:
                # Get the shifted position
                num = (dict1[char] + shift) % 26
                # Preserve case
                if char.isupper():
                    cipher += dict2[num]
                else:
                    cipher += dict2[num].lower()
    
    return cipher


def decrypt(cipher, shift):
    """
    Decrypt string while preserving numbers and case.

    Args:
        cipher (str): The encrypted message
        shift (int): The number of positions used in encryption

    Returns:
        str: The decrypted message with preserved numbers and spacing

    Example:
        >>> decrypt("Khoor 123 Zruog!", 3)
        'Hello 123 World!'
    """
    return encrypt(cipher, -shift)
