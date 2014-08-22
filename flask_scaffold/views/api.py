from __future__ import unicode_literals
import logging
logger = logging.getLogger(__name__)

from flask import Module
from flask import request
from flask import jsonify
from flask import abort


api = Module(__name__)


@api.route('/version', methods=['GET'])
def version():
    logger.debug('version')
    if request.method == 'GET':
        from ..default_settings import VERSION
        return jsonify(data=dict(version=VERSION))
    abort(403)


@api.route('/events', methods=['GET', 'POST', 'DELETE'])
def access_event():
    logger.debug('access event')
    if request.method == 'GET':
        try:
            from flask_scaffold.models.mongodb.event import EventModel

            request_values = request.values
            created_from = request_values.get('created_from')
            created_to = request_values.get('created_to')
            offset = request_values.get('offset')
            limit = int(request_values.get('limit', 100))
            event_model = EventModel()
            events = event_model.get_events(created_from=created_from,
                                            created_to=created_to,
                                            offset=offset,
                                            limit=limit)
            data = dict(status='ok', data=events)
        except Exception as err:
            logger.warn('Error: %r', err)
            data = dict(status='fail', message='{}'.format(err))
        return jsonify(**data)
    elif request.method == 'POST':
        try:
            from flask_scaffold.models.mongodb.event import EventModel

            request_form = request.form
            message = request_form['message']
            event_model = EventModel()
            event = event_model.add_event(message)
            data = dict(status='ok', data=event)
        except Exception as err:
            logger.warn('Error: %r', err)
            data = dict(status='fail', message='{}'.format(err))
        return jsonify(**data)
    abort(403)


@api.route('/events/<event_id>', methods=['GET', 'DELETE'])
def access_event2(event_id):
    logger.debug('access event')
    if request.method == 'GET':
        try:
            from flask_scaffold.models.mongodb.event import EventModel

            event_model = EventModel()
            event = event_model.get_event_by_id(event_id)
            data = dict(status='ok', data=event)
        except Exception as err:
            logger.warn('Error: %r', err)
            data = dict(status='fail', message='{}'.format(err))
        return jsonify(**data)
    elif request.method == 'DELETE':
        try:
            from flask_scaffold.models.mongodb.event import EventModel

            event_model = EventModel()
            result = event_model.remove_event(id=event_id)
            data = dict(status='ok', data=result)
        except Exception as err:
            logger.warn('Error: %r', err)
            data = dict(status='fail', message='{}'.format(err))
        return jsonify(**data)
    abort(403)