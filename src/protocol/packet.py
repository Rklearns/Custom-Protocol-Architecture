"""
Packet structure and serialization for our reliable UDP protocol.
"""

import struct
import hashlib
from enum import IntEnum

class PacketType(IntEnum):
    DATA = 0
    ACK = 1
    START = 2
    FIN = 3

class Packet:
    HEADER_FORMAT = '!BIIIB6s'
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    
    def __init__(self, packet_type, seq_num=0, ack_num=0, data=b'', flags=0):
        self.packet_type = packet_type
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.data = data
        self.flags = flags
        self.checksum = 0
        
    def calculate_checksum(self):
        content = struct.pack(self.HEADER_FORMAT, 
                            self.packet_type, self.seq_num, self.ack_num, 
                            0, self.flags, b'\x00' * 6) + self.data
        return int(hashlib.sha256(content).hexdigest()[:8], 16)
    
    def serialize(self):
        self.checksum = self.calculate_checksum()
        header = struct.pack(self.HEADER_FORMAT,
                           self.packet_type, self.seq_num, self.ack_num,
                           self.checksum, self.flags, b'\x00' * 6)
        return header + self.data
    
    @classmethod
    def deserialize(cls, data):
        if len(data) < cls.HEADER_SIZE:
            raise ValueError(f"Packet too short: {len(data)} bytes")
            
        header = data[:cls.HEADER_SIZE]
        payload = data[cls.HEADER_SIZE:]
        
        packet_type, seq_num, ack_num, checksum, flags, _ = struct.unpack(cls.HEADER_FORMAT, header)
        
        packet = cls(packet_type, seq_num, ack_num, payload, flags)
        packet.checksum = checksum
        
        if packet.calculate_checksum() != checksum:
            raise ValueError("Checksum mismatch - packet corrupted")
            
        return packet
    
    def is_data_packet(self):
        return self.packet_type == PacketType.DATA
    
    def is_ack_packet(self):
        return self.packet_type == PacketType.ACK
    
    def is_start_packet(self):
        return self.packet_type == PacketType.START
    
    def is_fin_packet(self):
        return self.packet_type == PacketType.FIN
    
    def __str__(self):
        type_name = PacketType(self.packet_type).name
        return f"Packet(type={type_name}, seq={self.seq_num}, ack={self.ack_num}, data_len={len(self.data)})"

def create_data_packet(seq_num, data):
    return Packet(PacketType.DATA, seq_num=seq_num, data=data)

def create_ack_packet(ack_num):
    return Packet(PacketType.ACK, ack_num=ack_num)

def create_start_packet():
    return Packet(PacketType.START)

def create_fin_packet():
    return Packet(PacketType.FIN)
