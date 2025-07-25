# Custom Protocol Architecture

A high-performance, custom implementation of a reliable transport protocol built on UDP with sliding window flow control, achieving 5.51 MB/s throughput with 100% data integrity.

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Custom implementation of a reliable transport layer protocol demonstrating advanced networking concepts including sliding window flow control, SHA-256 data integrity validation, and multi-threaded concurrent processing. Achieves up to 7,372% performance improvement over stop-and-wait protocols.

## Key Features

- Custom reliable transport protocol built from scratch on UDP
- Sliding window flow control with configurable window sizes
- SHA-256 checksums for cryptographic data integrity
- Multi-threaded architecture with concurrent packet processing
- Perfect reliability (100% success rate in testing)
- Scalable performance (improves with larger files)

## Performance Results

| File Size | Stop-and-Wait | Sliding Window | Improvement |
|-----------|---------------|----------------|-------------|
| 3MB | 0.07 MB/s | 1.52 MB/s | +2,004% |
| 10MB | 0.07 MB/s | 3.85 MB/s | +5,083% |
| 20MB | 0.07 MB/s | 5.51 MB/s | +7,372% |

📊 **[Complete Performance Report](https://github.com/Rklearns/Custom-Protocol-Architecture/blob/main/performance_report_20250725_030019.txt)**

This report contains:
- Detailed methodology and testing environment specifications
- Complete performance metrics for all file sizes and window configurations
- Statistical analysis of sliding window effectiveness
- Technical implementation validation results
- Cross-configuration performance comparisons

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/reliable-udp-transfer.git
cd reliable-udp-transfer
python3 -m venv venv
source venv/bin/activate
```
## 🧪 Basic Usage

### ✅ Option 1: Automated Testing (Recommended)

Run the complete test with both sender and receiver auto-launched:

```bash
python examples/fully_automated_test.py
```

### ✅ Option 2: Manual File Transfer

For manual testing, open **two separate terminals**.

#### 🖥️ Terminal 1 (Receiver)

Start the receiver first:

```bash
python examples/test_receiver.py
```

You should see output like:
```python
[Receiver] Listening on port 5001...
[Receiver] Receiving file: received_output.txt
```

#### 🖥️ Terminal 2 (Sender)

In another terminal, start the sender:

```bash
python examples/test_sender.py
```

Expected output:
```python
[Sender] Sending file: sample_input.txt
[Sender] File transfer complete.
```

### 🔍 What This Does

- Receiver listens for incoming UDP packets.
- Sender sends a test file over UDP.
- Receiver writes received data to a file.
- You can verify file correctness manually or by checksum.

## Configuration

Edit `src/utils/config.py`:

```python
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8888
WINDOW_SIZE = 5       # Sliding window size
TIMEOUT = 2.0         # Packet timeout (seconds)
PACKET_SIZE = 1024    # Total packet size
DATA_SIZE = 1004      # Payload size
```


## Important Limitations

**⚠️ Testing Environment**: This protocol was developed and tested exclusively on **localhost (127.0.0.1)** on a single macOS system with optimal conditions (0% packet loss, <1ms latency).

**Cross-System Deployment**: 
- NOT extensively tested between different computers
- Real network conditions will impact performance significantly
- Additional validation required for production use
- Firewall configuration needed for network deployment

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| macOS | ✅ Fully Tested | Primary development platform |
| Linux | ⚠️ Expected | Standard Python/socket APIs |
| Windows | ⚠️ Limited | May need minor modifications |

## Academic Context

This implementation demonstrates:
- Reliable transport protocol design
- Sliding window flow control mechanisms
- Multi-threaded network programming
- Cryptographic data validation
- Performance optimization techniques

Suitable for computer networks coursework, systems programming education, and network protocol research.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Concepts demonstrated from:
- RFC 793 (TCP specification)
- RFC 768 (UDP specification)  
- Google QUIC protocol design
- Modern reliable transport protocols

---

**Status**: Educational study
**Performance**: 5.51 MB/s peak throughput  
**Reliability**: 100% success rate (localhost testing)  
**Last Updated**: July 2025

### Steps to Contribute

1. **Fork the repository**  
   Click the `Fork` button at the top-right of this page to create your own copy.

2. **Clone your fork locally**

```bash
git clone https://github.com/yourusername/reliable-udp-transfer.git
cd reliable-udp-transfer
```
3. **Create a new branch for your feature or fix
```bash
git checkout -b feature/your-feature-name
```
4. **Edit files, add new code, or fix bugs.

5.Commit Changes
```bash
git add .
git commit -m "Add: meaningful commit message"
```

6.**Push to your fork
```bash
git push origin feature/your-feature-name
```

7.** Proceed with pull request 

## 📚 Academic Citation

**Custom Protocol Architecture: Reliable UDP Implementation**  
**Repository:** [https://github.com/yourusername/reliable-udp-transfer](https://github.com/yourusername/reliable-udp-transfer)  
**Performance:** 5.51 MB/s peak throughput, 7,372% improvement over stop-and-wait  
**Date:** July 2025




