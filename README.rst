sentry_elastic_nodestore
========================

:info: Sentry nodestore Elasticsearch backend

.. image:: https://img.shields.io/pypi/v/sentry_elastic_nodestore.svg
    :target: https://pypi.python.org/pypi/sentry_elastic_nodestore

Installation
------------

.. code-block:: shell

    pip install sentry_elastic_nodestore

Configuration
-------------

Set ``SENTRY_NODESTORE`` at Your ``sentry.conf.py``

.. code-block:: python

    from elasticsearch import Elasticsearch
    es = Elasticsearch(['127.0.0.1:9200'])
    SENTRY_NODESTORE = 'sentry_elastic_nodestore.ElasticNodeStorage'
    SENTRY_NODESTORE_OPTIONS = {
        'es': es,
    }

    from sentry.conf.server import *  # default for sentry.conf.py
    INSTALLED_APPS = list(INSTALLED_APPS)
    INSTALLED_APPS.append('sentry_elastic_nodestore')
    INSTALLED_APPS = tuple(INSTALLED_APPS)

Usage
-----

Setup elasticsearch template

.. code-block:: shell

    sentry --config sentry.conf.py django elastic_template
