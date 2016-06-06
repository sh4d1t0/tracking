from django.conf import settings

from pymongo import MongoClient
from pymongo.errors import AutoReconnect#, OperationFailure, ConnectionFailure

class MongoDB(object):
  #def __init__(self, *args, **kwargs):
  def __init__(self, username=None, password=None, source=None, *args, **kwargs):
    self.username = username
    self.password = password
    self.db = None
    self.source = source
    #if 'host' in kwargs and not kwargs['host']:
      #kwargs.pop('host')
    #if 'port' in kwargs and not kwargs['port']:
      #kwargs.pop('port')

    if not kwargs.get('port') and settings.MONGO_PORT:
        kwargs.update({'port': isinstance(settings.MONGO_PORT, basestring) and int(settings.MONGO_PORT) or settings.MONGO_PORT})

    self.cliente = None
    #self._collection = None
    self.conectar(*args, **kwargs)

  def __getitem__(self, index): # obtiene db
    try:
      self.db = self.cliente[index]
    except AutoReconnect:
      self.db = self[index]

    return self.db

  def conectar(self, *args, **kwargs):
    self.cliente = MongoClient(connect=False, *args, **kwargs) # raise ConnectionFailure

    if self.username and self.source:
        self[self.source].authenticate(self.username, self.password) # raise PyMongoError

    if self.db:
        for collection_name in self.db.collection_names(include_system_collections=False): # raise OperationFailure
            self.__dict__[''.join(map(lambda i: i.capitalize(), collection_name.replace('.', '_').split('_')))] = self.db[collection_name]

  #def obtener_collection(self):
    #return self._collection

  #def establecer_collection(self, collection):
    #self._collection = collection

  #collection = property(obtener_collection, establecer_collection)

  #def insertar(self, value):
    #try:
      #return self.collection.insert(value)
    #except AutoReconnect:
      #return self.insertar(value)

  def desconectar(self):
    if self.cliente is not None:
      self.cliente.close()