# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for invenio-records-lom."""

from __future__ import absolute_import, print_function

from . import config


class LomRecords(object):
    """invenio-records-lom extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['invenio-records-lom'] = self

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        with_endpoints = app.config.get(
            'INVENIO_RECORDS_LOM_ENDPOINTS_ENABLED', True)
        for k in dir(config):
            if k.startswith('INVENIO_RECORDS_LOM_'):
                app.config.setdefault(k, getattr(config, k))
            elif k == 'SEARCH_UI_JSTEMPLATE_RESULTS':
                app.config['SEARCH_UI_JSTEMPLATE_RESULTS'] = getattr(
                    config, k)
            elif k == 'PIDSTORE_RECID_FIELD':
                app.config['PIDSTORE_RECID_FIELD'] = getattr(config, k)
            else:
                for n in ['RECORDS_REST_ENDPOINTS', 'RECORDS_UI_ENDPOINTS']:
                    if k == n and with_endpoints:
                        app.config.setdefault(n, {})
                        app.config[n].update(getattr(config, k))
