import os, sys

try:
    if not os.environ['CONFIG_PATH'] == 'py_ferry.config.TestingConfig':
        print('Environment not set: run tests by executing `python manage.py test`')
        sys.exit(1)
except:
    print('Environment not set: run tests by executing "python manage.py test"')
    sys.exit(1)