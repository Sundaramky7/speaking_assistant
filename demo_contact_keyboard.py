#!/usr/bin/env python3
"""
Demo script for the updated contact management functionality
Shows how email addresses are now entered via keyboard instead of speech recognition
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

def demo_keyboard_email_input():
    """Demonstrate the keyboard email input functionality"""
    print("🎤 Rishi Voice Assistant - Contact Management Demo")
    print("=" * 55)
    print("🔧 This demo shows the updated contact functionality where:")
    print("   📝 Contact names: Voice recognition")  
    print("   ⌨️  Email addresses: Keyboard input")
    print("=" * 55)
    
    try:
        from contacts import contact_manager
        
        print("\n🧪 Testing Direct Contact Addition...")
        print("-" * 40)
        
        # Test the prompt_add_new_contact method directly
        print("Simulating: User said 'John Doe' but contact doesn't exist...")
        
        # This will prompt for keyboard input for email
        email, contact_name = contact_manager.prompt_add_new_contact("john doe")
        
        if email and contact_name:
            print(f"✅ Success! Contact added: {contact_name} -> {email}")
        else:
            print("❌ Contact addition was cancelled")
        
        print("\n📞 Current contacts:")
        contact_manager.list_contacts()
        
        print("\n🎯 How this works in the voice assistant:")
        print("1. Say: 'Add contact'")
        print("2. Assistant: 'What is the contact's name?'")
        print("3. You: Say the name (e.g., 'Jane Smith')")
        print("4. Assistant: 'Please type the email address on your keyboard'")
        print("5. You: Type the email (e.g., jane.smith@example.com)")
        print("6. Assistant: 'Contact Jane Smith has been added successfully'")
        
        print("\n🔄 Email sending workflow:")
        print("1. Say: 'Send email'")
        print("2. Assistant: 'Name the Receiver'")  
        print("3. You: Say a name")
        print("4. If contact doesn't exist:")
        print("   - Assistant prompts to add contact")
        print("   - You type 'y' to confirm")
        print("   - You type the email address")
        print("   - Email sending continues normally")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_voice_commands():
    """Show the available voice commands"""
    print("\n📞 Updated Voice Commands:")
    print("=" * 30)
    
    commands = [
        ("Add contact", "Add new contact (name by voice, email by keyboard)"),
        ("Send email", "Send email with smart contact lookup/addition"),
        ("List contacts", "Show all saved contacts"),
        ("Open YouTube", "Open YouTube website"),
        ("Search [query]", "Search Google for anything"),
        ("Wikipedia [topic]", "Get Wikipedia information"),
    ]
    
    for cmd, desc in commands:
        print(f"🎤 '{cmd:<15}' - {desc}")

if __name__ == "__main__":
    success = demo_keyboard_email_input()
    
    if success:
        show_voice_commands()
        
        print("\n🚀 Ready to test!")
        print("Run: python SpeakAssistant.py")
        print("Try: 'Add contact' or 'Send email'")
        
        print("\n💡 Benefits of keyboard email input:")
        print("✅ More accurate email addresses")
        print("✅ Supports special characters and symbols")
        print("✅ No speech recognition errors for emails")
        print("✅ Faster input for complex email addresses")
        print("✅ Visual confirmation of what you're typing")
    else:
        print("\n❌ Demo failed. Please check the setup.")
