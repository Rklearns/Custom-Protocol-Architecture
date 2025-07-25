import sys
import os
sys.path.append('src')

from sender.sender import ReliableSender

def main():
    # Create multi-packet test file
    content = ""
    for i in range(8):  # 8 packets
        chunk_content = f"Packet {i:02d}: " + "A" * 990 + "\n"
        content += chunk_content

    with open("multi_packet_test.txt", "w") as f:
        f.write(content)

    file_size = len(content.encode())
    print(f"Created test file with {file_size} bytes (~{file_size//1004 + 1} packets)")

    # Send the multi-packet file
    sender = ReliableSender("localhost", 8888)

    try:
        success = sender.send_file("multi_packet_test.txt")
        if success:
            print("✓ Multi-packet transfer completed successfully!")
        else:
            print("✗ Multi-packet transfer failed!")
    finally:
        sender.close()
        # Clean up
        if os.path.exists("multi_packet_test.txt"):
            os.remove("multi_packet_test.txt")

if __name__ == "__main__":
    main()
