"""
Simple test for the receiver functionality
"""

import sys
import os

# Add src directory to Python path
sys.path.append('src')

from receiver.receiver import ReliableReceiver

def main():
    print("🚀 Starting UDP file receiver test")
    
    # Create receiver
    receiver = ReliableReceiver("localhost", 8888)
    
    try:
        # Receive file and save as received_file.txt
        success = receiver.receive_file("received_file.txt")
        
        if success:
            print("🎉 Receiver test completed successfully!")
            
            # Check if file was created and show its contents
            if os.path.exists("received_file.txt"):
                with open("received_file.txt", "rb") as f:
                    content = f.read()
                print(f"📄 Received file content ({len(content)} bytes):")
                print(content.decode('utf-8'))
        else:
            print("❌ Receiver test failed!")
            
    except KeyboardInterrupt:
        print("\n🛑 Receiver stopped by user")
    finally:
        receiver.close()

if __name__ == "__main__":
    main()
