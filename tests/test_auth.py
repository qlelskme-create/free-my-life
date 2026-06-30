"""
Authentication module tests
"""

import unittest
from flask import Flask
from auth.authentication import User, AuthenticationManager, db

class TestAuthentication(unittest.TestCase):
    """Test authentication functionality"""
    
    def setUp(self):
        """Set up test app and database"""
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        
        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()
    
    def test_user_registration(self):
        """Test user registration"""
        with self.app.app_context():
            user = AuthenticationManager.register_user(
                'testuser',
                'test@example.com',
                'SecurePass123!'
            )
            
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.email, 'test@example.com')
    
    def test_duplicate_username(self):
        """Test registering duplicate username"""
        with self.app.app_context():
            AuthenticationManager.register_user('testuser', 'test@example.com', 'SecurePass123!')
            
            with self.assertRaises(ValueError):
                AuthenticationManager.register_user('testuser', 'other@example.com', 'SecurePass123!')
    
    def test_password_hashing(self):
        """Test password hashing"""
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('SecurePass123!')
            
            self.assertTrue(user.check_password('SecurePass123!'))
            self.assertFalse(user.check_password('WrongPassword'))
    
    def test_authentication(self):
        """Test user authentication"""
        with self.app.app_context():
            user = AuthenticationManager.register_user('testuser', 'test@example.com', 'SecurePass123!')
            db.session.commit()
            
            authenticated_user = AuthenticationManager.authenticate_user('testuser', 'SecurePass123!')
            self.assertIsNotNone(authenticated_user)
            self.assertEqual(authenticated_user.username, 'testuser')
    
    def test_wrong_password(self):
        """Test authentication with wrong password"""
        with self.app.app_context():
            AuthenticationManager.register_user('testuser', 'test@example.com', 'SecurePass123!')
            
            authenticated_user = AuthenticationManager.authenticate_user('testuser', 'WrongPassword')
            self.assertIsNone(authenticated_user)

if __name__ == '__main__':
    unittest.main()
