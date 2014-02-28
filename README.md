simshab_dataexporter
====================

data exporter in xml format for simshab<br>

How to install:<br>
1. virtualenv venv<br>
2. source venv/bin/activate<br>
3. pip install -r requirements.txt<br>
Add environment variable
4. set SIMS_OUT_PATH=/home/ovidiu/work/tst_sims
5. set SQLALCHEMY=

How to create eggs:
pip uninstall sims
python setup.py sdist --format=zip
pip install dist/sims-0.1.zip


