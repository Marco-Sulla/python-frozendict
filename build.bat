del /S /Q build dist frozendict.egg-info
set CIBUILDWHEEL="1"
python setup.py %*
