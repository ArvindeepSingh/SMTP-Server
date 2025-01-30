# SMTP Server with Ngrok TCP Tunneling

## Overview
This project implements a **basic SMTP server** using Python's `socket` module. The server listens for incoming TCP connections and processes standard SMTP commands. To make the server accessible over the internet, **Ngrok** is used to provide a public TCP address.

## Features
- Handles SMTP commands: `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`
- Stores email messages locally in a file-based format
- Uses **Ngrok** for tunneling, allowing external access
- Supports TCP connections via `ncat`

---

## Prerequisites
- Python 3.x
- `ncat` (Netcat) installed
- Ngrok installed and authenticated

### Install Ngrok
If you haven't installed Ngrok yet, download it from [Ngrok Official Site](https://ngrok.com/download).

---

## Setup and Usage

### **1. Clone the Repository**
```bash
git clone https://github.com/ArvindeepSingh/smtp-ngrok-server.git
cd smtp-ngrok-server
