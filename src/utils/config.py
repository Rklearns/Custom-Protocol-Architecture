"""
Configuration constants for our reliable UDP protocol.

This file contains all the important settings and parameters
that control how our protocol behaves.
"""

# =============================================================================
# PACKET SIZE SETTINGS
# =============================================================================

PACKET_SIZE = 1024      # Total size of each UDP packet in bytes
HEADER_SIZE = 20        # Size of our custom header
DATA_SIZE = PACKET_SIZE - HEADER_SIZE  # Actual file data per packet (1004 bytes)

# =============================================================================
# NETWORK SETTINGS  
# =============================================================================

DEFAULT_PORT = 8888     # Port number for our file transfer
DEFAULT_HOST = 'localhost'  # Default host for testing

# =============================================================================
# RELIABILITY SETTINGS
# =============================================================================

TIMEOUT = 2.0          # How long to wait before resending a packet (seconds)
WINDOW_SIZE = 5        # How many packets we can send without waiting for ACK
MAX_RETRIES = 5        # How many times to retry before giving up

# =============================================================================
# PACKET TYPES - Different kinds of messages in our protocol
# =============================================================================

PKT_DATA = 0          # Regular data packet (carries file content)
PKT_ACK = 1           # Acknowledgment packet (confirms receipt)
PKT_START = 2         # Start connection packet
PKT_FIN = 3           # End connection packet

# =============================================================================
# DEBUG SETTINGS
# =============================================================================

DEBUG_MODE = True     # Print detailed information
