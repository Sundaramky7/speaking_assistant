"""
Contact Management Module for Voice Assistant
Maps contact names to email addresses using a dictionary-based approach
"""

import colorama
import json
from pathlib import Path

class ContactManager:
    """Manages contact information for email functionality"""
    
    def __init__(self):
        self.contacts_file = Path(__file__).parent / 'contacts.json'
        self.contacts = self.load_contacts()
    
    def load_contacts(self):
        """Load contacts from a JSON file"""
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                return json.load(f)
        return {}

    def save_contacts(self):
        """Save contacts to a JSON file"""
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f, indent=4)
    
    def find_contact(self, name_input):
        """
        Find contact email based on name input
        
        Args:
            name_input (str): Name or partial name to search for
            
        Returns:
            tuple: (email_address, contact_name) or (None, None) if not found
        """
        name_input = name_input.lower().strip()
        
        # First try exact match
        if name_input in self.contacts:
            return self.contacts[name_input], name_input
        
        # Then try partial match
        for contact_name, email in self.contacts.items():
            if contact_name in name_input or name_input in contact_name:
                return email, contact_name
        
        return None, None
    
    def get_all_contacts(self):
        """Get all contacts as a dictionary"""
        return self.contacts.copy()
    
    def add_contact(self, name, email):
        """
        Add a new contact
        
        Args:
            name (str): Contact name
            email (str): Contact email address
        """
        self.contacts[name.lower().strip()] = email
        self.save_contacts()
        print(colorama.Fore.GREEN + f"✅ Contact '{name}' added with email '{email}'" + colorama.Fore.WHITE)
    
    def remove_contact(self, name):
        """
        Remove a contact
        
        Args:
            name (str): Contact name to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        name = name.lower().strip()
        if name in self.contacts:
            del self.contacts[name]
            print(colorama.Fore.GREEN + f"✅ Contact '{name}' removed" + colorama.Fore.WHITE)
            return True
        else:
            print(colorama.Fore.RED + f"❌ Contact '{name}' not found" + colorama.Fore.WHITE)
            return False
    
    def list_contacts(self):
        """List all contacts"""
        if not self.contacts:
            print(colorama.Fore.YELLOW + "\n📞 No contacts found. Add some contacts first!" + colorama.Fore.WHITE)
            return
            
        print(colorama.Fore.CYAN + "\n📞 Available Contacts:" + colorama.Fore.WHITE)
        print("-" * 40)
        for name, email in sorted(self.contacts.items()):
            print(f"  {name.title()}: {email}")
        print("-" * 40)
    
    def validate_email(self, email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def prompt_add_new_contact(self, name_input):
        """Prompt user to add a new contact when not found (keyboard input for email)"""
        print(colorama.Fore.YELLOW + f"\n❓ Contact '{name_input}' not found." + colorama.Fore.WHITE)
        
        while True:
            add_contact = input("Would you like to add this contact? (y/n): ").strip().lower()
            if add_contact in ['y', 'yes']:
                break
            elif add_contact in ['n', 'no']:
                print(colorama.Fore.RED + "❌ Email not sent." + colorama.Fore.WHITE)
                return None, None
            else:
                print(colorama.Fore.RED + "Please enter 'y' for yes or 'n' for no." + colorama.Fore.WHITE)
        
        # Get contact name (suggest the original input)
        suggested_name = name_input.title()
        contact_name = input(f"Contact name [{suggested_name}]: ").strip() or suggested_name
        
        # Get email address via keyboard input (more reliable than speech recognition)
        print(colorama.Fore.CYAN + "\n📧 Please type the email address (speech recognition not used for emails)" + colorama.Fore.WHITE)
        while True:
            try:
                email = input(f"📧 Email address for {contact_name}: ").strip()
                
                if not email:
                    print(colorama.Fore.RED + "❌ Email address is required!" + colorama.Fore.WHITE)
                    continue
                
                if not self.validate_email(email):
                    print(colorama.Fore.RED + "❌ Invalid email format! Please enter a valid email address." + colorama.Fore.WHITE)
                    continue
                
                break
                
            except KeyboardInterrupt:
                print(colorama.Fore.YELLOW + "\n⚠️ Contact addition cancelled" + colorama.Fore.WHITE)
                return None, None
        
        # Add the contact
        self.add_contact(contact_name, email)
        print(colorama.Fore.GREEN + f"✅ Contact '{contact_name}' added successfully!" + colorama.Fore.WHITE)
        return email, contact_name.lower()
    
    def find_or_add_contact(self, name_input):
        """Find contact or prompt to add if not found"""
        # Try to find existing contact first
        email, contact_name = self.find_contact(name_input)
        
        if email:
            return email, contact_name
        
        # Contact not found, prompt to add
        return self.prompt_add_new_contact(name_input)

# Global contact manager instance
contact_manager = ContactManager()
