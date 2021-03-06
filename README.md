# Procurement Spyder

### Problem

Money from World Bank supported projects impacts citizens and businesses directly
through the contracts that are awarded for public goods or services - such as
for laying roads or building schools. Surprisingly, not many many know about
these contracts we’re investing in, even when they represent large amounts of
public money meant for their neighborhood.

### Proposed Solutions

Procurement Spyder will have a knowledge of upcoming tender notices by
crawling world bank's site every day. Business owners can subscribe with the sectors and
location they are interested in. Procurement Spider notify business owners
whenever there is new tender or procurements under subscribed locations and sectors.

### Install dependencies

Following steps are only needed one time

  1. virtualenv venv
  2. source venv/bin/activate
  3. pip install -r requirements.pip

### Run application

    export MAILGUN_API_KEY=copy_from_conf
    source venv/bin/activate
    mongod
    cd wsgi/
    python server.py

To Scrawl the World Bank Projects and Procurements

    cd wsgi/
    python worldbank.py

### Deploy to openshift

    $ rhc env-set MAILGUN_API_KEY=copy_from_conf -a procurement
    $ rhc env-set HOSTED_AT=http://procurement-spyder.chennainerd.in -a procurement
    $ git push openshift master
