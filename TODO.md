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
