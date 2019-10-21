#!/usr/bin/env python3

from PIL import Image

import pyocr
import pyocr.builders

import av
import av.filter

import sys
import argparse
import json

def read_video(filename, delta=1, max=200):
  container = av.open(filename)
  stream = container.streams.video[0]

  last = -1
  for frame in container.decode(stream):
    t = frame.time
    if int(t) != last:
      yield(frame)
      last = int(t)
    if t >= max:
      break

# TODO:
# - put this into a class
# - use multiprocessing Queue?
# - automatically compute region for item text
# - why is tesseract slow?
# - pass crop region on command line
# - also OCR ammo counts
# - use PSM 7 (single line)
# - use OEM 1 (OCR engine mode neural nets only)
# - use PIL ImageStat to decide whether to OCR
def process(frame, tool, lang, **kwargs):
  image = frame.to_image()
  game_region = image.crop((320, 0, 1280, 720))
  item_region = game_region.crop((184, 360, 184+568, 360+72))
  # item_region = game_region.crop((184, 332, 184+568, 432))
  # item_region = game_region.crop((184, 332, 184+568, 464))
  # print(item_region.histogram())
  # item_region.save('t/t%d.png' % int(frame.time))
  try:
    builder = pyocr.builders.TextBuilder(**kwargs)
    item_text = tool.image_to_string(item_region, lang=args.ocr_lang,
        builder=builder)
  except pyocr.error.PyocrException:
    pass
  # try:
  #   builder = pyocr.builders.WordBoxBuilder(**kwargs)
  #   boxes = tool.image_to_string(item_region, lang=args.ocr_lang,
  #       builder=builder)
  # except pyocr.error.PyocrException:
  #   pass
  # print([dir(box) for box in boxes])
  # print([box.content for box in boxes])
  # print([box.position for box in boxes])
  return { 'time': frame.time, 'item': item_text }
  # return { 'time': frame.time, 'item': item_text, 'contents':
  #     [ box.content for box in boxes ], 'positions': [ box.position for
  #     box in boxes ] }

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='TODO')
  parser.add_argument('--ocr-tool', type=str, default='libtesseract')
  parser.add_argument('--ocr-lang', type=str, default='eng')
  parser.add_argument('filename', type=str)
  args = parser.parse_args()

  tool = getattr(pyocr, args.ocr_tool)
  lang = args.ocr_lang

  # reading video: 200/45s
  # to image: 200/63s
  # crop: 200/58s
  # crop2: 200/77s
  # ocr: 200/150s

  # PSM modes (time is for first 200 seconds):
  # 5 - 2m58s
  # 7 - 2m36s
  # 11 - 2m27s
  # 12 - 4m54s
  # 13 - 3m6s
  # TODO: none of these are performing very well and I don't know why -
  # did I get the image bounds wrong?

  # TODO: not sure if oem 1 is any faster or not than the default (which
  # I think is 3?).  Why can't I use 0?
  # TODO: is PSM 13 any good?
  # TODO: I think libtesseract is faster than tesseract even though we
  # can specify OEM with tessaract but not libtesseract.
  # TODO: Reusing the same builder each time means we are appending to
  # the string.

  for frame in read_video(args.filename):
    # print(frame.time, frame.time_base, frame)
    data = process(frame, tool=tool, lang=lang, tesseract_layout=7)
    print(json.dumps(data))
