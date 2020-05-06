#! /bin/sh

# see https://community.plone.org/t/not-using-bootstrap-py-as-default/620
ln -fs base.cfg buildout.cfg
virtualenv-2.7 .

./bin/pip install -U "zc.buildout==2.5.3"
./bin/pip install -U "setuptools==26.1.1"

./bin/buildout
