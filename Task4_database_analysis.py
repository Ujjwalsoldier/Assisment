import sqlite3

conn = sqlite3.connect("traffic.db")
cursor = conn.cursor()


cursor.execute("""SELECT strftime('%H', timestamp) AS hour,
       AVG(response_time_ms) AS avg_response_time
FROM request_logs
GROUP BY hour
ORDER BY avg_response_time DESC
LIMIT 1;""")
rows = cursor.fetchall()
for row in rows:
    print("Hour with the highest average response time",row)



cursor.execute("""SELECT ip_address, COUNT(*) AS request_count
FROM request_logs
WHERE status_code = 429
GROUP BY ip_address
HAVING COUNT(*) > 350;""")
rows = cursor.fetchall()
for row in rows:
    print("IPs with more than 350 requests with status 429",row)



cursor.execute("""SELECT SUM(bytes_sent) AS total_bytes
FROM request_logs
WHERE response_time_ms > 500;""")
rows = cursor.fetchall()
for row in rows:
    print("Total bytes sent for requests with response time > 500ms",row)    

conn.close()
