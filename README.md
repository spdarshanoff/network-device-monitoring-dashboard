# Network Device Monitoring Dashboard

A lightweight Network Operations Center (NOC) monitoring system built using Python, MySQL, and Flask.  
This project monitors network devices, checks availability, tracks latency, generates alerts, and displays results on a web dashboard.

---

## Features

- Device management
- Ping monitoring
- Latency measurement
- Health scoring system
- Alert generation
- Logs storage in MySQL
- Flask dashboard UI
- Login authentication
- Alerts page
- Health status page
- Devices page

---

## Tech Stack

- Python
- Flask
- MySQL
- HTML / Bootstrap
- Git / GitHub

---

## Project Architecture

Devices  
↓  
Python Monitoring Engine  
↓  
MySQL Database  
↓  
Flask Dashboard  

---

## How to Run

1. Install Python
2. Install MySQL
3. Install packages

pip install flask mysql-connector-python ping3


4. Run monitor

python -m monitoring_engine.monitor_runner


5. Run dashboard

python -m dashboard.app


Open browser

http://127.0.0.1:5000


Login

username: admin  
password: admin  


---

## Author

Darshan

# update project