from flask import url_for, redirect, render_template, flash, g, session, jsonify
from app import app
import cpuinfo
import psutil
import platform

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/info')
def info():
   osinfo = {}
   osinfo['plat'] = platform
   osinfo['cpu'] = cpuinfo.get_cpu_info()
   osinfo['mem'] = psutil.virtual_memory()
   osinfo['net'] = psutil.net_if_addrs()

   return render_template('info.html', info = osinfo)

@app.route('/monitor')
def monitor():
   return render_template('monitor.html')

apidata = {}

olddata = {}
olddata['disk_write'] = 0
olddata['disk_read'] = 0
olddata['net_sent'] = 0
olddata['net_recv'] = 0
@app.route('/api/monitor')
def api_monitor():
   global net_sent_o 
   apidata['cpu'] = psutil.cpu_percent(interval=0.9)
   apidata['mem'] = psutil.virtual_memory().percent
   apidata['disk'] = psutil.disk_usage('/').percent
   diskio = psutil.disk_io_counters()
   netio = psutil.net_io_counters()

   apidata['net_sent'] = 0 if olddata['net_sent'] == 0 else netio.bytes_sent - olddata['net_sent']
   olddata['net_sent'] = netio.bytes_sent
   apidata['net_recv'] = 0 if olddata['net_recv'] == 0 else netio.bytes_recv - olddata['net_recv']
   olddata['net_recv'] = netio.bytes_recv

   apidata['disk_write'] = 0 if olddata['disk_write'] == 0 else diskio.write_bytes - olddata['disk_write']
   olddata['disk_write'] = diskio.write_bytes
   apidata['disk_read'] = 0 if olddata['disk_read'] == 0 else diskio.read_bytes - olddata['disk_read']
   olddata['disk_read'] = diskio.read_bytes

   return jsonify(apidata)