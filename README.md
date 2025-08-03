# 🛠️ Azure-Based ETL Data Pipeline with Apache Airflow

This project demonstrates an end-to-end **ETL pipeline** built for a **low-memory Azure VM** using **Apache Airflow**, **Azure Blob Storage**, and **Azure SQL Database**.

It’s designed as a **portfolio project** to showcase skills in Data Engineering, Python, Airflow orchestration, and Azure services.

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Folder Structure](#folder-structure)
- [Setup Instructions](#setup-instructions)
- [DAG & Scripts](#dag--scripts)
- [Running the Pipeline](#running-the-pipeline)
- [Output & Logs](#output--logs)
- [Screenshots](#screenshots)
- [License](#license)

## 🧾 Project Overview

This ETL pipeline extracts sales data from **Azure Blob Storage**, transforms it using **pandas**, and loads it into an **Azure SQL Database**.

The orchestration is handled by **Apache Airflow** running on an Azure VM with **minimal resources (1 vCPU, 1GB RAM)**.

## 🗂️ Folder Structure

```
airflow/
│
├── dags/
│   └── etl_pipeline.py
│
├── scripts/
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_to_sql.py
│
├── data/
│   └── processed/
│       └── clean_superstore.csv
│
├── logs/
└── airflow.cfg
```

## 🏗️ Architecture

```
         Azure Blob Storage
               |
               ▼
         extract_data.py
               |
               ▼
       transform_data.py
               |
               ▼
          clean_superstore.csv
               |
               ▼
         load_to_sql.py
               |
               ▼
     Azure SQL Database (retailsalesdb)

 Orchestrated by:
 Apache Airflow (on Azure VM)
```

## 🧰 Technologies Used

- Python 3.11
- Apache Airflow
- Azure Blob Storage
- Azure SQL Database
- Azure Virtual Machine (Linux B1s)
- pyenv & virtualenv
- pandas, sqlalchemy, pyodbc

## ⚙️ Setup Instructions

### 🔹 Azure VM Setup (Linux B1s)

1. Create a resource group and VM with at least:
   - Ubuntu 22.04
   - 1 vCPU, 1GB RAM
   - Public IP and open port **22 (SSH)** and **8080 (Airflow)**

2. SSH into the VM:
   ```bash
   ssh azureuser@<your-vm-ip>
   ```

### 🔹 Install Python & Airflow with pyenv

```bash
# Install pyenv
curl https://pyenv.run | bash

# Load pyenv in .bashrc
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install Python
pyenv install 3.11.9
pyenv virtualenv 3.11.9 airflow-venv
pyenv activate airflow-venv

# Install Airflow
pip install --upgrade pip
pip install "apache-airflow[celery,postgres,azure]" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.11.txt"
```

### 🔹 Initialize Airflow & Tune

```bash
airflow db init

# (Optional) Create Admin User
airflow users create   --username admin --firstname Ayaz --lastname Rao   --role Admin --email ayaz@example.com --password admin

# Run tuning script (already included)
bash ~/tune_airflow_config.sh
```

## 🧠 DAG & Scripts Overview

### `etl_pipeline.py` (DAG)

Schedules and runs the 3 Python scripts:

```python
start = PythonOperator(task_id="extract", python_callable=extract_data)
middle = PythonOperator(task_id="transform", python_callable=transform_data)
end = PythonOperator(task_id="load", python_callable=load_to_sql)

start >> middle >> end
```

### `extract_data.py`

- Connects to Azure Blob Storage using `azure-storage-blob`
- Downloads a `.csv` file into `data/raw/`

### `transform_data.py`

- Cleans and filters the CSV using `pandas`
- Saves as `clean_superstore.csv` in `data/processed/`

### `load_to_sql.py`

- Uses `sqlalchemy` or `pyodbc` to connect to Azure SQL Database
- Loads cleaned data into the `sales_data` table

## ▶️ Running the Pipeline

### Webserver

```bash
airflow webserver --port 8080
```

### Scheduler (in a second terminal)

```bash
airflow scheduler
```

Then visit:

```
http://<your-vm-ip>:8080
```

Login with `admin / admin`

## 💾 Downloading Output Files

From your **local terminal**, run:

```bash
# Create folders
mkdir -p airflow_project/scripts airflow_project/dags airflow_project/data airflow_project/logs

# Download scripts
scp azureuser@<your-vm-ip>:~/airflow/scripts/*.py airflow_project/scripts/
scp azureuser@<your-vm-ip>:~/airflow/dags/etl_pipeline.py airflow_project/dags/
scp azureuser@<your-vm-ip>:~/airflow/data/processed/clean_superstore.csv airflow_project/data/
scp -r azureuser@<your-vm-ip>:~/airflow/logs airflow_project/logs/
```

## 🖼️ Screenshots

> Upload your screenshots to `screenshots/` and replace the placeholders below.

- ![Airflow UI](screenshots/airflow-ui.png)
- ![Running DAG](screenshots/dag-run.png)
- ![Azure SQL](screenshots/sql-database.png)

## 📜 License

MIT License. Use and modify freely. Credit appreciated.

## 🙋 Contact

Built by **Ayaz Rao**  
📧 [your-email@example.com]  
🌐 [LinkedIn or GitHub profile link]