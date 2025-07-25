# Simple test to make sure our config works
import sys
sys.path.append('src')

from utils.config import PACKET_SIZE, TIMEOUT, PKT_DATA

print("✅ Configuration loaded successfully!")
print(f"Packet size: {PACKET_SIZE} bytes")
print(f"Timeout: {TIMEOUT} seconds") 
print(f"Data packet type: {PKT_DATA}")