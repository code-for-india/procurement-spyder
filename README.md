# Procurement Spy

Money from World Bank supported projects impacts citizens and businesses directly
through the contracts that are awarded for public goods or services - such as
for laying roads or building schools. Surprisingly, not many many know about
these contracts we’re investing in, even when they represent large amounts of
public money meant for their neighbourhood.

1. Citizen oversight of who gets this money to do what and where can deter
corruption and improve quality of delivery.

2. Knowledge of upcoming tender notices can create a level playing field for
private sector, and be a useful resource for business owners.

Here we are solving second problem.

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

    export PYTHONPATH=$(pwd)/server/
    mongod
    python server.py
