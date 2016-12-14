import os
import sys
import math
from PIL import Image
from numpy import array
import numpy as np

cover_image_path = 'mares.bmp'
secret_image_path = 'lena.bmp'
steg_image_path = 'steg.bmp'
num_sb = 4

def get_clear_mask(num_sb):
	clear_mask = 255 - (1 << num_sb) + 1
	return clear_mask

def get_get_mask(num_sb):
	get_mask = (1 << num_sb) - 1
	return get_mask

def check_capacity(cover_image, secret_image):
	capacity = len(cover_image)*len(cover_image[0])*len(cover_image[0][0])
	if (capacity < (len(secret_image)*len(secret_image[0])*len(secret_image[0][0])*8 + 32*3)/num_sb):
		print('Cover image too small. Only able to hide', capacity*num_sb/8, 'bytes.')
		print('Use larger cover image or increment number of least significant bits.')
		sys.exit()

def embed():
	cover_image = array(Image.open(cover_image_path))
	secret_image = array(Image.open(secret_image_path))
	check_capacity(cover_image, secret_image)

	clear_mask = get_clear_mask(num_sb)
	get_mask = get_get_mask(num_sb)

	d1 = len(cover_image)
	d2 = len(cover_image[0])
	d3 = len(cover_image[0][0])

	s_d1 = len(secret_image)
	s_d2 = len(secret_image[0])
	s_d3 = len(secret_image[0][0])

	cover_byte_index = 0
	# Embedding secret image dimensions
	for i in range(32/num_sb):
		cover_image[cover_byte_index/(d2*d3)][cover_byte_index%(d2*d3)/d3][cover_byte_index%d3] = cover_image[cover_byte_index/(d2*d3)][cover_byte_index%(d2*d3)/d3][cover_byte_index%d3] & clear_mask | (s_d1 & get_mask)
		s_d1 = s_d1 >> num_sb
		cover_byte_index += 1

	for i in range(32/num_sb):
		cover_image[cover_byte_index/(d2*d3)][cover_byte_index%(d2*d3)/d3][cover_byte_index%d3] = cover_image[cover_byte_index/(d2*d3)][cover_byte_index%(d2*d3)/d3][cover_byte_index%d3] & clear_mask | (s_d2 & get_mask)
		s_d2 = s_d2 >> num_sb
		cover_byte_index += 1

	for i in range(32/num_sb):
		cover_image[cover_byte_index/(d2*d3)][cover_byte_index%(d2*d3)/d3][cover_byte_index%d3] = cover_image[cover_byte_index/(d2*d3)][cover_byte_index%(d2*d3)/d3][cover_byte_index%d3] & clear_mask | (s_d3 & get_mask)
		s_d3 = s_d3 >> num_sb
		cover_byte_index += 1

	# Embedding secret image content
	for i in range(len(secret_image)):
	    for j in range(len(secret_image[0])):
	    	for k in  range(len(secret_image[0][0])):
		    	for part in range(8/num_sb):
		    		cover_image[cover_byte_index/(d2*d3)][cover_byte_index%(d2*d3)/d3][cover_byte_index%d3] = cover_image[cover_byte_index/(d2*d3)][cover_byte_index%(d2*d3)/d3][cover_byte_index%d3] & clear_mask | (secret_image[i][j][k] & get_mask)
		    		secret_image[i][j][k] = secret_image[i][j][k] >> num_sb
		    		cover_byte_index += 1

	img_out = Image.fromarray(cover_image)
	img_out.save('steg.bmp')


def recover():
	steg_image = array(Image.open(steg_image_path))
	clear_mask = get_clear_mask(num_sb)
	get_mask = get_get_mask(num_sb)
	steg_byte_index = 0

	d1 = len(steg_image)
	d2 = len(steg_image[0])
	d3 = len(steg_image[0][0])

	s_d1 = 0
	for i in range(32/num_sb):
		s_d1 |= (steg_image[steg_byte_index/(d2*d3)][steg_byte_index%(d2*d3)/d3][steg_byte_index%d3] & get_mask) << (i*num_sb);
		steg_byte_index += 1

	s_d2 = 0
	for i in range(32/num_sb):
		s_d2 |= (steg_image[steg_byte_index/(d2*d3)][steg_byte_index%(d2*d3)/d3][steg_byte_index%d3] & get_mask) << (i*num_sb);
		steg_byte_index += 1

	s_d3 = 0
	for i in range(32/num_sb):
		s_d3 |= (steg_image[steg_byte_index/(d2*d3)][steg_byte_index%(d2*d3)/d3][steg_byte_index%d3] & get_mask) << (i*num_sb);
		steg_byte_index += 1

	for i in range(s_d1):
		for j in range(s_d2):
			for k in range(s_d3):
				cur = 0
				for part in range(8/num_sb):
					cur |= (steg_image[steg_byte_index/(d2*d3)][steg_byte_index%(d2*d3)/d3][steg_byte_index%d3] & get_mask) << (part*num_sb)
					steg_byte_index += 1
				steg_image[i][j][k] = cur

	img_out = Image.fromarray(steg_image)
	img_out.save('secret.bmp')



