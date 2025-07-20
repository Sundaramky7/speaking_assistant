"""
Secure Email Handler for Voice Assistant
Handles email sending with proper security and error handling
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import colorama
from config import config

class EmailHandler:
    """Secure email handler with proper error handling"""
    
    def __init__(self):
        self.email_config = config.get_email_config()
        self.is_configured = config.is_email_configured()
    
    def send_email(self, to_address, subject, content):
        """
        Send email securely with proper error handling
        
        Args:
            to_address (str): Recipient email address
            subject (str): Email subject
            content (str): Email content
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.is_configured:
            print(colorama.Fore.RED + "❌ Email not configured. Please check your .env file." + colorama.Fore.WHITE)
            return False
        
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.email_config['address']
            message["To"] = to_address
            message["Subject"] = subject
            
            # Add body to email
            message.attach(MIMEText(content, "plain"))
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            
            print(colorama.Fore.CYAN + "📧 Connecting to email server..." + colorama.Fore.WHITE)
            
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls(context=context)
                server.login(self.email_config['address'], self.email_config['password'])
                
                print(colorama.Fore.BLUE + "📤 Sending email..." + colorama.Fore.WHITE)
                
                text = message.as_string()
                server.sendmail(self.email_config['address'], to_address, text)
                
                print(colorama.Fore.GREEN + "✅ Email sent successfully!" + colorama.Fore.WHITE)
                return True
                
        except smtplib.SMTPAuthenticationError:
            print(colorama.Fore.RED + "❌ Email authentication failed. Check your credentials." + colorama.Fore.WHITE)
            print(colorama.Fore.YELLOW + "💡 Make sure you're using an app-specific password for Gmail." + colorama.Fore.WHITE)
            return False
            
        except smtplib.SMTPRecipientsRefused:
            print(colorama.Fore.RED + f"❌ Invalid recipient address: {to_address}" + colorama.Fore.WHITE)
            return False
            
        except smtplib.SMTPServerDisconnected:
            print(colorama.Fore.RED + "❌ Server disconnected. Check your internet connection." + colorama.Fore.WHITE)
            return False
            
        except Exception as e:
            print(colorama.Fore.RED + f"❌ Email sending failed: {str(e)}" + colorama.Fore.WHITE)
            return False
    
    def validate_email(self, email_address):
        """
        Basic email validation
        
        Args:
            email_address (str): Email address to validate
            
        Returns:
            bool: True if email appears valid, False otherwise
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email_address) is not None

# Global email handler instance
email_handler = EmailHandler()
