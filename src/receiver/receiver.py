"""
Reliable UDP receiver implementation.
Handles incoming packets and reconstructs files.
"""

import socket
import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from protocol.packet import Packet, PacketType, create_ack_packet
from utils.config import *

class ReliableReceiver:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.expected_seq = 1
        
    def receive_file(self, output_path):
        """Receive file and save to specified path"""
        print(f"Listening on {self.host}:{self.port}")
        print(f"Will save received file to: {output_path}")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        connection_started = False
        
        with open(output_path, 'wb') as output_file:
            while True:
                try:
                    # Receive packet from network
                    data, sender_addr = self.socket.recvfrom(PACKET_SIZE)
                    print(f"Received {len(data)} bytes from {sender_addr}")
                    
                    try:
                        packet = Packet.deserialize(data)
                        print(f"Deserialized: {packet}")
                    except Exception as e:
                        print(f"Error deserializing packet: {e}")
                        continue
                    
                    if packet.is_start_packet():
                        # Connection start
                        connection_started = True
                        print("✓ START packet received - Connection established")
                        
                        # Send ACK for START packet
                        ack_packet = create_ack_packet(0)
                        self.socket.sendto(ack_packet.serialize(), sender_addr)
                        print(f"✓ Sent START ACK to {sender_addr}")
                        
                    elif packet.is_data_packet():
                        print(f"Processing DATA packet: seq={packet.seq_num}, expected={self.expected_seq}")
                        
                        if not connection_started:
                            print("⚠️  DATA packet before START - auto-establishing connection")
                            connection_started = True
                            
                        if packet.seq_num == self.expected_seq:
                            # Correct sequence - write data to file
                            output_file.write(packet.data)
                            output_file.flush()
                            print(f"✓ Wrote {len(packet.data)} bytes to file")
                            
                            # Send ACK back to sender
                            ack_packet = create_ack_packet(packet.seq_num)
                            self.socket.sendto(ack_packet.serialize(), sender_addr)
                            print(f"✓ Sent ACK {packet.seq_num} to {sender_addr}")
                            
                            # Update expected sequence number
                            self.expected_seq += 1
                        else:
                            print(f"⚠️  Out of order packet: expected {self.expected_seq}, got {packet.seq_num}")
                            # Send ACK for the last correctly received packet
                            ack_packet = create_ack_packet(self.expected_seq - 1)
                            self.socket.sendto(ack_packet.serialize(), sender_addr)
                            print(f"✓ Sent duplicate ACK {self.expected_seq - 1}")
                            
                    elif packet.is_fin_packet():
                        # Connection end
                        print("✓ FIN packet received - File transfer complete")
                        
                        # Send ACK for FIN packet
                        ack_packet = create_ack_packet(0)
                        self.socket.sendto(ack_packet.serialize(), sender_addr)
                        print(f"✓ Sent FIN ACK to {sender_addr}")
                        break
                        
                except Exception as e:
                    print(f"Error processing packet: {e}")
                    continue
        
        print(f"✓ File saved successfully to {output_path}")
        return True
    
    def close(self):
        """Close the receiver"""
        self.socket.close()
        print("Receiver closed")
