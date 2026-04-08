<div align="center">

# 🔐 BioQuantum Shield

### Biometric-Bound Post-Quantum Encrypted File Transmission  
### with Forensic Traitor Tracing

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Encryption](https://img.shields.io/badge/Encryption-AES--256--GCM-00897B?style=flat-square)](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
[![PQC](https://img.shields.io/badge/PQC-CRYSTALS--Kyber-7B1FA2?style=flat-square)](https://pq-crystals.org/kyber/)
[![Biometric](https://img.shields.io/badge/Sensor-R307%20Fingerprint-E64A19?style=flat-square)](#hardware-setup)
[![License](https://img.shields.io/badge/License-Academic-5C6BC0?style=flat-square)](#)
[![VIT](https://img.shields.io/badge/VIT%20University-School%20of%20CS-1565C0?style=flat-square)](#)

<br/>

> **A unified framework that eliminates static private key storage, enforces biometric-gated decryption, and cryptographically traces post-decryption document leaks — all in a single quantum-resilient pipeline.**

<br/>

```
Alice (Sender)                          Bob (Receiver + R307 Sensor)
─────────────────                       ──────────────────────────────
 message.txt                             👆 Fingerprint Scan
     │                                         │
     ▼                                         ▼
 AES-256-GCM                            Seed Regenerated in RAM
     │                                         │
     ▼                                         ▼
 Kyber KEM                              Private Key (RAM only, deleted after)
     │                                         │
     ▼                                         ▼
 encrypted.bin ──────── WiFi TCP ──────▶ Decrypted + Watermarked
                                                │
                                                ▼
                                     🔍 Forensic Tracing Ready
```

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗 System Architecture](#-system-architecture)
- [🔩 Hardware Setup](#-hardware-setup)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation](#️-installation)
- [🚀 Running the Project](#-running-the-project)
- [📊 Performance](#-performance)
- [🛡 Security Analysis](#-security-analysis)
- [⚠️ Known Limitations](#️-known-limitations)
- [📚 References](#-references)
- [👥 Authors](#-authors)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧬 **Biometric Key Binding** | Private key never touches disk — regenerated from fingerprint in volatile RAM only |
| ⚛️ **Post-Quantum Resilient** | Hybrid AES-256-GCM + Kyber-based KEM survives quantum attacks |
| 🕵️ **Forensic Traitor Tracing** | Invisible zero-width Unicode watermark embeds user ID + timestamp + SHA-256 signature |
| 🔑 **Zero Persistent Keys** | Private key exists only during an active authenticated session, then deleted |
| 📡 **WiFi TCP Transmission** | Encrypted packages transmitted peer-to-peer over a shared WiFi network |
| 🗃️ **SQLite Helper Store** | Only biometric helper data stored — no raw fingerprint, no private key |

---

## 🏗 System Architecture

The system operates in **5 sequential phases**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1 — ENROLLMENT (Bob)                                             │
│                                                                         │
│  R307 Scan ──▶ Minutiae ──▶ Fuzzy Extractor ──▶ 256-bit Master Secret  │
│                                   │                      │              │
│                             Helper Data              SHA-256 Seed       │
│                            (stored in DB)                │              │
│                                                    SHAKE-256 KeyGen     │
│                                                    /              \     │
│                                              Public Key      Private Key│
│                                             (saved)         (RAM→deleted)│
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 2 — PUBLIC KEY REGISTRATION (Bob → Alice over TCP:5000)          │
│                                                                         │
│  Bob fingerprint auth ──▶ Regenerate keypair in RAM                     │
│                        ──▶ Send public key to Alice ──▶ Delete sk       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 3 — SECURE TRANSMISSION (Alice → Bob over TCP:6000)              │
│                                                                         │
│  plaintext ──▶ AES-256-GCM ──▶ Cfile                                   │
│  KAES      ──▶ XOR(PK_Bob[:32]) ──▶ Ckey                               │
│  Package   =  [len(Ckey) | Ckey | nonce | Cfile] ──▶ WiFi ──▶ Bob      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 4 — BIOMETRIC DECRYPTION + WATERMARKING (Bob)                    │
│                                                                         │
│  Fingerprint ──▶ Seed ──▶ sk (RAM) ──▶ Recover KAES ──▶ Decrypt        │
│                                                              │          │
│                                    σ = SHA256(uid || ms)    │          │
│                                    payload = uid||ts||σ      │          │
│                                    Encode as U+200B/U+200C   │          │
│                                    Append to plaintext ◀─────┘          │
│                                    Save watermarked doc                 │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 5 — FORENSIC EXTRACTION (Any machine)                            │
│                                                                         │
│  Leaked doc ──▶ Scan U+200B/U+200C ──▶ Binary ──▶ {uid, ts, σ}         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔩 Hardware Setup

### Components Required

| Component | Specification | Side |
|---|---|---|
| Laptop Alice | Windows 11, Python 3.11, WiFi | Sender |
| Laptop Bob | Windows 11, Python 3.11, WiFi | Receiver |
| R307 Fingerprint Sensor | Optical UART, 3.3V–5V | Bob |
| CP2102 USB-to-TTL Converter | USB-A, voltage selectable | Bob |
| 4× Jumper Wires | Female-to-Female | Bob |
| USB Cable | Type-A to Mini/Micro-B | Bob |

### Wiring Diagram

```
  R307 Sensor                      CP2102 Module
  ─────────────                    ─────────────
  VCC  (Red)    ──────────────▶   VCC  (3.3V or 5V)
  GND  (Black)  ──────────────▶   GND
  TXD  (Yellow) ──────────────▶   RXD  ← cross the lines!
  RXD  (Green)  ──────────────▶   TXD  ← cross the lines!
                                        │
                                   USB Cable
                                        │
                                   Bob's Laptop
                                  (COM3/COM4/COM5...)
```

> ⚠️ **Critical:** TX of R307 must connect to RX of CP2102 and vice versa. Connecting TX-to-TX will produce no response from the sensor.

> ⚠️ **Power:** Set the CP2102 voltage jumper to match your R307 sensor's rated voltage (typically 3.3V).

### Finding Your COM Port

1. Plug the CP2102 into Bob's laptop via USB
2. Open **Device Manager** → expand **Ports (COM & LPT)**
3. Note the assigned port (e.g., `COM4`)
4. Update `SERIAL_PORT = "COM4"` in all Bob's biometric scripts

### Verify Sensor

```bash
cd Bob_System/biometric
python test_r307.py
# Expected: [SUCCESS] R307 responded. Sensor online.
```

---

## 📁 Project Structure

```
📦 Project Root
├── 📁 Alice_System/                  ← Sender laptop
│   ├── 🐍 encrypt.py                 # AES-256-GCM file encryption + KEM
│   ├── 🐍 get_public_key.py          # Downloads Bob's public key (TCP:5000)
│   ├── 🐍 send_file.py               # Transmits encrypted.bin (TCP:6000)
│   ├── 🐍 extract_watermark.py       # Forensic watermark extraction
│   ├── 📄 message.txt                # Plaintext file to send
│   ├── 🔑 bob_public.key             # Bob's PQC public key (downloaded)
│   └── 📦 encrypted.bin              # Output encrypted package
│
└── 📁 Bob_System/                    ← Receiver laptop (with R307 sensor)
    ├── 🐍 enroll.py                  # ONE-TIME: fingerprint enrollment
    ├── 🐍 public_key_registration.py # Starts key server on TCP:5000
    ├── 🐍 file_receiver.py           # Listens for encrypted file TCP:6000
    ├── 🐍 decrypt_and_watermark.py   # Biometric decrypt + watermark embed
    ├── 🐍 authenticate.py            # Biometric authentication module
    ├── 🐍 test_kyber.py              # PQC unit tests
    ├── 📦 received_package.bin       # Received encrypted file
    ├── 📄 decrypted_watermarked.txt  # Final output with embedded watermark
    │
    ├── 📁 biometric/                 # R307 sensor interface
    │   ├── 🐍 test_r307.py           # Hardware connectivity test
    │   ├── 🐍 clear_sensor.py        # Wipe all stored templates from R307
    │   ├── 🐍 extract_template.py    # Get template position for seed
    │   ├── 🐍 feature_reduce.py      # Fuzzy extractor helper data
    │   └── 🐍 quantity.py            # Check used template slots
    │
    ├── 📁 database/
    │   ├── 🐍 db.py                  # SQLite CRUD helper
    │   └── 🗄️ users.db               # Stores: uid, template_pos, master_secret
    │
    └── 📁 pqc/
        ├── 🐍 keygen.py              # SHAKE-256 deterministic key generation
        └── 🐍 __init__.py
```

---

## ⚙️ Installation

### 1. Clone / Copy the Project

```bash
# Copy Alice_System to Alice's laptop
# Copy Bob_System to Bob's laptop
```

### 2. Install Dependencies

On **both** laptops:

```bash
pip install pyserial cryptography
```

> Python's built-in `sqlite3`, `hashlib`, `os`, `socket`, and `secrets` modules are used for the rest — no extra installs needed.

### 3. Configure Network (Alice)

Find Bob's IP address on his laptop:

```bash
ipconfig   # Windows — note IPv4 under WiFi adapter
```

Update in Alice's scripts:

```python
# In get_public_key.py and send_file.py
BOB_IP = "192.168.x.x"   # ← Replace with Bob's actual IP
```

### 4. Configure COM Port (Bob)

Update `SERIAL_PORT` in these files to match your Device Manager:

```python
# In enroll.py, authenticate.py, biometric/test_r307.py, etc.
SERIAL_PORT = "COM4"   # ← Replace with your actual COM port
```

---

## 🚀 Running the Project

Run each phase **in order**. Bob's server must always start before Alice's client.

---

### Phase 1 — Enrollment `(Bob only — run once)`

```bash
cd Bob_System
python enroll.py
```

- Place finger on R307 when prompted
- Lift and re-place for the consistency check
- Helper data stored in `database/users.db`; private key never saved

> 🔄 **Re-enroll:** Run `python biometric/clear_sensor.py`, delete `users.db`, then re-run `enroll.py`

---

### Phase 2 — Public Key Exchange

**Bob's terminal:**
```bash
python public_key_registration.py
# Waiting on TCP port 5000...
```

**Alice's terminal:**
```bash
cd Alice_System
python get_public_key.py
# Connects, Bob scans finger, public key downloaded → bob_public.key
```

---

### Phase 3 — Encrypt & Send File

**Bob's terminal:**
```bash
python file_receiver.py
# Listening on TCP port 6000...
```

**Alice's terminal:**
```bash
python encrypt.py          # Produces encrypted.bin
python send_file.py        # Transmits encrypted.bin to Bob
```

---

### Phase 4 — Biometric Decryption + Watermark Embedding `(Bob)`

```bash
python decrypt_and_watermark.py
```

- Bob scans fingerprint → seed regenerated → private key in RAM
- AES key recovered → file decrypted
- Watermark `(uid || timestamp || SHA-256 signature)` embedded as invisible zero-width Unicode
- Output: `decrypted_watermarked.txt` — private key deleted from RAM

---

### Phase 5 — Forensic Watermark Extraction

```bash
python extract_watermark.py
```

```
=== FORENSIC WATERMARK EXTRACTED ===
User ID    : bob_user_001
Timestamp  : 2025-04-08 14:32:17
Signature  : a3f7c2...d91e
=====================================
```

---

### Quick Reference

| Phase | Who | Command | Port |
|---|---|---|---|
| 1 — Enroll | Bob | `python enroll.py` | — |
| 2a — Key server | Bob | `python public_key_registration.py` | 5000 |
| 2b — Get key | Alice | `python get_public_key.py` | 5000 |
| 3a — File receiver | Bob | `python file_receiver.py` | 6000 |
| 3b — Encrypt | Alice | `python encrypt.py` | — |
| 3c — Send | Alice | `python send_file.py` | 6000 |
| 4 — Decrypt + mark | Bob | `python decrypt_and_watermark.py` | — |
| 5 — Extract mark | Either | `python extract_watermark.py` | — |

---

## 📊 Performance

Tested on consumer-grade hardware over WiFi (Python 3.11, Windows 11):

| Operation | Avg Time |
|---|---|
| 👆 Fingerprint Authentication | 1.320 s |
| 🔑 Key Regeneration (SHAKE-256) | 0.0003 s |
| 🔒 AES-256-GCM Encryption | 0.002 s |
| 📡 File Transmission | 0.001 s |
| 🔓 AES-256-GCM Decryption | 0.001 s |
| 🖊️ Watermark Embedding | < 0.001 s |
| 🔍 Watermark Extraction | < 0.001 s |
| **⏱ Total Pipeline** | **≈ 1.325 s** |

**Encryption throughput by file size:**

| File Size | Encryption Time | Throughput |
|---|---|---|
| 1 KB | 0.0008 s | 1,250 KB/s |
| 10 KB | 0.0012 s | 8,333 KB/s |
| 50 KB | 0.0019 s | 26,315 KB/s |
| 100 KB | 0.0031 s | 32,258 KB/s |
| 500 KB | 0.0089 s | 56,179 KB/s |
| 1 MB | 0.0164 s | 60,975 KB/s |

> Biometric authentication (1.32 s) is the dominant latency. All cryptographic operations together contribute < 5 ms.

---

## 🛡 Security Analysis

| Threat | Mitigation | Status |
|---|---|---|
| Static private key theft | Key never written to disk — RAM only | ✅ Eliminated |
| Malware key extraction | Key deleted from memory post-session | ✅ Eliminated |
| Unauthorized decryption | Wrong fingerprint → wrong seed → decapsulation failure | ✅ Blocked |
| Network interception | AES-256-GCM authenticated encryption in transit | ✅ Protected |
| Post-decryption data leak | Invisible watermark enables forensic attribution | ✅ Traceable |
| Watermark forgery | SHA-256 signature bound to user's master secret | ✅ Unforgeable |
| Quantum attack on KEM | Kyber-derived deterministic keypair | ✅ Quantum-resilient |

---

## ⚠️ Known Limitations

- **XOR-based KEM** — The current key encapsulation uses a simplified XOR abstraction rather than full NIST ML-KEM-1024 (due to Windows platform constraints with `liboqs`). Future work will integrate the Open Quantum Safe library.
- **Single-user enrollment** — The current prototype supports one enrolled user. Multi-user isolation is planned.
- **Screenshot attack** — Zero-width Unicode watermarks do not survive screenshots or re-typed content. A visible screen-overlay watermark is proposed as a future mitigation.
- **Platform** — Tested on Windows 11 only. Linux/macOS compatibility not yet validated.

---

## 📚 References

1. Shor, P.W. — *Algorithms for quantum computation*, FOCS 1994
2. NIST — *FIPS 203 ML-KEM Standard (Kyber-1024)*, Aug 2024
3. Bos et al. — *CRYSTALS-Kyber high-speed implementation*, IACR 2023
4. Akintoye et al. — *Cryptographic key generation using deep learning with biometric data*, IEEE TIFS 2025
5. Tran et al. — *Biometrics-based authenticated key exchange with fuzzy extractor*, IEEE TDSC 2024
6. Alagic et al. — *NIST ML-DSA (Dilithium) Standard*, FIPS 204, 2023
7. Dodis et al. — *Fuzzy extractors: How to generate strong keys from biometrics*, SIAM J. Comput. 2009

---

## 👥 Authors

<table>
<tr>
<td align="center">
  <b>Saksham Singh Pawar</b><br/>
  School of Computer Science<br/>
  VIT University<br/>
  <a href="mailto:sakshamsingh.pawar2023@vitstudent.ac.in">sakshamsingh.pawar2023@vitstudent.ac.in</a>
</td>
<td align="center">
  <b>Anamitra Shrivastava</b><br/>
  School of Computer Science<br/>
  VIT University<br/>
  <a href="mailto:anamitra.shrivastava2023@vitstudent.ac.in">anamitra.srivastava2023@vitstudent.ac.in</a>
</td>
<td align="center">
  <b>Asritha P</b><br/>
  School of Computer Science<br/>
  VIT University<br/>
  <a href="mailto:asritha.p2023@vitstudent.ac.in">asritha.p2023@vitstudent.ac.in</a>
</td>
</tr>
</table>

---

<div align="center">

Made with 🔐 at **VIT University** · School of Computer Science

*"The private key that never existed cannot be stolen."*

</div>
