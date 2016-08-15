import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# configure your app to use the testing configuration
if not 'CONFIG_PATH' in os.environ:
    os.environ['CONFIG_PATH'] = 'blog.config.TestingConfig'

from py_ferry import app
from py_ferry.database import Base, engine, session, User

'''adding engine disposition and drop_all before setup in case earlier test suite run was interrupted'''
engine.dispose()
Base.metadata.drop_all(engine)

class TestViews(unittest.TestCase):
    def setUp(self):
        ''' Test setup '''
        
        self.browser = Browser('phantomjs')
        
        # if we don't set the window size, we won't be able to interact with UI that might 
        # be hidden because of our media queries with a smaller emulated window
        self.browser.driver.set_window_size(1120, 550)
        
        # set up the tables in the database
        Base.metadata.create_all(engine)
        
        # create an example user
        self.user = User(name = 'capnmorgan', email = 'bob@aol.com',
            password = generate_password_hash('test'))
        session.add(self.user)
        session.commit()
        
        # create a second example user
        self.user = User(name = 'Bob', email = 'bob@example.com',
            password = generate_password_hash('test'))
        session.add(self.user)
        session.commit()
        
        self.process = multiprocessing.Process(target = app.run, kwargs = { 'port': 7000 })
        self.process.start()
        time.sleep(1)
        
    def tearDown(self):
        ''' Test teardown '''
        # remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()
        if os.environ['CONFIG_PATH'] != 'py_ferry.config.TravisConfig':
            os.system('pgrep phantomjs | xargs kill')
        
    def test_login_correct(self):
        self.browser.visit('http://127.0.0.1:7000/login')
        self.browser.fill('name', 'capnmorgan')
        self.browser.fill('password', 'test')
        button = self.browser.find_by_css('button.login')
        button.click()
        time.sleep(1)
        self.assertEqual(self.browser.url, 'http://127.0.0.1:7000/games')
        self.assertFalse(self.browser.is_element_present_by_css('button.login'))
        self.assertTrue(self.browser.is_element_present_by_css('#games'))
        
    def test_registration(self):
        self.browser.visit('http://127.0.0.1:7000/register')
        self.browser.fill('name', 'capn')
        self.browser.fill('email', 'capn@caribbean.com')
        self.browser.fill('password', 'test')
        self.browser.fill('passwordConfirm', 'test')
        checkbox = self.browser.find_by_css('input.checkbox')
        checkbox.click()
        button = self.browser.find_by_css('button.register')
        button.click()
        time.sleep(1)
        self.assertEqual(self.browser.url, 'http://127.0.0.1:7000/login')
        self.assertTrue(self.browser.is_element_present_by_css('button.login'))
        self.assertFalse(self.browser.is_element_present_by_css('button.register'))
        self.browser.fill('name', 'capnmorgan')
        self.browser.fill('password', 'test')
        button = self.browser.find_by_css('button.login')
        button.click()
        time.sleep(1)
        self.assertEqual(self.browser.url, 'http://127.0.0.1:7000/games')
        self.assertFalse(self.browser.is_element_present_by_css('button.login'))
        self.assertTrue(self.browser.is_element_present_by_css('#games'))

if __name__ == '__main__':
    unittest.main()