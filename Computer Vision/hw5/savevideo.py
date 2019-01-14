
import cv2
import os
import imageio

images = []


elems = []
directory = "optical_flows"
for root, dirs, files in os.walk(directory):
    files = sorted(files, key=lambda x: int(x[:-4]))
    for file in files:
        if file.endswith(".jpg"):
            img = cv2.imread(os.path.join(root, file))
            elems.append(img)


imageio.mimsave('flow.gif', elems)
