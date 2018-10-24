'''
This tool is for merge all bin as one file. Avoiding wasting of time at burning every bin one by one each time.
'''

from struct import pack
import os
from tqdm import tqdm,trange

__version__ = "0.1"
bin_map_info = []

#First step:
#Parsing config file, and get the file name\length and its start address in flash.
with open('address-map.ini') as config_file:
    try:
        for line in config_file.readlines():
            if not line.lstrip().startswith('#'):
                bin_map_info.append([line.split(',')[0].strip(), line.split(',')[1].strip(), line.split(',')[2].strip()])
    finally:
        config_file.close()
    
#print(bin_map_info)

#Creating a file which is filled by binary 1 and its size is the same with flash of DOT
with open('One-Entire-Image.bin', 'wb') as one_image:
    for i in trange(0xffffff):
        one_image.write(pack('B', 255))
    one_image.close()


#Second step:
#According to these infomations to get the related file and read out it as binary format.
#Then write its into the file which is deemed as the flash. Do it one by one.
pbar = tqdm(bin_map_info)
for item_bin in pbar:
    image_name, image_addr, image_len = item_bin
    pbar.set_description("Processing %s" % image_name)
    #print(image_name, image_addr, image_len)
    if not os.path.exists('full-loads/'+image_name):
        print("Warning: %s isn't exist!!!!" % ('full-loads/'+image_name))
        break
    
    file_size = os.path.getsize('full-loads/'+image_name)
    if (file_size > int(image_len, 16)):
        print("%s size(%x) greater than the reserved space(%x), failed!" % (image_name, file_size, int(image_len, 16)))
        break
    
    with open('full-loads/'+image_name, 'rb') as bin_F:
        bin_content = bin_F.read()
        bin_F.close()
        with open('One-Entire-Image.bin', 'rb+') as target_F:
            target_F.seek(int(image_addr, 16), 0)
            target_F.write(bin_content)
            target_F.flush()
            target_F.close()
            #print(" successed.")

os.system("pause")

'''
import pickle
F = open('One-Entire-Image.bin', 'wb')
pickle.dump('ff'*0xfff, F)
F.close()

S = open('One-Entire-Image.bin', 'rb')
E = pickle.load(S)
print(E)
'''


