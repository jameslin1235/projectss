
from PIL import Image
# im = Image.open("./static/img/avatar_original.jpg")
im = Image.open("./static/img/background_original.jpg")
# print(im.format, im.size, im.mode)
im.show()

width = im.width
height = im.height
aspect_ratio = width // height

small_width = 727
small_height = small_width // aspect_ratio
small_size = (small_width,small_height)

# medium_width = 125
# medium_height = medium_width // aspect_ratio
# medium_size = (medium_width,medium_height)
#
# large_width = 150
# large_height = large_width // aspect_ratio
# large_size = (large_width,large_height)


im.resize(small_size).save("./static/img/background_small.jpg")
# im.resize(medium_size).save("./static/img/avatar_medium.jpg")
# im.resize(large_size).save("./static/img/avatar_large.jpg")
