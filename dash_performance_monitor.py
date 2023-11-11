import subprocess
import threading
import time
import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to monitor CPU and memory usage
def monitor_resources(process):
    while True:
        # Get the main process info
        main_cpu = process.cpu_percent(interval=1)
        main_mem = process.memory_info().rss

        # Initialize cumulative CPU and memory usage
        total_cpu = main_cpu
        total_mem = main_mem

        # Get child processes
        children = process.children(recursive=True)
        for child in children:
            try:
                # Aggregate resource usage from child processes
                total_cpu += child.cpu_percent(interval=1)
                total_mem += child.memory_info().rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # If the child process has terminated or cannot be accessed, skip it
                continue

        print(f"Total CPU Usage: {total_cpu}%")
        print(f"Total Memory Usage: {total_mem / (1024 * 1024)} MB")
        time.sleep(1)

# Function to measure load time using Selenium
def measure_load_time():
    driver = webdriver.Chrome()
    try:
        start_time = time.time()
        driver.get('http://localhost:8050')
        WebDriverWait(driver, 3600).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-plotly-plot')))
        load_time = time.time() - start_time
        print(f"Load time: {load_time} seconds")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Start the Dash app as a subprocess
dash_process = subprocess.Popen(["python", "app.py"])

# Give the server some time to start
time.sleep(5)

# Get the PID of the Dash app
dash_pid = dash_process.pid
print(f"Dash app PID: {dash_pid}")

# Create a psutil Process object for the Dash app
dash_psutil_process = psutil.Process(dash_pid)

# Start the resource monitoring in a separate thread
monitor_thread = threading.Thread(target=monitor_resources, args=(dash_psutil_process,))
monitor_thread.start()

# Start the Selenium load time measurement in a separate thread
# selenium_thread = threading.Thread(target=measure_load_time)
# selenium_thread.start()

# Wait for the Selenium thread to finish
# selenium_thread.join()

# Stop the resource monitoring thread after a certain period
time.sleep(120)

# Stop the Dash app by terminating the subprocess
dash_process.terminate()
dash_process.wait()  # Wait for the subprocess to terminate
