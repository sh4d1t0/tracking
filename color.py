# encoding: utf-8

class Color(object):
  HEADER  = '\033[95m'
  OKBLUE  = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL    = '\033[91m'
  ENDC    = '\033[0m'

  def colorear(txt, color=None):
    color = not color and Color.FAIL or color
    return '%s%s%s' % (color, txt, Color.ENDC)

  colorear = staticmethod(colorear)