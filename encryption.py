from cryptography.fernet import Fernet

key = b'pfNKJcuwfI0ld-gRV5Ta_nzPb2S8rJBKXV10zTb6rq4='

cipher_suite = Fernet(key)
ciphered_text = b'gAAAAABeHHxs-Q_rgRuGjFJdkrzxu1HHEqPQzsCdzrFzW95WhQlZG5gm7HIbEFlXS5NhzdMV3-1-2X4d6LXo5BS08mfoGNqYgQ=='

unciphered_text = (cipher_suite.decrypt(ciphered_text))


print(unciphered_text)