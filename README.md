# Procurement Spyder

### Problem

Money from World Bank supported projects impacts citizens and businesses directly
through the contracts that are awarded for public goods or services - such as
for laying roads or building schools. Surprisingly, not many many know about
these contracts we’re investing in, even when they represent large amounts of
public money meant for their neighbourhood.

### Proposed Solutions

Procurement Spyder will have a knowledge of upcoming tender notices by
crawling world bank's site every day. Business owners can subscribe with the sectors and
location they are interested in. Procurement Spider notify business owners
whenever there is new tender or procurements under subscribed locations and sectors.

### Install dependencies

Following steps are only needed one time

  1. npm install
  2. bower install
  3. virtualenv venv
  4. source venv/bin/activate
  5. pip install -r requirements.pip


### Run gulp to watch and compile Sass

To compile a sass

    gulp

To compile and watch for sass file changes

    gulp watch

### Run application

    source venv/bin/activate
    mongod
    cd wsgi
    python server.py
