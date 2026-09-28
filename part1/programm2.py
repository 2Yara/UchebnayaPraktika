from collections import Counter
import time
from collections import Counter

def optimized_count_services(filename):
    counter = Counter()
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            service_raw = parts[4]
            if '[' in service_raw:
                service = service_raw[:service_raw.index('[')]
            else:
                service = service_raw.rstrip(':')
            counter[service] += 1
    
    return counter.most_common(5)

if __name__ == "__main__":
    start = time.time()
    top5 = optimized_count_services("Linux.log")
    end = time.time()

    print("Топ-5 IP (оптимизированный метод):")
    for ip, count in top5:
        print(f"{ip}: {count}")
    print(f"Время выполнения: {end - start:.4f} секунд")