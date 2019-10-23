TODO
----

* Create a class for processing frames; this could make it easier to
  support other OCR engines
* use multiprocessing Queue so we can decode and OCR on separate cores
* automatically compute region for item text
* pass crop region on command line
* also OCR ammo counts in addition to items
* use PIL ImageStat to decide whether to OCR (i.e. only if there is a
  black rectangle on the screen)
* limit characters to A-Z
  * https://stackoverflow.com/questions/2363490/limit-characters-tesseract-is-looking-for
  * https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00#fine-tuning-for--a-few-characters
  * Possible fonts to use for training:
    * https://www.fontspace.com/codeman38/kongtext
    * https://www.fontspace.com/codeman38/press-start
    * https://www.fontspace.com/codeman38/press-start-2p
    * https://fontstruct.com/fontstructions/show/648782/super_metroid_menu

