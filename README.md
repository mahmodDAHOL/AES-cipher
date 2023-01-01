### Advanced Encryption Standard (AES):
 is a specification for the encryption of electronic data established by the U.S National Institute of Standards and Technology (NIST) in 2001. AES is widely used today as it is a much stronger than DES and triple DES despite being harder to implement.

#### Block Ciphers:
AES is a block cipher, which just means it operates on blocks of text that are a fixed size — AES has specifically chosen a block size of 128 bits, or 16 bytes. However, it supports keys of either 128, 192, or 256 bits (16, 24, or 32 bytes respectively). The secret key is the piece of information shared with both parties — the ones encrypting and the ones decrypting.
Of course, not every string that we need to encode is cleanly divisible into 16-byte blocks

#### Initialization vector (IV):

An initialization vector (or IV) are used to ensure that the same value encrypted multiple times, even with the same secret key, will not always result in the same encrypted value. This is an added security layer. If strings did always have the same result when encrypted, it would be easier for someone to figure out what the starting value was just through brute force trial and error.


#### Modes:

Other than the encryption key and the initialization vector, the other thing you’ll notice about the initialization of the cipher, is that we’ve passed in a mode. The mode defines which algorithm is used to encrypt the data. Some provide a higher level of security/randomness than others, but the main thing here is to use the mode of encryption that will be used for decryption on the other side.


#### Padding:

When we actually call encrypt on our cipher (which has been initialized with the encryption key, encryption mode, and initialization vector), you’ll notice we’re also calling pad on the value we’re encrypting first. This goes back to the concept of “block size” that we talked about earlier. Because AES is a block cipher that works on “blocks” of a predefined length, if the value we’re encrypting isn’t cleanly divisible by that length, it won’t work. Calling pad on the value adds empty bytes to the end of your string until it’s the correct number of bytes long. It returns a byte string,


