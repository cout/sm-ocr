#!/usr/bin/env python3

from tesserocr import PyTessBaseAPI, PSM, OEM

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
def process(frame, api, **kwargs):
  image = frame.to_image()
  api.SetImage(image)
  api.SetRectangle(320+184, 360, 568, 72)
  item_text = api.GetUTF8Text().strip()
  return { 'time': frame.time, 'item': item_text }

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='TODO')
  parser.add_argument('filename', type=str)
  args = parser.parse_args()

  with PyTessBaseAPI(psm=PSM.SINGLE_LINE, oem=OEM.LSTM_ONLY) as api:
    for frame in read_video(args.filename):
      # print(frame.time, frame.time_base, frame)
      data = process(frame, api)
      print(json.dumps(data))
