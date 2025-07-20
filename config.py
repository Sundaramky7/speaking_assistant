"""
Secure Configuration Manager for Voice Assistant
Handles loading environment variables and configuration settings
"""

import os
import re
from pathlib import Path
import colorama
import getpass

class Config:
    """Configuration manager for voice assistant"""
    
    def __init__(self):
        self.env_path = Path(__file__).parent / '.env'
        self.setup_complete_file = Path(__file__).parent / '.setup_complete'
        self.load_env_file()
        
        # Check if first-time setup is needed
        if not self.is_setup_complete():
            self.run_first_time_setup()
        else:
            self.validate_config()
    
    def load_env_file(self):
        """Load environment variables from .env file"""
        env_path = Path(__file__).parent / '.env'
        
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        else:
            print(colorama.Fore.YELLOW + "⚠️  .env file not found. Using system environment variables." + colorama.Fore.WHITE)
    
    @property
    def email_address(self):
        """Get email address from environment"""
        return os.getenv('EMAIL_ADDRESS')
    
    @property
    def email_password(self):
        """Get email password from environment"""
        password = os.getenv('EMAIL_PASSWORD')
        if password:
            return password.replace(" ", "")
        return password
    
    @property
    def smtp_server(self):
        """Get SMTP server from environment"""
        return os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    
    @property
    def smtp_port(self):
        """Get SMTP port from environment"""
        port_str = os.getenv('SMTP_PORT', '587')
        try:
            port = int(port_str)
            if port <= 0:
                raise ValueError
            return port
        except (ValueError, TypeError):
            return 587
    
    @property
    def speech_rate(self):
        """Get speech rate from environment"""
        return int(os.getenv('SPEECH_RATE', '160'))
    
    @property
    def voice_name(self):
        """Get preferred voice name from environment"""
        return os.getenv('VOICE_NAME', 'Rishi')
    
    @property
    def wolfram_api_key(self):
        """Get Wolfram Alpha API key from environment"""
        return os.getenv('WOLFRAM_API_KEY')
    
    @property
    def weather_api_key(self):
        """Get Weather API key from environment"""
        return os.getenv('WEATHER_API_KEY')
    
    def validate_config(self):
        """Validate that required configuration is present"""
        required_vars = {
            'EMAIL_ADDRESS': self.email_address,
            'EMAIL_PASSWORD': self.email_password
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            print(colorama.Fore.RED + "❌ Missing required configuration:" + colorama.Fore.WHITE)
            for var in missing_vars:
                print(f"   - {var}")
            print(colorama.Fore.YELLOW + "📝 Please set these in your .env file or system environment variables." + colorama.Fore.WHITE)
            return False
        
        return True
    
    def get_email_config(self):
        """Get email configuration as dictionary"""
        return {
            'address': self.email_address,
            'password': self.email_password,
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port
        }
    
    def is_email_configured(self):
        """Check if email is properly configured"""
        return bool(self.email_address and self.email_password)
    
    def is_setup_complete(self):
        """Check if first-time setup has been completed"""
        return self.setup_complete_file.exists()
    
    def mark_setup_complete(self):
        """Mark setup as completed"""
        self.setup_complete_file.touch()
        print(colorama.Fore.GREEN + "✅ Setup completed successfully!" + colorama.Fore.WHITE)
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def run_first_time_setup(self):
        """Run the first-time setup wizard"""
        print(colorama.Fore.CYAN + "\n" + "="*60)
        print("🎤 Welcome to Rishi Voice Assistant!")
        print("="*60)
        print("First-time setup is required.")
        print(colorama.Fore.WHITE)
        
        # Get email address
        while True:
            print(colorama.Fore.YELLOW + "\n📧 Email Configuration" + colorama.Fore.WHITE)
            email = input("Enter your email address (for sending emails): ").strip()
            
            if not email:
                print(colorama.Fore.RED + "❌ Email address is required!" + colorama.Fore.WHITE)
                continue
            
            if not self.validate_email(email):
                print(colorama.Fore.RED + "❌ Invalid email format!" + colorama.Fore.WHITE)
                continue
            
            break
        
        # Get email password
        while True:
            print(colorama.Fore.YELLOW + "\n🔒 Email Password" + colorama.Fore.WHITE)
            print("For Gmail, use an App Password (not your regular password)")
            print("Generate one at: https://myaccount.google.com/apppasswords")
            
            password = getpass.getpass("Enter your email password/app password: ").strip().replace(" ", "")
            
            if not password:
                print(colorama.Fore.RED + "❌ Password is required!" + colorama.Fore.WHITE)
                continue
            
            break
        
        # Optional: SMTP settings
        print(colorama.Fore.YELLOW + "\n⚙️ SMTP Configuration (Optional)" + colorama.Fore.WHITE)
        smtp_server = input(f"SMTP Server [smtp.gmail.com]: ").strip() or "smtp.gmail.com"
        smtp_port_input = input(f"SMTP Port [587]: ").strip()
        smtp_port = smtp_port_input if smtp_port_input.isdigit() else "587"
        
        # Save configuration
        self.save_config_to_env(email, password, smtp_server, smtp_port)
        
        # Mark setup as complete
        self.mark_setup_complete()
        
        print(colorama.Fore.GREEN + "\n🎉 Setup completed! You can now use Rishi Voice Assistant." + colorama.Fore.WHITE)
        print(colorama.Fore.CYAN + "Tip: You can add contacts during conversations or manually edit contacts.json" + colorama.Fore.WHITE)
    
    def save_config_to_env(self, email, password, smtp_server, smtp_port):
        """Save configuration to .env file"""
        env_content = f"""# Rishi Voice Assistant Configuration
# Generated on first-time setup

# Email Configuration
EMAIL_ADDRESS={email}
EMAIL_PASSWORD={password}
SMTP_SERVER={smtp_server}
SMTP_PORT={smtp_port}

# Voice Configuration (Optional)
SPEECH_RATE=160
VOICE_NAME=Rishi

"""
        
        with open(self.env_path, 'w') as f:
            f.write(env_content)
        
        # Reload environment variables
        os.environ['EMAIL_ADDRESS'] = email
        os.environ['EMAIL_PASSWORD'] = password
        os.environ['SMTP_SERVER'] = smtp_server
        os.environ['SMTP_PORT'] = smtp_port
        
        print(colorama.Fore.GREEN + f"✅ Configuration saved to {self.env_path}" + colorama.Fore.WHITE)

# Global config instance
config = Config()
