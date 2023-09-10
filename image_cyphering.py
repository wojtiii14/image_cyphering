from PIL import Image
import random
import os
import numpy as np

# Function shuffling the image pixels

def shuffleImage(im, seed=42):
    # Get pixels and put in Numpy array for easy shuffling
    pix = np.array(im.getdata())

    # Generate an array of shuffled indices
    # Seed random number generation to ensure same result
    np.random.seed(seed)
    indices = np.random.permutation(len(pix))

    # Shuffle the pixels and recreate image
    shuffled = pix[indices].astype(np.uint8)
 
    return Image.fromarray(shuffled.reshape(im.width,im.height,3))

# Function unshuffling the image pixels

def unshuffleImage(im, seed=42):

    # Get shuffled pixels in Numpy array
    shuffled = np.array(im.getdata())
    nPix = len(shuffled)

    # Generate unshuffler
    np.random.seed(seed)
    indices = np.random.permutation(nPix)
    unshuffler = np.zeros(nPix, np.uint32)
    unshuffler[indices] = np.arange(nPix)

    unshuffledPix = shuffled[unshuffler].astype(np.uint8)
    return Image.fromarray(unshuffledPix.reshape(im.width,im.height,3))

# Deleting existing results

for file in os.listdir():
    if file == 'cactus_before.jpg':
        os.remove(file)
    elif file == 'cactus_after.jpg':
        os.remove(file)
    else:
        continue

# Loading random values to the tables

random_table = []

for x in range(256):
    random_table.append(random.randint(0, 255))

random_table1 = []

for x in range(256):
    random_table1.append(random.randint(0, 255))

random_table2 = []

for x in range(256):
    random_table2.append(random.randint(0, 255))

# Loading SBOX values to the table

with open('sbox_08x08_20130110_011319_02.SBX', 'rb') as  file:
    sbox = file.read()
    
    counter = 0
    all_bytes = []
    
    for byte in sbox:
        if counter % 2 == 0:
            all_bytes.append(byte)
        counter += 1

img = Image.open('cactus.jpg')
pix = img.load()

# Encrypting

counter = 0

for x in range(img.size[0]):
    for y in range(img.size[1]):
        [r, g, b]=img.getpixel((x, y))

        if(counter == 255):
            counter = 0
        else:
            counter = counter + 1

        r = r ^ all_bytes[random_table[counter]]
        g = g ^ all_bytes[random_table1[counter]]
        b = b ^ all_bytes[random_table2[counter]]
        
        value = (r, g, b)
        img.putpixel((x, y), value)

img = shuffleImage(img)

img.save('cactus_after.jpg')

# Decrypting

img = unshuffleImage(img)

counter = 0

for x in range(img.size[0]):
    for y in range(img.size[1]):
        [r, g, b]=img.getpixel((x, y))

        if(counter == 255):
            counter = 0
        else:
            counter = counter + 1

        r = r ^ all_bytes[random_table[counter]]
        g = g ^ all_bytes[random_table1[counter]]
        b = b ^ all_bytes[random_table2[counter]]
        
        value = (r, g, b)
        img.putpixel((x, y), value)

img.save('cactus_before.jpg')
