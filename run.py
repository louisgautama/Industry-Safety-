import os
import cv2

print("Opening Camera")

os.system("python detect.py --weights best.pt --img 416 --conf 0.5 --source 0")


         