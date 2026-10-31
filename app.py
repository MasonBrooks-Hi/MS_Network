import subprocess
import json
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

BACKUP_FILE = "network_backup.json"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/en')
def index_en():
    return send_from_directory('.', 'index_en.html')

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_services():
    services = run_command("networksetup -listallnetworkservices").split("\n")
    return [s for s in services if s and not s.startswith("*")]

def get_active_service():
    services = get_services()
    for service in services:
        info = run_command(f"networksetup -getinfo '{service}'")
        if "IP address:" in info and not "IP address: none" in info:
            return service
    return services[0] if services else None

@app.route('/api/status', methods=['GET'])
def status():
    service = get_active_service()
    if not service:
        return jsonify({"error": "No active network service found"}), 404
    
    info = run_command(f"networksetup -getinfo '{service}'")
    dns = run_command(f"networksetup -getdnsservers '{service}'")
    web_proxy = run_command(f"networksetup -getwebproxy '{service}'")
    secure_proxy = run_command(f"networksetup -getsecurewebproxy '{service}'")
    
    return jsonify({
        "service": service,
        "info": info,
        "dns": dns if "There aren't any DNS Servers" not in dns else "Automatic",
        "web_proxy": web_proxy,
        "secure_proxy": secure_proxy
    })

@app.route('/api/backup', methods=['POST'])
def backup():
    service = get_active_service()
    if not service:
        return jsonify({"error": "No active network service found"}), 404
    
    dns = run_command(f"networksetup -getdnsservers '{service}'")
    web_proxy = run_command(f"networksetup -getwebproxy '{service}'")
    secure_proxy = run_command(f"networksetup -getsecurewebproxy '{service}'")
    
    backup_data = {
        "service": service,
        "dns": dns,
        "web_proxy": web_proxy,
        "secure_proxy": secure_proxy
    }
    
    with open(BACKUP_FILE, "w") as f:
        json.dump(backup_data, f)
    
    return jsonify({"message": "Backup created successfully"})

@app.route('/api/restore', methods=['POST'])
def restore():
    if not os.path.exists(BACKUP_FILE):
        return jsonify({"error": "No backup found"}), 404
    
    try:
        with open(BACKUP_FILE, "r") as f:
            data = json.load(f)
        
        service = data['service']
        
        dns = data['dns']
        if "There aren't any DNS Servers" in dns or not dns:
            run_command(f"networksetup -setdnsservers '{service}' Empty")
        else:
            run_command(f"networksetup -setdnsservers '{service}' {dns.replace('\\n', ' ')}")
            
        run_command(f"networksetup -setwebproxystate '{service}' off")
        run_command(f"networksetup -setsecurewebproxystate '{service}' off")
        
        return jsonify({"message": "Restored to backup successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cert', methods=['POST'])
def add_cert():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    cert_path = os.path.join("/tmp", file.filename)
    file.save(cert_path)
    
    cmd = f"security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain '{cert_path}'"
    result = run_command(cmd)
    
    return jsonify({"message": "Certificate addition attempted", "details": result})

@app.route('/api/config', methods=['POST'])
def update_config():
    data = request.json
    service = get_active_service()
    
    if 'dns' in data:
        dns_str = data['dns']
        run_command(f"networksetup -setdnsservers '{service}' {dns_str}")
        
    if 'proxy' in data:
        proxy = data['proxy']
        run_command(f"networksetup -setwebproxy '{service}' {proxy['host']} {proxy['port']}")
        run_command(f"networksetup -setsecurewebproxy '{service}' {proxy['host']} {proxy['port']}")
        
    return jsonify({"message": "Configuration updated"})

def flush_dns():
if __name__ == '__main__':
    app.run(port=5000)
