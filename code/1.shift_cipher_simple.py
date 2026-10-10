# shift_cipher_simple.py
# A simple shift (Caesar) cipher.
# Chapter 1 - Practical Cryptography in Python (Nielson & Monson)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def make_tables(shift):
    encode_table = {}
    decode_table = {}
    for i in range(26):
        plain = ALPHABET[i]
        cipher = ALPHABET[(i + shift) % 26]
        encode_table[plain] = cipher
        decode_table[cipher] = plain
    return encode_table, decode_table


def convert(message, table):
    result = ""
    for letter in message.upper():
        if letter in table:
            result = result + table[letter]
        else:
            result = result + letter
    return result


def show_table(table):
    top = ""
    bottom = ""
    for letter in sorted(table):
        top = top + letter + " "
        bottom = bottom + table[letter] + " "
    print(top)
    print(bottom)


if __name__ == "__main__":
    shift = 1
    encode_table, decode_table = make_tables(shift)

    while True:
        print()
        print("SHIFT CIPHER   (current shift =", shift, ")")
        print("1. Show the tables")
        print("2. Encode a message")
        print("3. Decode a message")
        print("4. Change the shift")
        print("5. Quit")

        choice = input(">> ")

        if choice == "1":
            print("Encoding table:")
            show_table(encode_table)
            print("Decoding table:")
            show_table(decode_table)

        elif choice == "2":
            message = input("Message to encode: ")
            print("Encoded:", convert(message, encode_table))

        elif choice == "3":
            message = input("Message to decode: ")
            print("Decoded:", convert(message, decode_table))

        elif choice == "4":
            answer = input("New shift (1 to 25): ")
            if answer.isdigit() and 1 <= int(answer) <= 25:
                shift = int(answer)
                encode_table, decode_table = make_tables(shift)
                print("Shift is now", shift)
            else:
                print("Please type a whole number from 1 to 25.")

        elif choice == "5":
            print("Bye!")
            break

        else:
            print("Sorry, I do not know option", choice)
