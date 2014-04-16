simshab_dataexporter
====================

data exporter in xml format for simsha

How to install
--------------

Get the oracle runtime libraries and install them
somewhere on your system.

 1. virtualenv venv
 2. source venv/bin/activate
 3. pip install -r requirements.txt

Add environment variable in venv/bin/activate:

 4. export SIMS_OUT_PATH=/path/to/output/dir
 5. export SQLALCHEMY='schema:///'
 6. export LD_LIBRARY_PATH=/path/to/oracle/instantclient_11_2


Run the exporter locally
------------------------

Activate virtualenv, then:

 cd sims
 python ../tools/cli.py -h

Available commands are:

 * report [species|habitat]
 * checklist [species|habitat]


How to create eggs
------------------

 pip uninstall sims
 python setup.py sdist --format=zip
 pip install dist/sims-0.1.zip
