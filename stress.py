import subprocess
import mysql.connector
from mysql.connector import Error
import threading
import time
import os

# Function to perform CPU stress test
def cpu_stress_test():
    subprocess.run(['stress-ng', '--cpu', '2', '--timeout', '30'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("CPU stress test completed.")

# Function to perform memory stress test
def memory_stress_test():
    subprocess.run(['stress-ng', '--vm', '2', '--vm-bytes', '50%', '--timeout', '30'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Memory stress test completed.")

# Function to perform disk stress test
def disk_stress_test():
    subprocess.run(['stress-ng', '--hdd', '2', '--hdd-bytes', '50%', '--timeout', '30'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Disk stress test completed.")

# Function to perform network stress test
def network_stress_test():
    subprocess.run(['iperf3', '-c', '192.168.29.49', '-t', '120'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Network stress test completed.")

# Function to perform MySQL QPS stress test
def mysql_qps_stress_test():
    try:
        connection = mysql.connector.connect(
            host='192.168.29.49',
            database='sample',
            user='remote_user',
            password='Root@1234'  
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
        print(f"MySQL QPS stress test completed. Approximate QPS: {qps:.2f}")
        
    except Error as e:
        print("Error during MySQL QPS stress test:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



stress_tests = {
    1: cpu_stress_test,
    2: memory_stress_test,
    3: disk_stress_test,
    4: network_stress_test,
    5: mysql_qps_stress_test  
}


def main():
   
    os.system('nohup /root/node_exporter-1.8.2.linux-amd64/./node_exporter &')
    print("Node Exporter started.")

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
                print("Exiting...")
                break
            elif choice == 6:
                threads = [threading.Thread(target=test) for test in stress_tests.values()]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                print("All tests completed.")
            elif choice in stress_tests:
                stress_tests[choice]()
            else:
                print("Invalid choice")

            time.sleep(30)

    finally:
        print("Script completed.")


if __name__ == "__main__":
    main()
