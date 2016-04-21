#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

### INTEGRACION Django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracking.settings")

###


import logging
import logging.handlers
import time

from django import db
from django.conf import settings
from django.core.management.color import color_style
from django.db import transaction

from daemon import Daemon

# =-=-=-=-=-=-=-=-=-=-=-=-=-=- COLORES
style = color_style()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-
ARCHIVO_LOG = 'mdirectorlog.log'

# =-=-=-=-=-=-=-=-=-=-=-=-=-=- MENSAJES
MSJ_INICIANDO_SERV = style.HTTP_INFO('Iniciando servicio de actualizacion de MDirector.')
MSJ_TERMINANDO_SERV = style.HTTP_INFO('Terminando servicio de actualizacion de MDirector.')
MSJ_ERROR_SERV = style.ERROR('Ocurrio un error en el servicio: %s.')

# =-=-=-=-=-=-=-=-=-=-=-=-=-=- LOGGER
logger = logging.getLogger('%s.%s' % ('mdirector', __name__))
handler = logging.handlers.RotatingFileHandler(ARCHIVO_LOG, maxBytes=10000000, backupCount=20)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s - %(message)s')

logger.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

############### Daemon #####################


class MDirectorDaemon(Daemon):
  def __init__(self, pidfile, tiempo_ejecucion=900):
    self.tiempo_ejecucion = tiempo_ejecucion
    super(MDirectorDaemon, self).__init__(pidfile)

  def run(self):
  	from track.models import URLAccount
  	from mdirector.views import update_campaigns, update_delivery, update_statsdelivery
  	url_account = URLAccount.objects.filter(active=True, _client_key_md__isnull=False, _client_secret_md__isnull=False)
  	for url in url_account:
  		update_campaigns(url)
  		update_delivery(url)
      update_statsdelivery(url)





if __name__=='__main__':

  try:
    demonio = MDirectorDaemon('/var/run/mdirectorlog.pid')
    args = sys.argv

    if len(args) == 2:
      if args[1] == 'start':
        logger.info(MSJ_INICIANDO_SERV)
        demonio.start()
      elif args[1] == 'stop':
        logger.info(MSJ_TERMINANDO_SERV)
        demonio.stop()
      elif args[1] == 'restart':
        demonio.restart()
      elif args[1] == 'status':
        demonio.status()
      else:
        print style.ERROR('Opción no válida')
        sys.exit(2)

      sys.exit(0)
    else:
      sys.exit(2)

  except Exception, e:
    logger.error(MSJ_ERROR_SERV % unicode(e))
    sys.exit(1)