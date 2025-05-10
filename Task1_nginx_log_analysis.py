import re
from collections import Counter


log_file = "Ujjwal_Aditya/nginx_access.log"
output_file = "Ujjwal_Aditya/Task1_nginx_report.txt"

ip_counter = Counter()
total_requests = 0
error_requests = 0
get_response_sizes = []

log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s\w+\s\[.*?\]\s"[^"]+"\s"(?P<method>\w+)\s[^\s]+ [^"]+"\s(?P<status>\d{3})\s(?P<size>\d+)\s'
)

with open(log_file, 'r') as f:
    for line in f:
        match = log_pattern.search(line)
        if match:
            total_requests += 1
            ip = match.group('ip')
            method = match.group('method')
            status = int(match.group('status'))
            size = int(match.group('size'))

            ip_counter[ip] += 1

            if 400 <= status <= 599:
                error_requests += 1

            if method == "GET":
                get_response_sizes.append(size)


top_ips = ip_counter.most_common(5)
error_percent = (error_requests / total_requests) * 100 if total_requests else 0
average_get_size = sum(get_response_sizes) / len(get_response_sizes) if get_response_sizes else 0


with open(output_file, 'w') as f:
    f.write("Nginx Access Log Analysis Report\n")
    f.write("="*40 + "\n\n")

    f.write("Top 5 IP addresses by request count:\n")
    for ip, count in top_ips:
        f.write(f"{ip}: {count} requests\n")

    f.write(f"\nPercentage of 4xx/5xx requests: {error_percent:.2f}%\n")
    f.write(f"Average response size for GET requests: {average_get_size:.2f} bytes\n")

print(f"Report saved to {output_file}")