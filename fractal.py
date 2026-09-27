import os
mothApiKey = os.environ['MOTH_API_KEY']

import requests, time
def quantumSeed():
    httpsAPI = "https://api.mothquantum.com/api/v1"
    authHeader = {"Authorization": f"Bearer {mothApiKey}"}
    job = requests.post(
            f"{httpsAPI}/engines/comet-qrng-v1/process",
            headers = authHeader,
            json = {
                "params": {
                    "num_qubits": 12, # width of the randomness register
                    "shots": 4096, # The number of the register is measured from |+>
                    "mode": "emu", # Use the emulator backend
                    "bell_witness": True,
                    "output_bytes": 32,
                }
            }).json()
    # poll job until completed/failed/cancelled
    while True:
        st = requests.get(f"{httpsAPI}/jobs/{job['job_id']}/status", headers = authHeader).json()
        #print(st)
        if st["status"] in ("completed", "failed", "cancelled"):
            break
        time.sleep(1)
    # get result
    if st["status"]!= "completed":
          raise RuntimeError(f"job {st['status']}: {st['error']}")
    res = requests.get(f"{httpsAPI}/jobs/{job['job_id']}/result", headers = authHeader).json()
    return res["result"]["output"]["random"]["hex"] 
        
print("asking quantum computer for seed")
seed = quantumSeed() 
import random
random.seed(seed)

import numpy as np
import math
from PIL import Image
from statistics import mean

from imagesettings import *

outputscale = 0.75
outputdx, outputdy = -0.0, 0.2

counts = np.zeros((height*hscale, width*hscale), dtype = int)
colours = np.zeros((height*hscale, width*hscale, 3), dtype = float)

# draw fractal flame
print("Drawing")
samples = width*height* 5
pos = [0, 0]
pointColour = np.array([1,1,1])
import variations as va
def makeFlameFunction(weights, linear, translation, variations):
    return lambda x : sum([w*v(np.matmul(linear, x) + translation) for (w, v) in zip(weights, variations)])
flameFunctions = [makeFlameFunction([1, 0.1], np.array([[0.4, 0.],[0., 0.4]]), np.array([-0.3, -0.3]), [va.linear, va.spiral]),
                  makeFlameFunction([1, 0.1], np.array([[0.5, 0.],[0., 0.5]]), np.array([-1/2, 1/2]),[va.linear, va.spiral]),
                  makeFlameFunction([1, 0.1], np.array([[0.5, 0.],[0., 0.5]]), np.array([1/2, -1/2]),[va.linear, va.spiral]),
                  makeFlameFunction([1/6, 5/6], np.array([[0.5, 0.],[0., 0.5]]), np.array([1/2, 1/2]), [va.heart, va.linear]),
                  makeFlameFunction([1/2, 1/2], np.array([[0.5, 0.],[0., 0.5]]), np.array([0, 0]), [va.swirl, va.linear]),
                  #makeFlameFunction([2/3, 1/3], np.array([[0.05, -0.1], [0.05,-0.1]]), np.array([0.08,-0.25]), [va.linear, va.spherical])
                  makeFlameFunction([2/3, 1/3], np.array([[0.1, -0.2], [0.1,-0.2]]), np.array([0.08,-0.25]), [va.hyperbolic, va.spherical]),
                  makeFlameFunction([4/5,1/5], np.array([[1, -0.05], [0.05,1]]), np.array([0.0,0.0]), [va.polar, va.disc]),
                  ]
probabilities = [0.75/5 for i in range(5)] + [0.2, 0.05]
flameColour = np.array([[0.5, 0, 1], [0.5, 0, 1] , [1, 0, 0], [0.5,0,1], [1,0,0], [0, 1, 1], [0,0.5,1]])
assert len(flameColour) == len(flameFunctions) == len(probabilities)
for sample in range(samples):
    p = random.random()
    i = 0
    while i< len(probabilities)-1 and p > probabilities[i]:
        p -= probabilities[i]
        i += 1
    pos = flameFunctions[i](pos)
    pointColour = (pointColour+flameColour[i])/2
    # pos to pixel coordinates
    x =int( ((pos[0]+outputdx)*outputscale)*(height*hscale)/2 + width*hscale/2)
    y =int( ((pos[1]+outputdy)*outputscale+1)*(height*hscale)/2 )
    if(0<=x<width*hscale and 0<= y < height*hscale):
        counts[y,x] += 1
        colours[y,x, :] = (colours[y,x,:]+ pointColour)/2

# render
np.save("./output-colors-array.npy", colours)
np.save("./output-counts-array.npy", counts)
coloursAvg = colours.reshape(height, hscale, width, hscale, 3).mean(axis = (1,3))
countsAvg = counts.reshape(height, hscale, width, hscale).astype(float).mean(axis = (1,3))
countMax = countsAvg.max()
alpha = np.vectorize(lambda x: math.log(x+1)/math.log(countMax+1))(countsAvg)
pixels = (np.clip(coloursAvg, 0,1)*255*alpha[:, :, None]**(1/gamma)).astype(np.uint8)
# save as image
Image.fromarray(pixels, "RGB").save("output.png")











