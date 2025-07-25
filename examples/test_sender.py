"""
Simple test for the basic sender functionality
"""

import sys
import os

# Add src directory to Python path
sys.path.append('src')

from sender.sender import ReliableSender

def main():
    # Create a test file
    test_content = b"Hello, this is a test file for our reliable UDP protocol!\nThis content will be sent packet by packet.\nLet's see if it works!"

    with open("test_file.txt", "wb") as f:
        f.write(test_content)

    print("📁 Created test file with", len(test_content), "bytes")

    # Create sender and send file
    sender = ReliableSender("localhost", 8888)

    try:
        success = sender.send_file("test_file.txt")
        if success:
            print("🎉 Sender test completed successfully!")
        else:
            print("❌ Sender test failed!")
    finally:
        sender.close()
        # Clean up test file
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")

if __name__ == "__main__":
    main()
