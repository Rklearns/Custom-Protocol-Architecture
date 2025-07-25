import sys
sys.path.append('src')
from utils.config import DATA_SIZE

# Create a file that requires multiple packets
content = ""
for i in range(10):  # Create 10 chunks
    # Each chunk will be close to DATA_SIZE (1004 bytes)
    chunk_content = f"Packet {i:02d}: " + "X" * 950 + "\n"
    content += chunk_content

with open("multi_packet_test.txt", "w") as f:
    f.write(content)

file_size = len(content.encode())
packets_needed = (file_size + DATA_SIZE - 1) // DATA_SIZE

print(f"Created file with {file_size} bytes")
print(f"DATA_SIZE: {DATA_SIZE} bytes")
print(f"Estimated packets needed: {packets_needed}")
print(f"With window size 5, should send up to 5 packets simultaneously")
