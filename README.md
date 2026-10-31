# MS Network

[中文版本](README_CN.md)

MS Network is a modern, lightweight utility designed for macOS users to manage local network configurations, certificates, and monitor network status with ease. It provides a clean web-based interface to perform system-level network operations.

## Features
- **Network Monitoring**: Real-time view of active network services, IP addresses, and DNS settings.
- **Config Management**: Easily modify DNS servers and HTTP/HTTPS proxy settings.
- **Certificate Installer**: Install and trust local root certificates with one click.
- **One-Click Restore**: Backup your initial network settings and restore them anytime to avoid configuration errors.

## Tech Stack
- **Backend**: Python 3.15 + Flask
- **Frontend**: React 18 + Tailwind CSS (Modern UI)
- **System Integration**: macOS `networksetup` and `security` CLI tools.

## How to Run
1. Ensure you have Python 3 installed.
2. Install dependencies:
   ```bash
   pip install flask flask-cors
   ```
3. Start the backend:
   ```bash
   python3 app.py
   ```
4. Open `index.html` in your browser or visit `http://localhost:5000`.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
