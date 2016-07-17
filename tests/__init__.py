import os, sys

try:
    if not os.environ['CONFIG_PATH'] == 'py_ferry.config.TestingConfig':
        print('Environment not set: run tests by executing `python manage.py test`.')
        sys.exit('Run tests by executing `python manage.py test`.')
except:
    sys.exit('Environment not set: run tests by executing `python manage.py test`.')