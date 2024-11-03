from flask import Flask, request
import datetime
import socket
import netifaces as ni
import os

app = Flask(__name__)

def get_mac_address():
    try:
        # Try common interface names in containers
        interfaces = ['eth0', 'en0', 'ens33', 'ens5']
        
        for iface in interfaces:
            if iface in ni.interfaces():
                addr = ni.ifaddresses(iface)
                if ni.AF_LINK in addr:
                    return addr[ni.AF_LINK][0]['addr']
                elif ni.AF_PACKET in addr:
                    return addr[ni.AF_PACKET][0]['addr']
        
        # Fallback: try to get any interface
        for iface in ni.interfaces():
            if iface != 'lo':  # Skip loopback
                addr = ni.ifaddresses(iface)
                if ni.AF_LINK in addr:
                    return addr[ni.AF_LINK][0]['addr']
                elif ni.AF_PACKET in addr:
                    return addr[ni.AF_PACKET][0]['addr']
                
        return "MAC address not available"
    except Exception as e:
        return f"Error getting MAC address: {str(e)}"

@app.route('/')
def user_info():
    user_ip = request.remote_addr
    
    username = request.headers.get('Username', 'Guest')
    
    mac_address = get_mac_address()
    hostname = socket.gethostname()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    debug_info = {
        'interfaces': ni.interfaces(),
        'hostname': hostname,
        'container_id': os.popen('cat /etc/hostname').read().strip()
    }

    return f"""
    <html>
    <body>
        <h2>User Information</h2>
        <p><b>IP Address:</b> {user_ip}</p>
        <p><b>MAC Address:</b> {mac_address}</p>
        <p><b>Username:</b> {username}</p>
        <p><b>Timestamp:</b> {timestamp}</p>
        <br>
        <h3>Assignment completed successfully!</h3>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)