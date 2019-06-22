#!/usr/bin/python

import os, random
import getpass
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = "(encrypted)"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize)
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename[11:]

	with open(filename, 'rb') as infile:
		filesize = long(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)


def getKey(password):
	hasher = SHA256.new(password)
	return hasher.digest()

def Main():
	os.system('clear')
	print " _____        _____                  _   "
	print "|  __ \      / ____|                | |  "
	print "| |__) |   _| |     _ __ _   _ _ __ | |_ "
	print "|  ___/ | | | |    | '__| | | | '_ \| __|"
	print "| |   | |_| | |____| |  | |_| | |_) | |_ "
	print "|_|    \__, |\_____|_|   \__, | .__/ \__|"
        print "        __/ |             __/ | |        "
        print "       |___/             |___/|_|        "
        print "                                 elkoyote"


	choice = raw_input("Would you like to (E)ncrypt or (D)ecrypt?: ")

	if choice == 'E':
		filename = raw_input("File to encrypt: ")
		password = getpass.getpass("Password: ")
		encrypt(getKey(password), filename)
		print "Done."
	elif choice == 'D':
		filename = raw_input("File to decrypt: ")
		password = getpass.getpass("Password: ")
		decrypt(getKey(password), filename)
		print "Done."
	else:
		print "No Option selected, closing..."

if __name__ == '__main__':
	Main()
