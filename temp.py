import csv
import os
import platform
import mysql.connector
import re

plat = platform.system()

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
def insert_ping_result(cursor, vm, status, min_val, max_val, avg_val):
    # import pdb; pdb.set_trace()
    sql = "INSERT INTO Pingdata (status, min_val, max_val, avg_val) VALUES (%s, %s, %s, %s)"
    values = (status, min_val, max_val, avg_val)
    cursor.execute(sql, values)

# Import the list of hosts/servers/ipaddress from CSV file
with open('data.csv', 'r') as servers_list:
    servers = csv.DictReader(servers_list)

    for row in servers:
        vm = row['websites']
        print("---- Trying to Ping a Server with IPAddress ----", row['websites'])

        # Check for Linux Platforms
        if plat == "Linux":
            response = os.system("ping -c 4 -W 3 " + vm)
            

            # Parse the ping output to get min, max, avg values
            if response == 0:
                output = os.popen(f"ping -c 4 -W 3 {vm}").read()
                match = re.search(r"min/avg/max/.*?=\s*(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)", output)

                if match:
                    min_val = float(match.group(1))
                    avg_val = float(match.group(2))
                    max_val = float(match.group(3))
                    
                    # Set status as UP
                    status = 'UP'
                else:
                    print(row['websites'], 'is DOWN and No response from Server!\n')
                    # Set status as DOWN
                    status = 'DOWN'
            else:
                print(row['websites'], 'is DOWN and No response from Server!\n')
                # Set status as DOWN
                status = 'DOWN'
                
            # Insert ping results into MySQL
            insert_ping_result(cursor, vm, status, min_val, max_val, avg_val)


# Commit changes and close connections
connection.commit()
cursor.close()
connection.close()
