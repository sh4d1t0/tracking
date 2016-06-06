from track.mongo import MongoDB
from django.conf import settings

cliente_mongo = MongoDB(username=settings.MONGO_USERNAME, password=settings.MONGO_PWD, source=settings.MONGO_DB)
events_collection = cliente_mongo.Events