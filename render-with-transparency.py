import numpy as np
import math
from PIL import Image
from imagesettings import *
folder = "."
colours = np.load(f"{folder}/output-colors-array.npy")
counts = np.load(f"{folder}/output-counts-array.npy")
coloursAvg = colours.reshape(height, hscale, width, hscale, 3).mean(axis = (1,3))
countsAvg = counts.reshape(height, hscale, width, hscale).astype(float).mean(axis = (1,3))
countMax = countsAvg.max()
alpha = np.vectorize(lambda x: math.log(x+1)/math.log(countMax+1))(countsAvg)
pixels = (np.clip(coloursAvg, 0,1)*255*alpha[:, :, None]**(1/gamma)).astype(np.uint8)
result = np.concatenate((pixels, (255*alpha.reshape(height, width, 1)).astype(np.uint8)), axis = 2)
# save as image
Image.fromarray(result, "RGBA").save("output-transparency.png")

