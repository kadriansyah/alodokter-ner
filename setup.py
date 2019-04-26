from setuptools import find_packages
from setuptools import setup

#####
# We need to install some additional packages in order to compile
# OpenAI Gym on CMLE.
# Reference:
# https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/complete/juliaset/setup.py
import subprocess
from distutils.command.build import build as _build

import setuptools

class build(_build):
    """A build command class that will be invoked during package install.
    The package built using the current setup.py will be staged and later
    installed in the worker using `pip install package'. This class will be
    instantiated during install for this specific scenario and will trigger
    running the custom commands specified.
    """
    sub_commands = _build.sub_commands + [('CustomCommands', None)]

# The list of required libraries is taken from:
# https://github.com/openai/gym#installing-everything
_LIBS = 'python-numpy python-dev cmake zlib1g-dev libjpeg-dev xvfb libav-tools xorg-dev python-opengl libboost-all-dev libsdl2-dev swig'.split()

CUSTOM_COMMANDS = [
    ['apt-get', 'update'],
    ['apt-get', 'install', '-y'] + _LIBS,
]


class CustomCommands(setuptools.Command):
    """A setuptools Command class able to run arbitrary commands."""
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def RunCustomCommand(self, command_list):
        print('Running command: %s' % command_list)
        p = subprocess.Popen(
            command_list,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # Can use communicate(input='y\n'.encode()) if the command run requires
        # some confirmation.
        stdout_data, _ = p.communicate()
        print('Command output: %s' % stdout_data)
        if p.returncode != 0:
            raise RuntimeError('Command %s failed: exit code: %s' % (command_list, p.returncode))

    def run(self):
        for command in CUSTOM_COMMANDS:
            self.RunCustomCommand(command)

#####

REQUIRED_PACKAGES = [
    'pip>=19.1',
    'absl-py==0.2.2',
    'anago==1.0.8',
    'aniso8601==1.2.0',
    'asn1crypto==0.24.0',
    'astor==0.6.2',
    'beautifulsoup4==4.6.0',
    'bleach==1.5.0',
    'boto==2.48.0',
    'boto3==1.7.24',
    'botocore==1.10.24',
    'bz2file==0.98',
    'certifi==2018.4.16',
    'cffi==1.11.5',
    'chardet==3.0.4',
    'click==6.7',
    'cryptography==2.2.2',
    'docutils==0.14',
    'Flask==1.0.2',
    'Flask-RESTful==0.3.6',
    'gast==0.2.0',
    'gensim==3.4.0',
    'grpcio==1.12.1',
    'h5py==2.9.0',
    'html5lib==0.9999999',
    'idna==2.6',
    'itsdangerous==0.24',
    'Jinja2==2.10',
    'jmespath==0.9.3',
    'Keras==2.2.4',
    'Keras-Applications==1.0.7',
    'Keras-Preprocessing==1.0.9',
    'lxml==4.2.1',
    'Markdown==2.6.11',
    'MarkupSafe==1.0',
    'nltk==3.3',
    'numpy==1.14.3',
    'pandas==0.23.0',
    'protobuf>=3.6.0',
    'pycparser==2.18',
    'pycrypto==2.6.1',
    'pymongo==3.4.0',
    'pyOpenSSL==18.0.0',
    'PySocks==1.6.8',
    'python-dateutil==2.7.3',
    'pytz==2018.4',
    'PyYAML==5.1',
    'requests==2.18.4',
    's3transfer==0.1.13',
    'scikit-learn==0.19.1',
    'scipy==1.1.0',
    'seqeval==0.0.9',
    'six==1.11.0',
    'smart-open==1.5.7',
    'SQLAlchemy==1.2.8',
    'tensorboard==1.8.0',
    'tensorflow==1.8.0',
    'termcolor==1.1.0',
    'urllib3==1.22',
    'uWSGI==2.0.17',
    'Werkzeug==0.14.1'
]

setup(
    name='aloner',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    package_data={'trainer': ['data/*.txt']},
    description='Alodokter NER using Anago',
    cmdclass={
        # Command class instantiated and run during pip install scenarios.
        'build': build,
        'CustomCommands': CustomCommands,
    }
)