import os
import io
import json
from optparse import make_option

from elasticsearch import TransportError
from django.core.management.base import BaseCommand, CommandError
from sentry.app import nodestore
from sentry.utils.functional import extract_lazy_object
from sentry_elastic_nodestore import ElasticNodeStorage


class Command(BaseCommand):
    help = 'Create elasticsearch template for nodestore'

    option_list = BaseCommand.option_list + (
        make_option(
            '--template',
            default=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                '..',
                '..',
                'templates',
                'sentry.json',
            ),
            help='Path to elasticsearch template'),
        )

    def handle(self, *args, **options):
        if not isinstance(extract_lazy_object(nodestore), ElasticNodeStorage):
            raise CommandError('ElasticNodeStorage is not correctly configured')

        template = os.path.abspath(options['template'])

        with io.open(template, mode='rt', encoding=nodestore.encoding) as fp:
            template = json.load(fp)

        try:
            nodestore.put_template(template)
        except TransportError as exc:
            if exc.info.get('error', {}).get('reason') == 'index_template [sentry] already exists':
                raise CommandError('Template already exists')

            raise

        self.stdout.write('Successfully created elastic template')
