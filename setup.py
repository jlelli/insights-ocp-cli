from setuptools import setup

SHORT_DESC = 'Red Hat Insights OCP CLI'
LONG_DESC = 'CLI for manipulating Red Hat Insights OCP'
VERSION = '0.0.1'

setup(
    name='insights-ocp-cli',
    author='Jeremy Crafts <jcrafts@redhat.com>',
    author_email='jcrafts@redhat.com',
    license='GPL',
    version='0.0.1',
    description='Red Hat Insights OCP CLI',
    long_description='CLI for manipulating Red Hat Insights OCP',
    entry_points={'console_scripts': [
        'insights-cli = deploy:main'
    ]},
    data_files=[('', ['dev/api.yaml',
                      'dev/ui.yaml',
                      'dev/controller.yaml',
                      'dev/scanner.yaml',
                      'dev/scan-job.yaml'])])