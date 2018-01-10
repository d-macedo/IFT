from PIL import Image 
image_file = Image.open("glasses.jpeg") # open colour image
image_file = image_file.convert('L') # convert image to black and white
image_file.save('result.jpg')