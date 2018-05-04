from setuptools import setup, find_packages

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
    packages=find_packages(),
    entry_points={'console_scripts': [
        'insights-ocp-cli = insights_ocp_cli:main'
    ]},
    data_files=[('/etc/insights-ocp-cli',
                ['yaml/imagestreams.yaml',
                 'yaml/api.yaml',
                 'yaml/ui.yaml',
                 'yaml/scanner.yaml'])])
