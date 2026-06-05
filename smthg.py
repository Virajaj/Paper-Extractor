from PIL import Image

# load your jpeg image
img = Image.open("icon.jpeg")

# convert & save as ico
img.save("icon.ico", format="ICO", sizes=[(256, 256)])