import io
import os
import re

from setuptools import setup


def get_version():
    regex = r"__version__\s=\s\'(?P<version>[\d\.]+?)\'"

    path = ('sentry_elastic_nodestore', '__init__.py')

    return re.search(regex, read(*path)).group('version')


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


setup(
    name='sentry_elastic_nodestore',
    version=get_version(),
    author='hellysmile@gmail.com',
    author_email='hellysmile@gmail.com',
    url='https://github.com/hellysmile/sentry_elastic_nodestore',
    description='Sentry nodestore Elasticsearch backend',
    long_description=read('README.rst'),
    packages=[
        'sentry_elastic_nodestore',
        'sentry_elastic_nodestore.management',
        'sentry_elastic_nodestore.management.commands',
    ],
    package_data={
        'sentry_elastic_nodestore': [
            'templates/*',
        ],
    },
    include_package_data=True,
    install_requires=[
        'sentry',
        'elasticsearch',
        'lz4',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    keywords=['sentry', 'elasticsearch', 'nodestore', 'backend'],
)
