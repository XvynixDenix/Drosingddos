# 🌊 DDOS DROSING TOOLS - D3N!X

**Multi-Method DDoS Testing Tool for Educational Purposes**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Educational-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()

---

## ⚖️ DISCLAIMER & TANGGUNG JAWAB

> **PERINGATAN HUKUM!**
>
> Tools ini dibuat **SEMATA-MATA UNTUK EDUKASI** dan **PENGUJIAN KEAMANAN**.
>
> **DENIX TIDAK BERTANGGUNG JAWAB ATAS:**
> - Penyalahgunaan tools ini untuk serangan ilegal
> - Kerusakan atau kerugian yang ditimbulkan
> - Tindakan hukum yang dihadapi pengguna
> - Pelanggaran UU ITE atau hukum yang berlaku
>
> **Menggunakan tools ini berarti Anda:**
> 1. Telah membaca dan memahami disclaimer ini
> 2. Bertanggung jawab penuh atas tindakan Anda
> 3. Hanya akan menguji sistem yang Anda miliki atau memiliki izin tertulis
> 4. Menerima segala risiko hukum yang mungkin timbul
>
> **Ancaman Hukum (UU ITE Pasal 33 ayat 2-3):**

---

## 📋 Table of Contents

- [Disclaimer & Tanggung Jawab](#-disclaimer--tanggung-jawab)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Attack Methods](#-attack-methods)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Requirements](#-requirements)
- [FAQ](#-faq)
- [Legal Notice](#-legal-notice)

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **13 Attack Methods** | HTTP, UDP, Slowloris, DNS Amplification, SYN Flood, SSL Renegotiation, and more |
| **Multi-Threading** | Configurable thread count (1-2000) |
| **Proxy Support** | Auto-fetch proxies from multiple sources |
| **Real-time Stats** | Request count, error rate, bandwidth usage, success rate |
| **Auto-Save Logs** | All attacks logged with timestamps |
| **Cross-Platform** | Works on Termux (Android), Linux, Windows |
| **User-Agent Rotation** | Random User-Agent & Referer headers |

---

## 📦 Installation

### Termux (Android)
```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/yourusername/drosingddos.git
cd drosingddos
pip install requests
python drosing.py
