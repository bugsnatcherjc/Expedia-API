# Email service integration for OTP (Production Ready)

import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import os
from typing import Optional
import random
import string

class EmailService:
    def __init__(self):
        # Email configuration - set these in environment variables for production
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', 'your-email@gmail.com')
        self.smtp_password = os.getenv('SMTP_PASSWORD', 'your-app-password')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@expedia-inspired.com')
        
        # Development mode flag
        self.development_mode = os.getenv('DEVELOPMENT_MODE', 'true').lower() == 'true'
        self.static_otp = os.getenv('STATIC_OTP', '123456')
    
    def generate_otp(self, length: int = 6) -> str:
        """Generate random OTP"""
        if self.development_mode:
            return self.static_otp
        
        # Generate random numeric OTP
        return ''.join(random.choices(string.digits, k=length))
    
    def send_otp_email(self, to_email: str, otp_code: str, purpose: str = 'signup') -> dict:
        """
        Send OTP via email
        
        Args:
            to_email: Recipient email address
            otp_code: The OTP code to send
            purpose: 'signup', 'login', or 'password_reset'
        
        Returns:
            dict: Success/failure status with message
        """
        
        if self.development_mode:
            # Development mode - don't actually send email
            print(f"📧 [DEV MODE] OTP Email would be sent to: {to_email}")
            print(f"🔑 [DEV MODE] OTP Code: {otp_code}")
            return {
                'success': True,
                'message': f'Development mode: OTP is {otp_code}',
                'otp_code': otp_code  # Only include in development
            }
        
        try:
            # Create email message
            subject = self._get_email_subject(purpose)
            body = self._get_email_body(otp_code, purpose)
            
            msg = MimeMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MimeText(body, 'html'))
            
            # Connect to server and send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable encryption
            server.login(self.smtp_username, self.smtp_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            print(f"✅ OTP email sent successfully to {to_email}")
            return {
                'success': True,
                'message': f'OTP sent to {to_email}'
            }
            
        except Exception as e:
            print(f"❌ Failed to send OTP email: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send email: {str(e)}'
            }
    
    def _get_email_subject(self, purpose: str) -> str:
        """Get email subject based on purpose"""
        subjects = {
            'signup': '🏨 Welcome to Expedia Inspired - Verify Your Email',
            'login': '🔐 Your Login Code - Expedia Inspired',
            'password_reset': '🔑 Password Reset Code - Expedia Inspired'
        }
        return subjects.get(purpose, '🔐 Your Verification Code')
    
    def _get_email_body(self, otp_code: str, purpose: str) -> str:
        """Generate HTML email body"""
        
        if purpose == 'signup':
            return f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background-color: #003580; color: white; padding: 20px; text-align: center;">
                        <h1>🏨 Welcome to Expedia Inspired!</h1>
                    </div>
                    
                    <div style="padding: 30px;">
                        <h2>Verify Your Email Address</h2>
                        <p>Thank you for signing up! Please use the verification code below to complete your registration:</p>
                        
                        <div style="background-color: #f8f9fa; border: 2px solid #003580; padding: 20px; text-align: center; margin: 20px 0;">
                            <h2 style="color: #003580; margin: 0; font-size: 32px; letter-spacing: 5px;">{otp_code}</h2>
                        </div>
                        
                        <p><strong>This code will expire in 10 minutes.</strong></p>
                        
                        <p>If you didn't request this code, please ignore this email.</p>
                        
                        <hr style="margin: 30px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated message from Expedia Inspired. Please do not reply to this email.
                        </p>
                    </div>
                </body>
            </html>
            """
        
        elif purpose == 'login':
            return f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background-color: #003580; color: white; padding: 20px; text-align: center;">
                        <h1>🔐 Login Verification</h1>
                    </div>
                    
                    <div style="padding: 30px;">
                        <h2>Your Login Code</h2>
                        <p>Someone requested to log in to your Expedia Inspired account. Use the code below:</p>
                        
                        <div style="background-color: #f8f9fa; border: 2px solid #003580; padding: 20px; text-align: center; margin: 20px 0;">
                            <h2 style="color: #003580; margin: 0; font-size: 32px; letter-spacing: 5px;">{otp_code}</h2>
                        </div>
                        
                        <p><strong>This code will expire in 10 minutes.</strong></p>
                        
                        <p>If this wasn't you, please secure your account immediately.</p>
                        
                        <hr style="margin: 30px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated message from Expedia Inspired. Please do not reply to this email.
                        </p>
                    </div>
                </body>
            </html>
            """
        
        else:  # password_reset
            return f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background-color: #003580; color: white; padding: 20px; text-align: center;">
                        <h1>🔑 Password Reset</h1>
                    </div>
                    
                    <div style="padding: 30px;">
                        <h2>Reset Your Password</h2>
                        <p>You requested to reset your password. Use the code below to proceed:</p>
                        
                        <div style="background-color: #f8f9fa; border: 2px solid #003580; padding: 20px; text-align: center; margin: 20px 0;">
                            <h2 style="color: #003580; margin: 0; font-size: 32px; letter-spacing: 5px;">{otp_code}</h2>
                        </div>
                        
                        <p><strong>This code will expire in 10 minutes.</strong></p>
                        
                        <p>If you didn't request this, please ignore this email.</p>
                        
                        <hr style="margin: 30px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated message from Expedia Inspired. Please do not reply to this email.
                        </p>
                    </div>
                </body>
            </html>
            """

# Initialize email service
email_service = EmailService()

# Example usage:
"""
# For development (uses static OTP)
result = email_service.send_otp_email("user@example.com", "123456", "signup")

# For production (set environment variables):
# DEVELOPMENT_MODE=false
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
# FROM_EMAIL=noreply@expedia-inspired.com
"""
