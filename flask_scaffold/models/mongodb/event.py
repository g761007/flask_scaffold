from __future__ import unicode_literals

import logging

from flask_scaffold.patterns.singleton import singleton
from flask_scaffold.models import mongodb
from flask_scaffold.utils import GuidFactory

@singleton
class EventModel(object):

    make_guid = GuidFactory('E')

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.db = mongodb.MongoDB()

    @property
    def _events(self):
        return self.db.getCollection('events')

    def add_event(self, message, created=None):
        events = self._events
        json_data = {
            '_id': self.make_guid(),
            'message': message,
            'created': created or self.db.getServerTimestamp()
        }
        id = events.insert(json_data)
        if id is None:
            raise RuntimeError('Failed to insert event. ({})'.format(json_data))
        return json_data

    def get_event_by_id(self, id):
        events = self._events
        return events.find_one({'_id': id})

    def iter_events(self, **kwargs):
        events = self._events
        params = {}
        created_from = kwargs.get('created_from')
        if created_from is not None:
            params['created'] = {'$gt': float(created_from)}
        created_to = kwargs.get('created_to')
        if created_to is not None:
            if 'created' not in params:
                params['created'] = {}
            params['created'].update({'$lt': float(created_to)})
        query = events.find(params)
        offset = kwargs.get('offset')
        if offset is not None:
            query = query.skip(int(offset))
        limit = kwargs.get('limit', 100)
        if limit is not None:
            query = query.limit(int(limit))
        sort = kwargs.get('sort')
        if sort is not None:
            query = query.sort(sort)
        else:
            query = query.sort([('created', -1)])
        for json_data in query:
            yield json_data

    def get_events(self, **kwargs):
        return list(self.iter_events(**kwargs))

    def count(self, **kwargs):
        events = self._events
        params = {}
        created_from = kwargs.get('created_from')
        if created_from is not None:
            params['created'] = {'$gt': float(created_from)}
        created_to = kwargs.get('created_to')
        if created_to is not None:
            if 'created' not in params:
                params['created'] = {}
            params['created'].update({'$lt': float(created_to)})
        return events.find(params).count()

    def remove_event(self, **kwargs):
        events = self._events
        params = {}
        id = kwargs.get('id')
        if id is not None:
            params['_id'] = id
        created_from = kwargs.get('created_from')
        if created_from is not None:
            params['created'] = {'$gt': float(created_from)}
        created_to = kwargs.get('created_to')
        if created_to is not None:
            if 'created' not in params:
                params['created'] = {}
            params['created'].update({'$lt': float(created_to)})
        return events.remove(params)
