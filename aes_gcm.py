import os
import sys
import scrypt
from Crypto.Cipher import AES


class encryptFile():
    def __init__(self, filename, password):
        self.filename = filename
        self.password = password

    def encrypt(self):
        data = open(self.filename, 'rb').read()
        key = scrypt.hash(self.password, "")[:32]  # N=16384, r=8, p=1
        nonce = os.urandom(32)
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        ciphertext = cipher.encrypt(data)
        ciphertext = nonce + ciphertext
        open('output.txt', 'wb').write(ciphertext)
        return ciphertext


class decryptFile():
    def __init__(self, filename, password):
        self.filename = filename
        self.password = password

    def decrypt(self):
        nonce_and_data = open(self.filename, 'rb').read()
        nonce = nonce_and_data[:32]
        data = nonce_and_data[32:]
        key = scrypt.hash(self.password, "")[:32]
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        plaintext = cipher.decrypt(data)
        open('output2.txt', 'wb').write(plaintext)
        return plaintext

    def test_decrypt(self, ciphertext):
        nonce_and_data = open(self.filename, 'rb').read()
        nonce = nonce_and_data[:32]
        data = nonce_and_data[32:]
        key = scrypt.hash(self.password, "")[:32]
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        plaintext = cipher.decrypt(data)
        return plaintext


password = sys.argv[2]
input_file = sys.argv[3]
if len(sys.argv) >= 5:
    output_file = sys.argv[4]
else:
    output_file = input_file


if sys.argv[1] == '-e':
    password_check = input('Re-enter your password : ')
    if password_check != password:
        print('Passwords does not match')
        sys.exit(1)

    encrypt_file = encryptFile(input_file, password)
    ciphertext = encrypt_file.encrypt()
    print(f'File {input_file} successfully encrypted in {output_file}')

elif sys.argv[1] == '-d':
    decrypt_file = decryptFile(input_file, password)
    plaintext = decrypt_file.decrypt()
    print(plaintext)
    print(f'File {input_file} successfully decrypted in {output_file}')

else:
    print('Error...')
