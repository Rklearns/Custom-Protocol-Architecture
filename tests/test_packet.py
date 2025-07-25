import sys
sys.path.append('src')

from protocol.packet import Packet, PacketType, create_data_packet, create_ack_packet

def test_packet_creation():
    """Test basic packet creation"""
    print("🔍 Testing packet creation...")
    
    # Test DATA packet
    data_packet = create_data_packet(seq_num=5, data=b"Hello World")
    print(f"✅ DATA packet: {data_packet}")
    
    # Test ACK packet  
    ack_packet = create_ack_packet(ack_num=5)
    print(f"✅ ACK packet: {ack_packet}")
    
    print()

def test_serialization_deserialization():
    """Test converting packets to bytes and back"""
    print("🔍 Testing serialization/deserialization...")
    
    # Create a packet with some data
    original_packet = create_data_packet(seq_num=10, data=b"Test file content chunk")
    print(f"Original: {original_packet}")
    
    # Convert to bytes (like sending over network)
    packet_bytes = original_packet.serialize()
    print(f"Serialized to {len(packet_bytes)} bytes")
    
    # Convert back to packet (like receiving from network)
    received_packet = Packet.deserialize(packet_bytes)
    print(f"Deserialized: {received_packet}")
    
    # Verify they're the same
    assert original_packet.packet_type == received_packet.packet_type
    assert original_packet.seq_num == received_packet.seq_num
    assert original_packet.data == received_packet.data
    print("✅ Serialization/deserialization successful!")
    print()

def test_checksum_validation():
    """Test that corrupted packets are detected"""
    print("🔍 Testing checksum validation...")
    
    # Create a packet
    packet = create_data_packet(seq_num=1, data=b"Important data")
    packet_bytes = packet.serialize()
    
    # Corrupt the data (flip a bit)
    corrupted_bytes = packet_bytes[:-1] + b'X'  # Change last byte
    
    # Try to deserialize corrupted packet
    try:
        Packet.deserialize(corrupted_bytes)
        print("❌ Should have detected corruption!")
    except ValueError as e:
        print(f"✅ Corruption detected: {e}")
    
    print()

def test_packet_types():
    """Test all packet types work correctly"""
    print("🔍 Testing packet types...")
    
    # Test each packet type
    packets = [
        (Packet(PacketType.DATA, seq_num=1, data=b"data"), "DATA"),
        (Packet(PacketType.ACK, ack_num=1), "ACK"),
        (Packet(PacketType.START), "START"),
        (Packet(PacketType.FIN), "FIN")
    ]
    
    for packet, expected_type in packets:
        packet_bytes = packet.serialize()
        received = Packet.deserialize(packet_bytes)
        print(f"✅ {expected_type} packet: {received}")
    
    print()

if __name__ == "__main__":
    print("🧪 Running Packet Implementation Tests\n")
    
    try:
        test_packet_creation()
        test_serialization_deserialization() 
        test_checksum_validation()
        test_packet_types()
        
        print("🎉 All tests passed! Packet implementation is working correctly.")
        print("📦 Ready to move on to building the sender component.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("🔧 Fix the issue before proceeding.")
