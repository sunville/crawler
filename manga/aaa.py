#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import codecs
from PIL import Image, ImageFile
from io import BytesIO

url = 'http://cartoon.youzu88.com/manhuatuku/3105/manhua_12_20160401_2016040107503361822.jpg'
path = '/Users/tony/Desktop/reptile/test.jpg'

r = requests.get(url)
img = Image.open(BytesIO(r.content))
print img.size[1]
# try:
# 	print img.size[0]
# 	img.save(path, "JPEG", quality=80, optimize=True, progressive=True)
# except IOError:
# 	print img.size[0]
# 	PIL.ImageFile.MAXBLOCK = img.size[0] * img.size[1]
# 	img.save(path, "JPEG", quality=80, optimize=True, progressive=True)
