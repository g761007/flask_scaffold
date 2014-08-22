from __future__ import unicode_literals
import logging
import datetime

from pymongo import Connection

from flask_scaffold.patterns.singleton import singleton
from flask_scaffold.core import app

class MongoDBError(RuntimeError):
    """MongoDB error

    """

@singleton
class MongoDB(object):

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        hosts = app.config['MONGO_HOSTS']
        args = app.config['MONGO_ARGS']
        self.connection = Connection(hosts, **args)
        self.logger.info('Setup Mongo db connection %r', args)

        db = app.config['MONGO_DB']
        self.db = self.connection[db]
        self.logger.info('Switch to DB %r', db)

    def getCollection(self, name):
        collection = self.db[name]
        return collection

    def getServerTimestamp(self):
        """Get time stamp from MongoDB server

        """
        timestamp = self.db.eval('new Date().getTime()')
        timestamp /= 1000.0
        return timestamp

    def getServerDatetime(self):
        """Get current DateTime from MongoDB server

        """
        timestamp = self.getServerTimestamp()
        return datetime.datetime.utcfromtimestamp(timestamp)