import csv
import os
import platform
import mysql.connector
import re


plat = platform.system()
# myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "root@123")  
# print(myconn) 

# Define MySQL connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root@123',
    'database': 'PINGTABLE'
}
   # Connect to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Function to insert ping results into MySQL
def insert_ping_result(cursor, vm, min_val, max_val, avg_val):
    sql = "INSERT INTO Pingdata (host, status, min, max, avg) VALUES (%s, %s, %s,%s,%s)"
    values = (vm,status,min_val, max_val, avg_val)
    cursor.execute(sql, values)

# Import the list of hosts/servers/ipaddress from CSV file
with open('data.csv', 'r') as servers_list:
    servers = csv.DictReader(servers_list)
    
 

    for row in servers:
        vm = row['websites']
        print("---- Trying to Ping a Server with IPAddress ----", row['websites'])

        # Check for Windows and Linux Platforms  # Perform 4 pings for better statistics
        plat == "Linux"
        response = os.system("ping -c 4 -W 3 " + vm)
        # import pdb; pdb.set_trace()
        # Parse the ping output to get min, max, avg values
        # if response == 0:
        #     # import pdb; pdb.set_trace()
        output = os.popen(f"ping -c 4 -W 3 {vm}").read()
        #     min_val=float(output.split("min/avg/max/mdev")[1].split()[0])
        #     avg_val=float(output.split("min/avg/max/mdev")[1].split()[1])
        #     max_val=float(output.split("min/avg/max/mdev")[1].split()[2])
        match = re.search(r"min/avg/max/.*?=\s*(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)", output)
        
        if match:
            min_val = float(match.group(1))
            avg_val = float(match.group(2))
            max_val = float(match.group(3))   
            # Insert ping results into MySQL
            insert_ping_result(cursor, vm, min_val, max_val, avg_val)
        else:
            print(row['websites'], 'is DOWN and No response from Server!\n')
            # import pdb; pdb.set_trace()
            # Insert ping results into MySQL
            insert_ping_result(cursor, vm, min_val, max_val, avg_val)

    # Commit changes and close connections
    connection.commit()
    cursor.close()
    connection.close()
