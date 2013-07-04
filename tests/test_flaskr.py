import unittest
import uuid

import flaskr


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()

    def tearDown(self):
        pass

    def login(self, username):
        return self.app.post(
            '/login',
            data={'username': username},
            follow_redirects=True)

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True)

    def test_login_without_username(self):
        r = self.login('')
        self.assertIn('Invalid username', r.data)

    def test_login_logout(self):
        username = uuid.uuid4().hex

        r = self.login(username)
        self.assertIn('Welcome, %s' % username, r.data)

        r = self.logout()
        self.assertIn('You were logged out', r.data)
        self.assertNotIn(username, r.data)

    def test_logout_idempotent(self):
        r = self.logout()
        self.assertIn('You were logged out', r.data)

        r = self.logout()
        self.assertIn('You were logged out', r.data)

if __name__ == '__main__':
    unittest.main()