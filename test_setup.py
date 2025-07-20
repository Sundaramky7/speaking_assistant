#!/usr/bin/env python3
"""
Test script for the first-time setup functionality
This script demonstrates the setup process without running the full voice assistant
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

def test_first_time_setup():
    """Test the first-time setup process"""
    print("🧪 Testing First-Time Setup Functionality")
    print("=" * 50)
    
    # Remove existing setup files to simulate first-time run
    setup_complete_file = Path(__file__).parent / '.setup_complete'
    env_file = Path(__file__).parent / '.env'
    contacts_file = Path(__file__).parent / 'contacts.json'
    
    if setup_complete_file.exists():
        setup_complete_file.unlink()
        print("✅ Removed existing setup completion marker")
    
    if env_file.exists():
        print(f"📄 Existing .env file found: {env_file}")
        choice = input("Do you want to remove it to test fresh setup? (y/n): ")
        if choice.lower() == 'y':
            env_file.unlink()
            print("✅ Removed existing .env file")
    
    if contacts_file.exists():
        print(f"📞 Existing contacts.json file found: {contacts_file}")
        choice = input("Do you want to remove it to test fresh contacts? (y/n): ")
        if choice.lower() == 'y':
            contacts_file.unlink()
            print("✅ Removed existing contacts.json file")
    
    print("\n🚀 Now importing config module (this will trigger setup)...")
    print("=" * 50)
    
    try:
        # Import config - this will trigger the first-time setup
        from config import config
        
        print("\n✅ Setup completed successfully!")
        print("📧 Email configured:", config.is_email_configured())
        
        # Test contact manager
        print("\n🧪 Testing contact manager...")
        from contacts import contact_manager
        
        print("📞 Current contacts:", len(contact_manager.contacts))
        
        # Test adding a contact programmatically
        contact_manager.add_contact("Test User", "test@example.com")
        print("✅ Test contact added successfully")
        
        print("\n🎉 All tests passed! The setup functionality is working correctly.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_setup_info():
    """Show information about the setup files created"""
    print("\n📂 Setup Files Created:")
    print("=" * 30)
    
    setup_files = [
        ('.env', 'Environment configuration'),
        ('.setup_complete', 'Setup completion marker'),
        ('contacts.json', 'Contact database'),
        ('voice_assistant.log', 'Application logs')
    ]
    
    for filename, description in setup_files:
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            print(f"✅ {filename:<20} - {description}")
        else:
            print(f"❌ {filename:<20} - {description} (missing)")

if __name__ == "__main__":
    print("🎤 Rishi Voice Assistant - Setup Test")
    print("=" * 40)
    
    success = test_first_time_setup()
    
    if success:
        show_setup_info()
        print("\n🎯 Next Steps:")
        print("1. Run: python SpeakAssistant.py")
        print("2. Try voice commands like:")
        print("   - 'Send email'")
        print("   - 'Add contact'")
        print("   - 'List contacts'")
        print("   - 'Open YouTube'")
    else:
        print("\n❌ Setup test failed. Please check the error messages above.")
