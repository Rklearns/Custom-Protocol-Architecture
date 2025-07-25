"""
Reliable UDP sender implementation with sliding window protocol.
Handles file transmission with concurrent sending and ACK processing.
"""

import socket
import threading
import time
import os
import sys
import select

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from protocol.packet import Packet, PacketType, create_data_packet, create_start_packet, create_fin_packet
from utils.config import *
from .window import SlidingWindow

class ReliableSender:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, window_size=WINDOW_SIZE):
        self.host = host
        self.port = port
        
        # Create socket and bind to local port for receiving ACKs
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Bind to a local port so we can receive ACKs
        self.socket.bind(('', 0))
        self.local_addr = self.socket.getsockname()
        print(f"Sender bound to local address: {self.local_addr}")
        
        self.window = SlidingWindow(window_size)
        self.running = False
        self.ack_thread = None
        self.timeout_thread = None
        
    def send_file(self, file_path):
        """Send a file reliably using sliding window protocol"""
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return False
            
        print(f"Starting file transfer: {file_path}")
        self.running = True
        
        # Start background threads
        self._start_background_threads()
        
        try:
            # Send START packet and wait for connection
            if not self._establish_connection():
                print("Failed to establish connection")
                return False
            
            # Send file data using sliding window
            with open(file_path, 'rb') as file:
                while True:
                    # Read next chunk
                    chunk = file.read(DATA_SIZE)
                    if not chunk:
                        break
                    
                    # Wait if window is full
                    while not self.window.can_send():
                        time.sleep(0.01)
                    
                    # Create and send DATA packet
                    data_packet = create_data_packet(0, chunk)  # seq_num assigned by window
                    seq_num = self.window.add_packet(data_packet)
                    
                    self.socket.sendto(data_packet.serialize(), (self.host, self.port))
                    print(f"Sent packet {seq_num}, size: {len(chunk)} bytes")
            
            # Wait for all packets to be acknowledged
            print("Waiting for all packets to be acknowledged...")
            timeout_count = 0
            while not self.window.is_complete():
                time.sleep(0.1)
                timeout_count += 1
                if timeout_count > 100:  # 10 seconds timeout
                    print("Timeout waiting for ACKs")
                    break
            
            # Send FIN packet
            fin_packet = create_fin_packet()
            self.socket.sendto(fin_packet.serialize(), (self.host, self.port))
            print("File transfer complete")
            
            return True
            
        except Exception as e:
            print(f"Error during file transfer: {e}")
            return False
        finally:
            self.running = False
            self._stop_background_threads()
    
    def _establish_connection(self):
        """Send START packet and wait for connection establishment"""
        print("Establishing connection...")
        
        for attempt in range(3):  # Reduced to 3 attempts
            # Send START packet
            start_packet = create_start_packet()
            self.socket.sendto(start_packet.serialize(), (self.host, self.port))
            print(f"Sent START packet (attempt {attempt + 1})")
            
            # Wait for response
            time.sleep(0.5)
            
        print("Connection establishment completed")
        return True
    
    def _start_background_threads(self):
        """Start threads for ACK processing and timeout handling"""
        self.ack_thread = threading.Thread(target=self._ack_handler, daemon=True)
        self.timeout_thread = threading.Thread(target=self._timeout_handler, daemon=True)
        
        self.ack_thread.start()
        self.timeout_thread.start()
        print("Started background threads for ACK and timeout handling")
    
    def _stop_background_threads(self):
        """Wait for background threads to finish"""
        if self.ack_thread and self.ack_thread.is_alive():
            self.ack_thread.join(timeout=1.0)
        if self.timeout_thread and self.timeout_thread.is_alive():
            self.timeout_thread.join(timeout=1.0)
        print("Background threads stopped")
    
    def _ack_handler(self):
        """Background thread to process incoming ACK packets"""
        print("ACK handler thread started")
        
        while self.running:
            try:
                # Use select for non-blocking receive
                ready = select.select([self.socket], [], [], 0.1)
                
                if ready[0]:
                    data, addr = self.socket.recvfrom(PACKET_SIZE)
                    
                    try:
                        ack_packet = Packet.deserialize(data)
                        
                        if ack_packet.is_ack_packet():
                            if ack_packet.ack_num == 0:
                                # START or FIN packet ACK - just acknowledge
                                print(f"✓ Received connection ACK from {addr}")
                            else:
                                # DATA packet ACK - process through sliding window
                                success = self.window.acknowledge_packet(ack_packet.ack_num)
                                if success:
                                    print(f"✓ Successfully processed DATA ACK {ack_packet.ack_num}")
                                else:
                                    print(f"Warning: Failed to process DATA ACK {ack_packet.ack_num}")
                        else:
                            print(f"Received non-ACK packet: {ack_packet}")
                            
                    except Exception as e:
                        print(f"Error deserializing ACK packet: {e}")
                        
            except Exception as e:
                if self.running:
                    print(f"Error in ACK handler: {e}")
        
        print("ACK handler thread stopped")
    
    def _timeout_handler(self):
        """Background thread to handle packet retransmission on timeout"""
        print("Timeout handler thread started")
        
        while self.running:
            try:
                timeout_packets = self.window.get_timeout_packets()
                
                for packet in timeout_packets:
                    self.socket.sendto(packet.serialize(), (self.host, self.port))
                    print(f"Retransmitted packet {packet.seq_num}")
                
                time.sleep(0.1)  # Check for timeouts every 100ms
                
            except Exception as e:
                if self.running:
                    print(f"Error in timeout handler: {e}")
        
        print("Timeout handler thread stopped")
    
    def close(self):
        """Close the sender and cleanup resources"""
        self.running = False
        self.socket.close()
        print("Sender closed")
