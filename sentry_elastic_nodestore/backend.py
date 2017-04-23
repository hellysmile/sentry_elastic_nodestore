import base64
import datetime
import uuid
import warnings
import logging
try:
    import cPickle as pickle
except ImportError:
    import pickle  # noqa

import lz4
from elasticsearch import NotFoundError
from sentry.exceptions import InvalidConfiguration
from sentry.nodestore.base import NodeStorage

logger = logging.getLogger(__name__)


class ElasticNodeStorage(NodeStorage):
    encoding = 'utf-8'

    template_not_found_msg = '''
        Missing elasticsearch template

        Run sentry --config sentry.conf.py django elastic_template
    '''

    def __init__(
        self,
        es,
        index='sentry-{date}',
        doc_type='node',
        template_name='sentry',
    ):
        self.es = es
        self.index = index
        self.doc_type = doc_type
        self.template_name = template_name

        self._template_found = False
        self._validated = False

        super(ElasticNodeStorage, self).__init__()

    def validate(self):
        if self._validated:
            return

        self._validated = True

        if not self.es.ping():
            raise InvalidConfiguration('Can not connect to elasticsearch')

        try:
            ret = self.es.indices.get_template(name=self.template_name)
            self._template_found = True
        except NotFoundError:
            logger.error(self.template_not_found_msg)

    def delete(self, id):
        self._ensure_template()

        index = self._get_index(id)

        self.es.delete(id=id, index=index, doc_type=self.doc_type)

    def get(self, id):
        self._ensure_template()

        index = self._get_index(id)

        try:
            response = self.es.get(id=id, index=index, doc_type=self.doc_type)
        except NotFoundError:
            return None
        else:
            return self._loads(response['_source']['data'])

    def set(self, id, data):
        self._ensure_template()

        index = self._get_index(id)

        data = self._dumps(data)

        data = {
            'data': data,
        }

        self.es.index(id=id, index=index, doc_type=self.doc_type, body=data)

    def generate_id(self):
        return uuid.uuid1().hex

    def cleanup(self, cutoff_timestamp):
        raise NotImplementedError

    def _get_index(self, id):
        if not isinstance(id, uuid.UUID):
            id = uuid.UUID(id)

        assert id.version == 1

        t = id.time
        t = t - 0x01b21dd213814000
        t = t / 1e7
        t = int(t)

        d = datetime.datetime.utcfromtimestamp(t)

        return self.index.format(date=d.strftime('%Y.%m.%d'))

    def _loads(self, data):
        data = base64.b64decode(data.encode(self.encoding))
        data = lz4.block.decompress(data)
        return pickle.loads(data)

    def _dumps(self, data):
        data = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        data = lz4.block.compress(
            data,
            mode='high_compression',
            compression=9,
            store_size=True,
        )
        return base64.b64encode(data).decode(self.encoding)

    def _ensure_template(self):
        if not self._validated:
            self.validate()

        if not self._template_found:
            raise InvalidConfiguration(self.template_not_found_msg)

    def put_template(self, template):
        self.es.indices.put_template(
            name=self.template_name,
            body=template,
            create=True,
        )
