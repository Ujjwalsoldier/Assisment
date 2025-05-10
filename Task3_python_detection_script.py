#Two assuptions for bad ip detection
# Flag IPs with too many 4xx or 5xx errors (bad behavior) - assumption: more than 350
# Flag IPs with too many requests (possibly it can be bots) - assumption : more than 240

import re
from collections import defaultdict, Counter

log_file = 'Ujjwal_Aditya/nginx_access.log'

ip_request_count = Counter()
ip_error_count = Counter()

pattern = re.compile(r'^(\d+\.\d+\.\d+\.\d+).*?"\w+ [^"]+ HTTP/\d\.\d" (\d{3})')

with open(log_file, 'r') as file:
    for line in file:
        match = pattern.search(line)
        if match:
            ip, status = match.groups()
            status = int(status)

            ip_request_count[ip] += 1
            if 400 <= status <= 599:
                ip_error_count[ip] += 1

# Detect suspicious IPs
print(" detection Summary:\n")
for ip in ip_request_count:
    total = ip_request_count[ip]
    errors = ip_error_count.get(ip, 0)

    if total > 350 or errors > 240:  # we can be adjust these.
        error_rate = (errors / total) * 100
        print(f"IP: {ip} | Requests: {total} | Errors: {errors} | Error Rate: {error_rate:.1f}%")