"""
Sliding window implementation for reliable UDP transmission.
Manages multiple in-flight packets and tracks acknowledgments.
"""

import time
import threading
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.config import WINDOW_SIZE, TIMEOUT

class SlidingWindow:
    """
    Manages the sliding window for reliable packet transmission.
    
    Key concepts:
    - base: oldest unacknowledged packet sequence number
    - next_seq_num: next sequence number to assign to new packets
    - window_size: maximum number of unacknowledged packets allowed
    """
    
    def __init__(self, window_size=WINDOW_SIZE):
        self.window_size = window_size
        self.base = 1  # First packet sequence number
        self.next_seq_num = 1  # Next sequence to assign
        
        # Track in-flight packets: {seq_num: (packet, send_time)}
        self.in_flight = {}
        
        # Thread safety
        self.lock = threading.Lock()
        
        print(f"Sliding window initialized: size={window_size}")
    
    def can_send(self):
        """Check if we can send more packets (window not full)"""
        with self.lock:
            in_flight_count = self.next_seq_num - self.base
            can_send = in_flight_count < self.window_size
            return can_send
    
    def add_packet(self, packet):
        """Add packet to window when sending"""
        with self.lock:
            # Assign sequence number
            packet.seq_num = self.next_seq_num
            
            # Track packet with timestamp
            self.in_flight[self.next_seq_num] = (packet, time.time())
            
            # Move to next sequence number
            self.next_seq_num += 1
            
            print(f"Added packet {packet.seq_num} to window (in-flight: {len(self.in_flight)})")
            return packet.seq_num
    
    def acknowledge_packet(self, ack_num):
        """Process ACK and slide window forward if possible"""
        with self.lock:
            if ack_num in self.in_flight:
                # Remove acknowledged packet
                del self.in_flight[ack_num]
                print(f"✓ ACK received for packet {ack_num}")
                
                # Slide window forward if this was the base packet
                while self.base not in self.in_flight and self.base < self.next_seq_num:
                    self.base += 1
                
                print(f"Window position: base={self.base}, next={self.next_seq_num}, in-flight={len(self.in_flight)}")
                return True
            else:
                print(f"Warning: Received ACK for unknown packet {ack_num}")
                return False
    
    def get_timeout_packets(self):
        """Get packets that need retransmission due to timeout"""
        current_time = time.time()
        timeout_packets = []
        
        with self.lock:
            for seq_num, (packet, send_time) in self.in_flight.items():
                if current_time - send_time > TIMEOUT:
                    # Update send time for retransmission
                    self.in_flight[seq_num] = (packet, current_time)
                    timeout_packets.append(packet)
                    print(f"Packet {seq_num} timed out, needs retransmission")
        
        return timeout_packets
    
    def is_complete(self):
        """Check if all packets have been acknowledged"""
        with self.lock:
            return len(self.in_flight) == 0
    
    def get_status(self):
        """Get current window status for debugging"""
        with self.lock:
            return {
                'base': self.base,
                'next_seq_num': self.next_seq_num,
                'in_flight_count': len(self.in_flight),
                'window_size': self.window_size
            }
