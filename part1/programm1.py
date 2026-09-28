import time 

def naive_count_services(filename):
    services = []
    counts = []
    
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
            
            found = False
            for i in range(len(services)):
                if services[i] == service:
                    counts[i] += 1
                    found = True
                    break
            if not found:
                services.append(service)
                counts.append(1)
    
    result = sorted(zip(services, counts), key=lambda x: x[1], reverse=True)
    return result

if __name__ == "__main__":
    start = time.time()
    result = naive_count_services("Linux.log")
    end = time.time()

    print("Топ-5 IP (простой метод):")
    for ip, count in result[:5]:
        print(f"{ip}: {count}")
    print(f"Время выполнения: {end - start:.4f} секунд")