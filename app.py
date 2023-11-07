from flask import Flask, render_template, jsonify
import psutil
import GPUtil
import pynvml
import time

app = Flask(__name__)

pynvml.nvmlInit()

def cpu():
    return psutil.cpu_percent(interval=1)

def ram():
    ram = psutil.virtual_memory().used / (1024 ** 3)
    return round(ram, 2)

def gpu():
    try:
        gpu = GPUtil.getGPUs() [0]
        usage = round(gpu.load * 100, 1)
        return format(usage, ".1f")
    except Exception as e:
        return 0
    
def temp():
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        return temp
    except Exception as e:
        return 0
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/usage_json")
def usage_json():
    cpu = cpu()
    ram = ram()
    gpu = gpu()
    temp = temp()
    return jsonify({"cpu": cpu, "ram": ram, "gpu": gpu, "temp": temp})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)