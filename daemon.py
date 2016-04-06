#!/usr/bin/env python
# encoding: utf-8

import atexit, os, sys, time
from signal import SIGTERM 


from color import Color

MSG_PID_EXISTE = 'Pidfile %s existe, demonio ejecutandose'
MSG_PID_NO_EXISTE = 'Pidfile %s no existe, el demonio no esta ejecutandose'

MSJ_STATUS = lambda service_name, status, msg_pid: 'Service \'{service_name}\' is {status}{msg_pid}'.format(service_name = service_name, status=status, msg_pid=msg_pid)

CODIGO_NO_SUCH_PROCESS = 3

class Daemon(object):
  def __init__(self, pidfile, **kwargs):
    self.pidfile = pidfile

  def daemonize(self):
    #atexit.register(self.borrar_pid)
    pid = str(os.getpid())
    with file(self.pidfile, 'w+') as f:
      f.write("%s\n" % pid)

  def borrar_pid(self):
    os.remove(self.pidfile)

  def status(self):
    try:
      pf = file(self.pidfile, 'r')
      pid = int(pf.read().strip())
      pf.close()
    except IOError:
      pid = None
    print Color.colorear(MSJ_STATUS(self.__str__(), 
      pid and 'running' or 'stopped', 
      pid and ' with pid: {pid}.'.format(pid=pid) or '.'), color=pid and Color.OKGREEN or Color.WARNING)

    sys.exit()

  def start(self):
    try:
      pf = file(self.pidfile, 'r')
      pid = int(pf.read().strip())
      pf.close()
    except Exception as e:
      pid = None

    if pid:
      print Color.colorear(MSG_PID_EXISTE % self.pidfile)
      sys.exit(1)

    # start the daemon
    self.daemonize()
    self.run()

  def stop(self):
    try:
      pf = file(self.pidfile, 'r')
      pid = int(pf.read().strip())
      pf.close()
    except IOError:
      pid = None

    if not pid:
      print Color.colorear(MSG_PID_NO_EXISTE % self.pidfile, color=Color.WARNING)
      return # no es error en 'restart'

    # Matar el demonio
    try:
      while 1:
        os.kill(pid, SIGTERM)
        time.sleep(0.1)
    except OSError, err:
      codigo_error, msg_error = err
      if codigo_error == CODIGO_NO_SUCH_PROCESS:
        if os.path.exists(self.pidfile):
          os.remove(self.pidfile)
      else:
        print Color.colorear(msg_error)
        sys.exit(1)

  def restart(self):
    self.stop()
    self.start()

  def run(self):
    """Sobreescribir este método"""