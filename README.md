simshab_dataexporter
====================

data exporter in xml format for simshab<br>

How to install:<br>
1. virtualenv venv<br>
2. source venv/bin/activate<br>
3. pip install -r requirements.txt<br>
Add environment variable <br>
4. set SIMS_OUT_PATH=/home/ovidiu/work/tst_sims<br>
5. set SQLALCHEMY= <br>

How to create eggs:
pip uninstall sims<br>
python setup.py sdist --format=zip<br>
pip install dist/sims-0.1.zip<br>


