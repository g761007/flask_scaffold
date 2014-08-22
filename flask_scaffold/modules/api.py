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
