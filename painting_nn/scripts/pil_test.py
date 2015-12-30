from PIL import Image

im = Image.open('../images/D110.gif')
rgb_im = im.convert('RGB')
r, g, b = rgb_im.getpixel((1, 1))

print(str(im.size))

for i in range(0, 20):
	line = ''
	for j in range(0, 20):
		r, g, b = rgb_im.getpixel((i+1, j+1))
		line += str(r/255.0) + '\t'
	print(str(line.strip()))
