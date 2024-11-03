import subprocess
import mysql.connector
from mysql.connector import Error
import threading
import time
import os
import logging
import psutil

# Configure logging
logging.basicConfig(
    filename="stress_test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to log system stats
def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    logging.info(f"System stats - CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%")

# Function to perform CPU stress test
def cpu_stress_test():
    logging.info("Starting CPU stress test.")
    get_system_stats()
    try:
        subprocess.run(['stress-ng', '--cpu', '2', '--timeout', '30'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info("CPU stress test completed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during CPU stress test: {e}")
    get_system_stats()

# Function to perform memory stress test
def memory_stress_test():
    logging.info("Starting memory stress test.")
    get_system_stats()
    try:
        subprocess.run(['stress-ng', '--vm', '2', '--vm-bytes', '50%', '--timeout', '30'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info("Memory stress test completed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during memory stress test: {e}")
    get_system_stats()

# Function to perform disk stress test
def disk_stress_test():
    logging.info("Starting disk stress test.")
    get_system_stats()
    try:
        subprocess.run(['stress-ng', '--hdd', '2', '--hdd-bytes', '50%', '--timeout', '30'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info("Disk stress test completed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during disk stress test: {e}")
    get_system_stats()

# Function to perform network stress test
def network_stress_test():
    logging.info("Starting network stress test.")
    get_system_stats()
    try:
        subprocess.run(['iperf3', '-c', 'ip', '-t', '120'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info("Network stress test completed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during network stress test: {e}")
    get_system_stats()

# Function to perform MySQL QPS stress test
def mysql_qps_stress_test():
    logging.info("Starting MySQL QPS stress test.")
    get_system_stats()
    try:
        connection = mysql.connector.connect(
            host='ip',
            database='sample',
            user='remote_user',
            password=''  
        )
        cursor = connection.cursor()

        start_time = time.time()
        query_count = 0
        duration = 60

        while time.time() - start_time < duration:
            cursor.execute("SELECT * FROM sbtest1 LIMIT 1")
            cursor.fetchall()
            query_count += 1

        elapsed_time = time.time() - start_time
        qps = query_count / elapsed_time
        logging.info(f"MySQL QPS stress test completed. Approximate QPS: {qps:.2f}")

    except Error as e:
        logging.error("Error during MySQL QPS stress test: " + str(e))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    get_system_stats()

# Dictionary mapping choices to functions
stress_tests = {
    1: cpu_stress_test,
    2: memory_stress_test,
    3: disk_stress_test,
    4: network_stress_test,
    5: mysql_qps_stress_test  
}

def main():
    logging.info("Starting Node Exporter.")
    os.system('nohup /root/node_exporter-1.8.2.linux-amd64/./node_exporter &')
    logging.info("Node Exporter started.")

    try:
        while True:
            print("\nSelect the stress test to run:")
            print("1. CPU Stress Test")
            print("2. Memory Stress Test")
            print("3. Disk Stress Test")
            print("4. Network Stress Test")
            print("5. MySQL QPS Stress Test")
            print("6. Run All Tests")
            print("0. Exit")

            choice = int(input("Enter your choice: "))

            if choice == 0:
                logging.info("Exiting script.")
                break
            elif choice == 6:
                logging.info("Running all stress tests.")
                threads = [threading.Thread(target=test) for test in stress_tests.values()]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                logging.info("All stress tests completed.")
            elif choice in stress_tests:
                logging.info(f"Running test {choice}")
                stress_tests[choice]()
            else:
                print("Invalid choice. Please select a valid option.")

            time.sleep(30)

    finally:
        logging.info("Script completed.")

if __name__ == "__main__":
    main()
