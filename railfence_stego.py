from PIL import Image

# -------- Rail Fence Cipher --------
def rail_fence_encrypt(text, rails):
    rail = [''] * rails
    row, step = 0, 1
    for ch in text:
        rail[row] += ch
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    return ''.join(rail)

def rail_fence_decrypt(cipher, rails):
    pattern = [['\n' for _ in range(len(cipher))] for _ in range(rails)]
    row, step = 0, 1
    for i in range(len(cipher)):
        pattern[row][i] = '*'
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    index = 0
    for i in range(rails):
        for j in range(len(cipher)):
            if pattern[i][j] == '*' and index < len(cipher):
                pattern[i][j] = cipher[index]
                index += 1
    result = []
    row, step = 0, 1
    for i in range(len(cipher)):
        result.append(pattern[row][i])
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    return ''.join(result)

# -------- LSB Steganography --------
def embed_in_lsb(image_path, message, output_path):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    message += '###'  # end marker
    binary = ''.join(format(ord(i), '08b') for i in message)
    data_index = 0

    for x in range(width):
        for y in range(height):
            if data_index >= len(binary):
                break
            pixel = list(img.getpixel((x, y)))
            for n in range(3):
                if data_index < len(binary):
                    pixel[n] = pixel[n] & ~1 | int(binary[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
        if data_index >= len(binary):
            break
    encoded.save(output_path)
    print(f"Stego image saved as: {output_path}")

def extract_from_lsb(image_path):
    img = Image.open(image_path)
    binary = ''
    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            for n in range(3):
                binary += str(pixel[n] & 1)
    all_bytes = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for byte in all_bytes:
        message += chr(int(byte, 2))
        if message[-3:] == '###':
            break
    return message[:-3]

# -------- Main Menu --------
def main():
    while True:
        print("\n--- Rail Fence Cipher + Image Stego ---")
        print("1. Encrypt and Embed")
        print("2. Extract and Decrypt")
        print("3. Exit")
        ch = input("Enter your choice: ")

        if ch == '1':
            msg = input("Enter message: ")
            rails = int(input("Enter number of rails: "))
            img_path = input("Enter image path (e.g., logo.png): ")
            out_path = "stego.png"

            cipher = rail_fence_encrypt(msg, rails)
            print(f"Ciphertext: {cipher}")
            embed_in_lsb(img_path, cipher, out_path)

        elif ch == '2':
            img_path = input("Enter stego image path (e.g., stego.png): ")
            rails = int(input("Enter number of rails used: "))
            cipher = extract_from_lsb(img_path)
            print(f"Extracted Cipher: {cipher}")
            print("Decrypted Message:", rail_fence_decrypt(cipher, rails))

        elif ch == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
