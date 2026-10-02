from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)
attendance_logs = []
device_info = {}

HTML = """
<!DOCTYPE html>
<html><head><title>ZK Cloud LIVE</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:sans-serif;background:#0f172a;color:white;padding:20px}
.card{background:#1e293b;padding:15px;border-radius:12px;margin:10px 0}
h1{color:#38bdf8}
.badge{background:#22c55e;padding:5px 10px;border-radius:20px;font-size:12px}
table{width:100%;border-collapse:collapse}
th,td{padding:10px;text-align:left;border-bottom:1px solid #334155}
</style>
<script>setTimeout(()=>location.reload(),10000)</script>
</head><body>
<h1>ZK Cloud LIVE Attendance</h1>
<p><span class="badge">CLOUD CONNECTED</span> Auto refresh 10 sec</p>
<div class="card">Total: {{logs|length}} | Device: {{device}}</div>
<div class="card">
<table><tr><th>Time</th><th>User ID</th><th>Data</th></tr>
{% for l in logs[::-1][:100] %}
<tr><td>{{l.time}}</td><td>{{l.user}}</td><td>{{l.type}}</td></tr>
{% endfor %}
</table>
</div>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, logs=attendance_logs, device=device_info.get('sn','Not Connected'))

@app.route('/iclock/cdata', methods=['GET','POST'])
def cdata():
    data = request.data.decode('utf-8', errors='ignore') if request.data else ''
    args = request.args
    print(f"PUSH Args:{args} Data:{data[:500]}")
    if data:
        for line in data.strip().split('\n'):
            if line.strip():
                parts = line.replace(',', '\t').split('\t')
                attendance_logs.append({
                    'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'user': parts[0].strip() if parts else 'Unknown',
                    'type': line[:100]
                })
    device_info['sn'] = args.get('SN','Unknown')
    return "OK"

@app.route('/iclock/getrequest', methods=['GET','POST'])
def getrequest():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
