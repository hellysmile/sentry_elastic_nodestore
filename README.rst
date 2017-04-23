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

Set `SENTRY_NODESTORE` at Your `sentry.conf.py`

.. code-block:: python

    from elasticsearch import Elasticsearch
    es = Elasticsearch(['127.0.0.:9200'])
    SENTRY_NODESTORE = 'sentry_elastic_nodestore.ElasticNodeStorage'
    SENTRY_NODESTORE_OPTIONS = {
        'es': es,
    }

Usage
-----

Setup elasticsearch template

.. code-block:: shell

    sentry --config sentry.conf.py django elastic_template
