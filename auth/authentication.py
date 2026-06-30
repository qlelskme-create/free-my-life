"""
Authentication module - User authentication and 2FA
"""

import bcrypt
import pyotp
import qrcode
import io
from datetime import datetime, timedelta
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 2FA
    totp_secret = db.Column(db.String(32), nullable=True)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Login attempts
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set password"""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    def is_account_locked(self):
        """Check if account is locked due to failed attempts"""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        elif self.locked_until and datetime.utcnow() >= self.locked_until:
            self.failed_login_attempts = 0
            self.locked_until = None
            db.session.commit()
        return False
    
    def record_failed_login(self, max_attempts=5, lockout_minutes=15):
        """Record a failed login attempt"""
        self.failed_login_attempts += 1
        
        if self.failed_login_attempts >= max_attempts:
            self.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
        
        db.session.commit()
    
    def record_successful_login(self):
        """Record a successful login"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def enable_two_factor(self):
        """Enable 2FA and generate secret"""
        self.totp_secret = pyotp.random_base32()
        self.two_factor_enabled = False  # Will be enabled after verification
        db.session.commit()
        return self.totp_secret
    
    def get_totp_uri(self):
        """Get TOTP URI for QR code"""
        if not self.totp_secret:
            return None
        
        totp = pyotp.TOTP(self.totp_secret)
        return totp.provisioning_uri(
            name=self.email,
            issuer_name='FreeMyLife'
        )
    
    def verify_totp(self, token):
        """Verify TOTP token"""
        if not self.totp_secret:
            return False
        
        totp = pyotp.TOTP(self.totp_secret)
        return totp.verify(token)
    
    def disable_two_factor(self):
        """Disable 2FA"""
        self.totp_secret = None
        self.two_factor_enabled = False
        db.session.commit()
    
    def get_qr_code(self):
        """Generate QR code for 2FA setup"""
        uri = self.get_totp_uri()
        if not uri:
            return None
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for display in HTML
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        import base64
        return base64.b64encode(img_io.getvalue()).decode()


class AuthenticationManager:
    """Manages user authentication"""
    
    @staticmethod
    def register_user(username, email, password):
        """Register a new user"""
        # Check if user exists
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists")
        
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already exists")
        
        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user by username and password"""
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return None
        
        if user.is_account_locked():
            raise Exception("Account locked. Try again later.")
        
        if not user.check_password(password):
            user.record_failed_login()
            return None
        
        return user
    
    @staticmethod
    def verify_two_factor(user, token):
        """Verify 2FA token"""
        if not user.two_factor_enabled:
            return False
        
        return user.verify_totp(token)
