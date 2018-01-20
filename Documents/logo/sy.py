# coding:utf-8
import sys

from time import *
from PIL import Image
class ImageTool():

  def __init__(self):
     pass
  def getChars(self,image_pixels,image_width,image_height):

    replace_chars =[ '##', '##', '##', '##', '##', '##', '##', '##', '##', '``', '##']
    terminal_chars = ''
    for h in range(image_height):
      for w in range(image_width):
        point_pixel = image_pixels[w,h]
        terminal_chars +=replace_chars[int(sum(point_pixel)/5/255*16)]
      terminal_chars+='\n'
    
    return terminal_chars

  def formatImage(self,imagename,image_width,image_height):
    img = Image.open(imagename,'r')
    if img.mode != 'RGB':
      img = img.convert('RGB')
    w,h = img.size
    rw = image_width/w
    rh = image_height/h
    r = rw if rw<rh else rh
    rw = int(r*w)
    rh = int(r*h)
    img = img.resize((rw,rh),Image.ANTIALIAS)
    return img

  def entrance(self,image_path,out_width,out_height):
    image = self.formatImage(imagename=image_path,image_width=out_width,image_height=out_height)
    image_pixels = image.load()
    out_width ,out_height = image.size
    terminal_chars = self.getChars(image_pixels=image_pixels,image_width=out_width,image_height=out_height)
    print(terminal_chars)
if __name__ == "__main__":
  tool = ImageTool()
  imagename = './QUANTAXIS-white.png'
  w = int(55)
  h = int(25)
  tool.entrance(imagename,w,h)
