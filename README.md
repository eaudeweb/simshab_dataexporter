simshab_dataexporter
====================

data exporter in xml format for simsha

How to install
--------------

Get the oracle runtime libraries and install them
somewhere on your system

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Add environment variable in venv/bin/activate:

    export SIMS_OUT_PATH=/path/to/output/dir
    export SQLALCHEMY='schema:///'
    export LD_LIBRARY_PATH=/path/to/oracle/instantclient_11_2


Run the exporter locally
------------------------

Activate virtualenv, then:

    python cli.py -h

Available commands are:

 * report [species|habitat]
 * checklist [species|habitat]


How to create eggs
------------------

    pip uninstall sims
    python setup.py sdist --format=zip
    pip install dist/sims-0.1.zip
