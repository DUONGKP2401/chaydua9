import threading
import base64
import os
import time
import re
import requests
import socket
import sys
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
from collections import Counter, deque, defaultdict
from urllib.parse import urlparse, parse_qs
import random
import math
import hashlib
import platform
import subprocess
import statistics
import string
import urllib.parse

# Check và cài đặt các thư viện cần thiết
try:
    from colorama import init, Fore, Style
    import pytz
    from faker import Faker
    from requests import session
    import pystyle
    init(autoreset=True)
except ImportError:
    print('__Đang cài đặt thư viện, vui lòng chờ...__')
    os.system("pip install requests colorama pytz faker pystyle bs4")
    print('__Cài đặt hoàn tất, vui lòng chạy lại Tool__')
    sys.exit()

# =====================================================================================
# PHẦN 1: MÃ NGUỒN TỪ KEYV8.PY (LOGIC XÁC THỰC - GIỮ NGUYÊN)
# =====================================================================================

# CONFIGURATION FOR VIP KEY
VIP_KEY_URL = "https://raw.githubusercontent.com/DUONGKP2401/KEY-VIP.txt/main/KEY-VIP.txt"
VIP_CACHE_FILE = 'vip_cache.json'

# Encrypt and decrypt data using base64
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

# Colors for display (từ keyv8.py)
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

# Đổi tên hàm banner của file banner.py để tránh xung đột
def authentication_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner_text = f"""
{luc}████████╗ ██████╗░░ ██╗░░██╗░
{luc}╚══██╔══╝ ██╔══██╗░ ██║██╔╝░░
{luc}░░░██║░░░ ██║░░██║░ █████╔╝░░
{luc}░░░██║░░░ ██║░░██║░ ██╔═██╗░░
{luc}░░░██║░░░ ██║░░██║░ ██║░╚██╗░
{luc}░░░╚═╝░░░ ╚█████╔╝░ ╚═╝░░╚═╝░
{trang}══════════════════════════

{vang}Tool VIP V9
{trang}══════════════════════════
"""
    for char in banner_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.0001)

# DEVICE ID AND IP ADDRESS FUNCTIONS
def get_device_id():
    """Generates a stable device ID based on CPU information."""
    system = platform.system()
    try:
        if system == "Windows":
            cpu_info = subprocess.check_output('wmic cpu get ProcessorId', shell=True, text=True, stderr=subprocess.DEVNULL)
            cpu_info = ''.join(line.strip() for line in cpu_info.splitlines() if line.strip() and "ProcessorId" not in line)
        else:
            try:
                cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True, text=True)
            except:
                cpu_info = platform.processor()
        if not cpu_info:
            cpu_info = platform.processor()
    except Exception:
        cpu_info = "Unknown"

    hash_hex = hashlib.sha256(cpu_info.encode()).hexdigest()
    only_digits = re.sub(r'\D', '', hash_hex)
    if len(only_digits) < 16:
        only_digits = (only_digits * 3)[:16]

    return f"DEVICE-{only_digits[:16]}"

def get_ip_address():
    """Gets the user's public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_data = response.json()
        return ip_data.get('ip')
    except Exception as e:
        print(f"{do}Lỗi khi lấy địa chỉ IP: {e}{trang}")
        return None

def display_machine_info(ip_address, device_id):
    """Displays the banner, IP address, and Device ID."""
    authentication_banner() # Gọi hàm banner đã đổi tên
    if ip_address:
        print(f"{trang}[{do}<>{trang}] {do}Địa chỉ IP: {vang}{ip_address}{trang}")
    else:
        print(f"{do}Không thể lấy địa chỉ IP của thiết bị.{trang}")

    if device_id:
        print(f"{trang}[{do}<>{trang}] {do}Mã Máy: {vang}{device_id}{trang}")
    else:
        print(f"{do}Không thể lấy Mã Máy của thiết bị.{trang}")


# FREE KEY HANDLING FUNCTIONS
def luu_thong_tin_ip(ip, key, expiration_date):
    """Saves free key information to a json file."""
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))
    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    """Loads free key information from the json file."""
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def kiem_tra_ip(ip):
    """Checks for a saved free key for the current IP."""
    data = tai_thong_tin_ip()
    if data and ip in data:
        try:
            expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
            if expiration_date > datetime.now():
                return data[ip]['key']
        except (ValueError, KeyError):
            return None
    return None

def generate_key_and_url(ip_address):
    """Creates a free key and a URL to bypass the link."""
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'VTD9{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://tdkvuatocdo.blogspot.com/2025/09/key-vtdv9_18.html?m={key}'
    return url, key, expiration_date

def get_shortened_link_phu(url):
    """Shortens the link to get the free key."""
    try:
        token = "6725c7b50c661e3428736919"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

def process_free_key(ip_address):
    """Handles the entire process of obtaining a free key."""
    url, key, expiration_date = generate_key_and_url(ip_address)

    with ThreadPoolExecutor(max_workers=1) as executor:
        yeumoney_future = executor.submit(get_shortened_link_phu, url)
        yeumoney_data = yeumoney_future.result()

    if yeumoney_data and yeumoney_data.get('status') == "error":
        print(yeumoney_data.get('message'))
        return False

    link_key_yeumoney = yeumoney_data.get('shortenedUrl')
    print(f'{trang}[{do}<>{trang}] {hong}Link Để Vượt Key Là {xnhac}: {link_key_yeumoney}{trang}')

    while True:
        keynhap = input(f'{trang}[{do}<>{trang}] {vang}Key Đã Vượt Là: {luc}')
        if keynhap == key:
            print(f'{luc}Key Đúng! Mời Bạn Dùng Tool{trang}')
            sleep(2)
            luu_thong_tin_ip(ip_address, keynhap, expiration_date)
            return True
        else:
            print(f'{trang}[{do}<>{trang}] {hong}Key Sai! Vui Lòng Vượt Lại Link {xnhac}: {link_key_yeumoney}{trang}')


# VIP KEY HANDLING FUNCTIONS
def save_vip_key_info(device_id, key, expiration_date_str):
    """Saves VIP key information to a local cache file."""
    data = {'device_id': device_id, 'key': key, 'expiration_date': expiration_date_str}
    encrypted_data = encrypt_data(json.dumps(data))
    with open(VIP_CACHE_FILE, 'w') as file:
        file.write(encrypted_data)
    print(f"{luc}Đã lưu thông tin Key VIP cho lần đăng nhập sau.{trang}")

def load_vip_key_info():
    """Loads VIP key information from the local cache file."""
    try:
        with open(VIP_CACHE_FILE, 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return None

def display_remaining_time(expiry_date_str):
    """Calculates and displays the remaining time for a VIP key."""
    try:
        expiry_date = datetime.strptime(expiry_date_str, '%d/%m/%Y').replace(hour=23, minute=59, second=59)
        now = datetime.now()

        if expiry_date > now:
            delta = expiry_date - now
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"{xnhac}Key VIP của bạn còn lại: {luc}{days} ngày, {hours} giờ, {minutes} phút.{trang}")
        else:
            print(f"{do}Key VIP của bạn đã hết hạn.{trang}")
    except ValueError:
        print(f"{vang}Không thể xác định ngày hết hạn của key.{trang}")

def check_vip_key(machine_id, user_key):
    """Checks the VIP key from the URL on GitHub."""
    print(f"{vang}Đang kiểm tra Key VIP...{trang}")
    try:
        response = requests.get(VIP_KEY_URL, timeout=10)
        if response.status_code != 200:
            print(f"{do}Lỗi: Không thể tải danh sách key (Status code: {response.status_code}).{trang}")
            return 'error', None

        key_list = response.text.strip().split('\n')
        for line in key_list:
            parts = line.strip().split('|')
            if len(parts) >= 4:
                key_ma_may, key_value, _, key_ngay_het_han = parts

                if key_ma_may == machine_id and key_value == user_key:
                    try:
                        expiry_date = datetime.strptime(key_ngay_het_han, '%d/%m/%Y')
                        if expiry_date.date() >= datetime.now().date():
                            return 'valid', key_ngay_het_han
                        else:
                            return 'expired', None
                    except ValueError:
                        continue
        return 'not_found', None
    except requests.exceptions.RequestException as e:
        print(f"{do}Lỗi kết nối đến server key: {e}{trang}")
        return 'error', None

# MAIN AUTHENTICATION FLOW
def main_authentication():
    ip_address = get_ip_address()
    device_id = get_device_id()
    display_machine_info(ip_address, device_id)

    if not ip_address or not device_id:
        print(f"{do}Không thể lấy thông tin thiết bị cần thiết. Vui lòng kiểm tra kết nối mạng.{trang}")
        return False

    cached_vip_info = load_vip_key_info()
    if cached_vip_info and cached_vip_info.get('device_id') == device_id:
        try:
            expiry_date = datetime.strptime(cached_vip_info['expiration_date'], '%d/%m/%Y')
            if expiry_date.date() >= datetime.now().date():
                print(f"{luc}Đã tìm thấy Key VIP hợp lệ, tự động đăng nhập...{trang}")
                display_remaining_time(cached_vip_info['expiration_date'])
                sleep(3)
                return True
            else:
                print(f"{vang}Key VIP đã lưu đã hết hạn. Vui lòng lấy hoặc nhập key mới.{trang}")
        except (ValueError, KeyError):
            print(f"{do}Lỗi file lưu key. Vui lòng nhập lại key.{trang}")

    if kiem_tra_ip(ip_address):
        print(f"{trang}[{do}<>{trang}] {hong}Key free hôm nay vẫn còn hạn. Mời bạn dùng tool...{trang}")
        time.sleep(2)
        return True

    while True:
        print(f"{trang}========== {vang}MENU LỰA CHỌN{trang} ==========")
        print(f"{trang}[{luc}1{trang}] {xduong}Nhập Key VIP{trang}")
        print(f"{trang}[{luc}2{trang}] {xduong}Lấy Key Free (Dùng trong ngày){trang}")
        print(f"{trang}======================================")

        try:
            choice = input(f"{trang}[{do}<>{trang}] {xduong}Nhập lựa chọn của bạn: {trang}")
            print(f"{trang}═══════════════════════════════════")

            if choice == '1':
                vip_key_input = input(f'{trang}[{do}<>{trang}] {vang}Vui lòng nhập Key VIP: {luc}')
                status, expiry_date_str = check_vip_key(device_id, vip_key_input)

                if status == 'valid':
                    print(f"{luc}Xác thực Key VIP thành công!{trang}")
                    save_vip_key_info(device_id, vip_key_input, expiry_date_str)
                    display_remaining_time(expiry_date_str)
                    sleep(3)
                    return True
                elif status == 'expired':
                    print(f"{do}Key VIP của bạn đã hết hạn. Vui lòng liên hệ admin.{trang}")
                elif status == 'not_found':
                    print(f"{do}Key VIP không hợp lệ hoặc không tồn tại cho mã máy này.{trang}")
                else:
                    print(f"{do}Đã xảy ra lỗi trong quá trình xác thực. Vui lòng thử lại.{trang}")
                sleep(2)

            elif choice == '2':
                if process_free_key(ip_address):
                    return True
                else:
                    return False

            else:
                print(f"{vang}Lựa chọn không hợp lệ, vui lòng nhập 1 hoặc 2.{trang}")

        except (KeyboardInterrupt):
            print(f"\n{trang}[{do}<>{trang}] {do}Cảm ơn bạn đã dùng Tool !!!{trang}")
            sys.exit()

# =====================================================================================
# PHẦN 2: MÃ NGUỒN TỪ T22.PY (TOOL CHÍNH)
# =====================================================================================

# Bảng màu
class Colors:
    RED = "\033[1;31m"; GREEN = "\033[1;32m"; YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"; MAGENTA = "\033[1;35m"; CYAN = "\033[1;36m"
    WHITE = "\033[1;37m"; RESET = "\033[0m"; HEADER = "\033[38;2;255;185;0m"
    BORDER = "\033[38;2;100;100;100m"; PROFIT = "\033[38;2;0;255;127m"
    LOSS = "\033[38;2;255;80;80m"; TEXT_LABEL = "\033[38;2;175;175;175m"
    TEXT_VALUE = "\033[38;2;255;255;255m"

NV = {
    1: 'Bậc thầy tấn công', 2: 'Quyền sắt', 3: 'Thợ lặn sâu',
    4: 'Cơn lốc sân cỏ', 5: 'Hiệp sĩ phi nhanh', 6: 'Vua home run'
}

# =====================================================================================
# PHẦN LOGIC NÂNG CẤP - THAY THẾ TOÀN BỘ CLASS LOGICENGINE CŨ
# =====================================================================================
class LogicEngine:
    def __init__(self, recency_window=20):
        self.history_data = deque(maxlen=200)
        self.losing_streak_count = 0
        self.recency_window = recency_window
        self.last_bet_on = None
        # Khởi tạo danh sách 50 logic khác nhau
        self.logics = self._initialize_logics()

    def add_result(self, winner): self.history_data.append(winner)
    def record_win(self): self.losing_streak_count = 0; self.last_bet_on = None
    def record_loss(self, bet_on_char): self.losing_streak_count += 1; self.last_bet_on = bet_on_char

    def _get_stats(self):
        """Hàm trợ giúp tính toán trước các chỉ số thống kê từ lịch sử."""
        if not self.history_data:
            return None
        
        history = list(self.history_data)
        recent_history = history[-self.recency_window:]
        
        # Tần suất
        overall_freq = Counter(history)
        recent_freq = Counter(recent_history)
        
        # Xếp hạng
        # sorted trả về list các tuple (char_id, count). Dùng [0] để lấy char_id
        overall_ranks = [item[0] for item in overall_freq.most_common()]
        recent_ranks = [item[0] for item in recent_freq.most_common()]
        
        # Lịch sử vị trí (last seen)
        last_seen_indices = {char_id: i for i, char_id in enumerate(reversed(history))}

        # Đảm bảo tất cả nhân vật đều có trong danh sách
        for char_id in NV.keys():
            if char_id not in overall_ranks: overall_ranks.append(char_id)
            if char_id not in recent_ranks: recent_ranks.append(char_id)
            if char_id not in last_seen_indices: last_seen_indices[char_id] = float('inf')

        # Sắp xếp theo chỉ số nhìn thấy lần cuối để tìm con "lạnh" nhất và "nóng" nhất
        coldest_to_hottest = sorted(last_seen_indices.keys(), key=lambda x: last_seen_indices[x], reverse=True)

        return {
            "history": history,
            "overall_ranks": overall_ranks, # [Top1, Top2, Top3...]
            "recent_ranks": recent_ranks,
            "coldest_to_hottest": coldest_to_hottest, # [Lạnh nhất, Lạnh nhì, ..., Nóng nhất]
            "last_winner": history[-1] if history else None
        }

    def _initialize_logics(self):
        """Khởi tạo 50 chiến lược phân tích khác nhau."""
        
        logics_list = []
        
        # --- Nhóm 1: Logic dựa trên Tần suất Tổng thể (Overall Frequency) ---
        logics_list.append(lambda s: s['overall_ranks'][0])  # 1. Top 1 nhiều nhất tổng thể
        logics_list.append(lambda s: s['overall_ranks'][-1]) # 2. Top cuối (ít nhất) tổng thể
        logics_list.append(lambda s: s['overall_ranks'][1] if len(s['overall_ranks']) > 1 else s['overall_ranks'][0]) # 3. Top 2 nhiều nhất tổng thể
        logics_list.append(lambda s: s['overall_ranks'][-2] if len(s['overall_ranks']) > 2 else s['overall_ranks'][-1]) # 4. Top áp chót tổng thể
        logics_list.append(lambda s: s['overall_ranks'][2] if len(s['overall_ranks']) > 2 else s['overall_ranks'][0]) # 5. Top 3 nhiều nhất tổng thể
        
        # --- Nhóm 2: Logic dựa trên Tần suất Gần đây (Recent Frequency) ---
        logics_list.append(lambda s: s['recent_ranks'][0])  # 6. Top 1 nhiều nhất gần đây
        logics_list.append(lambda s: s['recent_ranks'][-1]) # 7. Top cuối (ít nhất) gần đây
        logics_list.append(lambda s: s['recent_ranks'][1] if len(s['recent_ranks']) > 1 else s['recent_ranks'][0]) # 8. Top 2 nhiều nhất gần đây
        logics_list.append(lambda s: s['recent_ranks'][-2] if len(s['recent_ranks']) > 2 else s['recent_ranks'][-1]) # 9. Top áp chót gần đây
        logics_list.append(lambda s: s['recent_ranks'][2] if len(s['recent_ranks']) > 2 else s['recent_ranks'][0]) # 10. Top 3 nhiều nhất gần đây

        # --- Nhóm 3: Logic dựa trên Chuỗi Nóng/Lạnh (Hot/Cold Streaks) ---
        logics_list.append(lambda s: s['coldest_to_hottest'][0])  # 11. Lạnh nhất (lâu ra nhất)
        logics_list.append(lambda s: s['coldest_to_hottest'][-1]) # 12. Nóng nhất (vừa ra xong)
        logics_list.append(lambda s: s['coldest_to_hottest'][1])  # 13. Lạnh thứ 2
        logics_list.append(lambda s: s['coldest_to_hottest'][-2]) # 14. Nóng thứ 2
        logics_list.append(lambda s: s['coldest_to_hottest'][2])  # 15. Lạnh thứ 3
        logics_list.append(lambda s: s['coldest_to_hottest'][-3]) # 16. Nóng thứ 3

        # --- Nhóm 4: Logic dựa trên Mẫu (Patterns) ---
        logics_list.append(lambda s: s['history'][-2] if len(s['history']) > 1 else s['overall_ranks'][0]) # 17. Con về trước con cuối cùng
        logics_list.append(lambda s: s['history'][0]) # 18. Con về đầu tiên trong lịch sử
        logics_list.append(lambda s: s['history'][-3] if len(s['history']) > 2 else s['overall_ranks'][0]) # 19. Con về cách đây 2 ván
        logics_list.append(lambda s: s['history'][len(s['history']) // 2]) # 20. Con về ở giữa lịch sử
        logics_list.append(lambda s: s['last_winner']) # 21. Lặp lại con vừa thắng (logic ngược)

        # --- Nhóm 5: Logic Lai (Hybrid) - Kết hợp các yếu tố ---
        logics_list.append(lambda s: s['overall_ranks'][0] if s['overall_ranks'][0] != s['last_winner'] else s['overall_ranks'][1]) # 22. Top 1 tổng thể, nếu trùng con cuối thì lấy top 2
        logics_list.append(lambda s: s['recent_ranks'][0] if s['recent_ranks'][0] != s['last_winner'] else s['recent_ranks'][1]) # 23. Top 1 gần đây, nếu trùng con cuối thì lấy top 2
        logics_list.append(lambda s: [c for c in s['overall_ranks'] if c in s['recent_ranks'][:3]][0]) # 24. Top 1 tổng thể mà cũng nằm trong top 3 gần đây
        logics_list.append(lambda s: [c for c in s['recent_ranks'] if c in s['overall_ranks'][:3]][0]) # 25. Top 1 gần đây mà cũng nằm trong top 3 tổng thể
        logics_list.append(lambda s: [c for c in s['coldest_to_hottest'] if c in s['overall_ranks'][:2]][0]) # 26. Con lạnh nhất trong số 2 con top đầu tổng thể
        logics_list.append(lambda s: [c for c in s['overall_ranks'] if c in s['coldest_to_hottest'][:3]][0]) # 27. Con top 1 tổng thể trong số 3 con lạnh nhất
        logics_list.append(lambda s: s['overall_ranks'][-1] if s['overall_ranks'][-1] != s['last_winner'] else s['overall_ranks'][-2]) # 28. Ít nhất tổng thể, nếu trùng con cuối thì lấy con ít thứ 2
        logics_list.append(lambda s: s['coldest_to_hottest'][0] if s['coldest_to_hottest'][0] != s['last_winner'] else s['coldest_to_hottest'][1]) # 29. Lạnh nhất, nếu trùng con cuối thì lấy con lạnh thứ 2
        logics_list.append(lambda s: s['recent_ranks'][-1] if s['recent_ranks'][-1] != s['last_winner'] else s['recent_ranks'][-2]) # 30. Ít nhất gần đây, nếu trùng con cuối thì lấy con ít thứ 2

        # --- Nhóm 6: Logic Phức Tạp và các biến thể khác ---
        logics_list.append(lambda s: s['overall_ranks'][3] if len(s['overall_ranks']) > 3 else s['overall_ranks'][0]) # 31. Top 4 tổng thể
        logics_list.append(lambda s: s['recent_ranks'][3] if len(s['recent_ranks']) > 3 else s['recent_ranks'][0]) # 32. Top 4 gần đây
        logics_list.append(lambda s: s['coldest_to_hottest'][3] if len(s['coldest_to_hottest']) > 3 else s['coldest_to_hottest'][0]) # 33. Lạnh thứ 4
        logics_list.append(lambda s: s['coldest_to_hottest'][-4] if len(s['coldest_to_hottest']) > 3 else s['coldest_to_hottest'][-1]) # 34. Nóng thứ 4
        logics_list.append(lambda s: statistics.mode(s['history'][:10]) if len(s['history']) >= 10 else s['overall_ranks'][0]) # 35. Con về nhiều nhất trong 10 ván đầu tiên
        logics_list.append(lambda s: statistics.mode(s['history'][-10:]) if len(s['history']) >= 10 else s['recent_ranks'][0]) # 36. Con về nhiều nhất trong 10 ván cuối cùng (khác top 1 recent)
        logics_list.append(lambda s: s['overall_ranks'][s['recent_ranks'].index(s['last_winner'])] if s['last_winner'] in s['recent_ranks'] else s['overall_ranks'][0]) # 37. Lấy con có rank tổng thể tương ứng với rank gần đây của con vừa thắng
        logics_list.append(lambda s: s['recent_ranks'][s['overall_ranks'].index(s['last_winner'])] if s['last_winner'] in s['overall_ranks'] else s['recent_ranks'][0]) # 38. Lấy con có rank gần đây tương ứng với rank tổng thể của con vừa thắng
        logics_list.append(lambda s: s['coldest_to_hottest'][s['overall_ranks'].index(s['last_winner'])] if s['last_winner'] in s['overall_ranks'] else s['coldest_to_hottest'][0]) # 39. Lấy độ "lạnh" tương ứng với rank tổng thể của con vừa thắng
        logics_list.append(lambda s: random.choice(s['overall_ranks'][:3])) # 40. Ngẫu nhiên 1 trong 3 con top tổng thể
        logics_list.append(lambda s: random.choice(s['recent_ranks'][:3])) # 41. Ngẫu nhiên 1 trong 3 con top gần đây
        logics_list.append(lambda s: random.choice(s['coldest_to_hottest'][:3])) # 42. Ngẫu nhiên 1 trong 3 con lạnh nhất
        logics_list.append(lambda s: random.choice(s['coldest_to_hottest'][-3:])) # 43. Ngẫu nhiên 1 trong 3 con nóng nhất
        
        # Thêm các logic cuối để đủ 50
        history_len = len(self.history_data)
        logics_list.append(lambda s: s['history'][int(history_len * 0.25)] if history_len > 4 else s['overall_ranks'][0]) # 44. Con ở vị trí 1/4 lịch sử
        logics_list.append(lambda s: s['history'][int(history_len * 0.75)] if history_len > 4 else s['overall_ranks'][0]) # 45. Con ở vị trí 3/4 lịch sử
        logics_list.append(lambda s: s['overall_ranks'][len(s['overall_ranks']) // 2]) # 46. Con có rank ở giữa BXH tổng thể
        logics_list.append(lambda s: s['recent_ranks'][len(s['recent_ranks']) // 2]) # 47. Con có rank ở giữa BXH gần đây
        logics_list.append(lambda s: s['coldest_to_hottest'][len(s['coldest_to_hottest']) // 2]) # 48. Con có độ nóng/lạnh ở giữa
        logics_list.append(lambda s: [c for c in s['overall_ranks'] if c not in s['recent_ranks'][:3]][0]) # 49. Top 1 tổng thể nhưng không nằm trong top 3 gần đây (con "cũ mà mạnh")
        logics_list.append(lambda s: [c for c in s['recent_ranks'] if c not in s['overall_ranks'][:3]][0]) # 50. Top 1 gần đây nhưng không nằm trong top 3 tổng thể (con "mới nổi")
        
        return logics_list

    def analyze_and_select(self, user_id, issue_id):
        # --- BƯỚC 1: KIỂM TRA ĐIỀU KIỆN ---
        # Nếu không đủ dữ liệu, chọn ngẫu nhiên để tránh lỗi
        if len(self.history_data) < self.recency_window:
            return random.choice(list(NV.keys()))

        # --- BƯỚC 2: TẠO "HẠT GIỐNG" DUY NHẤT (CƠ CHẾ LÀM NHIỄU & PHÂN TÁN) ---
        # Kết hợp user_id và issue_id để tạo ra một chuỗi độc nhất
        seed_str = f"{user_id}-{issue_id}"
        # Dùng SHA256 để băm chuỗi, tạo ra một giá trị gần như ngẫu nhiên nhưng có thể lặp lại nếu input giống nhau
        hash_hex = hashlib.sha256(seed_str.encode()).hexdigest()
        # Chuyển giá trị hash thành một số nguyên lớn
        hash_int = int(hash_hex, 16)
        
        # --- BƯỚC 3: CHỌN LOGIC ---
        # Dùng số vừa tạo để chọn một logic từ danh sách 50 logic.
        # Mỗi user, mỗi ván sẽ có một logic khác nhau.
        logic_index = hash_int % len(self.logics)
        selected_logic = self.logics[logic_index]
        
        # --- BƯỚC 4: THỰC THI LOGIC VÀ TRẢ KẾT QUẢ ---
        stats = self._get_stats()
        if not stats:
            return random.choice(list(NV.keys())) # Fallback an toàn

        try:
            # Chạy logic đã chọn để tìm ra nhân vật cần né
            final_choice = selected_logic(stats)
        except (IndexError, KeyError, TypeError):
            # Nếu logic được chọn bị lỗi (ví dụ: lịch sử quá ngắn), quay về logic an toàn nhất
            final_choice = stats['overall_ranks'][0]

        # Đảm bảo kết quả luôn hợp lệ
        if final_choice not in NV.keys():
             final_choice = stats['overall_ranks'][0]

        return final_choice

# =====================================================================================
# KẾT THÚC PHẦN LOGIC NÂNG CẤP
# =====================================================================================

logic_engine = LogicEngine()

# =====================================================================================
# PHẦN GIAO DIỆN VÀ HIỂN THỊ (ĐÃ SỬA LỖI)
# =====================================================================================

def clear_screen():
    """
    Xóa màn hình console một cách mượt mà bằng mã ANSI.
    Di chuyển con trỏ về góc trái trên và xóa toàn bộ nội dung.
    """
    print("\033[H\033[J", end="")

def format_time(seconds):
    if seconds < 0: return "0 ngày 0 giờ 0 phút"
    days = int(seconds // (24 * 3600)); seconds %= (24 * 3600)
    hours = int(seconds // 3600); seconds %= 3600
    minutes = int(seconds // 60)
    return f"{days} ngày {hours} giờ {minutes} phút"

def add_log(logs_deque, message):
    hanoi_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    timestamp = datetime.now(hanoi_tz).strftime('%H:%M:%S')
    logs_deque.append(f"{Colors.TEXT_LABEL}{timestamp}{Colors.RESET} {message}")

def display_dashboard(config, stats, wallet_asset, htr, logs, coin_type, status_message=""):
    """
    Hàm chịu trách nhiệm vẽ toàn bộ giao diện người dùng.
    Nó sẽ xóa màn hình, sau đó dựng lại toàn bộ bảng điều khiển với dữ liệu mới nhất.
    Tất cả nội dung được gom vào một chuỗi và in ra một lần để chống nháy và chống trôi.
    """
    clear_screen()

    bet_amount0 = config['bet_amount0']
    heso = config['heso']
    start_time = config['start_time']
    total_games = stats['win'] + stats['lose']

    last_result_str = f"{Colors.WHITE}CHƯA CÓ"
    if htr:
        last_result_str = f"{Colors.PROFIT}THẮNG" if htr[-1]['kq'] else f"{Colors.LOSS}THUA"

    profit = wallet_asset.get(coin_type, 0) - stats['asset_0']
    profit_color = Colors.PROFIT if profit >= 0 else Colors.LOSS
    profit_str = f"{profit_color}{profit:+.4f} {coin_type}{Colors.RESET}"

    ls1, ls2, ls3, ls4 = stats.get('lose_streak_1', 0), stats.get('lose_streak_2', 0), stats.get('lose_streak_3', 0), stats.get('lose_streak_4', 0)

    dashboard_lines = []
    WIDTH = 64
    BORDER_COLOR = Colors.BORDER

    # Header
    dashboard_lines.append(f"{Colors.HEADER}{' ' * ((WIDTH - 12) // 2)}TOOL VIP V9{' ' * ((WIDTH - 12) // 2)}{Colors.RESET}")
    dashboard_lines.append(f"{BORDER_COLOR}═" * WIDTH)

    # 1. Nhật ký hoạt động
    dashboard_lines.append(f"{Colors.HEADER}NHẬT KÝ HOẠT ĐỘNG{Colors.RESET}")
    log_lines = list(logs)
    for log_entry in reversed(log_lines):
        dashboard_lines.append(log_entry)
    dashboard_lines.append(f"{BORDER_COLOR}═" * WIDTH)

    # 2. Trạng thái hiện tại (Đang đợi kết quả, v.v.)
    if status_message:
        dashboard_lines.append(status_message)
        dashboard_lines.append(f"{BORDER_COLOR}═" * WIDTH)

    # 3. Bảng thống kê chi tiết
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Thời Gian Chạy: {Colors.CYAN}{format_time(time.time() - start_time)}{Colors.RESET}")
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Phiên Bản:      {Colors.TEXT_VALUE}LOGIC V9{Colors.RESET}")
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Lợi Nhuận:      {profit_str}")
    dashboard_lines.append(f"{BORDER_COLOR}─" * WIDTH)
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Tổng Trận:      {Colors.TEXT_VALUE}{total_games}{Colors.RESET}")
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Thắng/Thua:     {Colors.PROFIT}{stats['win']}{Colors.RESET} / {Colors.LOSS}{stats['lose']}{Colors.RESET}")
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Chuỗi Thắng:    {Colors.PROFIT}{stats['streak']} (Max: {stats['max_streak']}){Colors.RESET}")
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Chuỗi Thua:     {Colors.LOSS}{stats['lose_streak']}{Colors.RESET}")
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Số Lần Thua(1/2/3/4): {Colors.TEXT_VALUE}{ls1}/{ls2}/{ls3}/{ls4}{Colors.RESET}")
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Kết Quả Trước:  {last_result_str}")
    dashboard_lines.append(f"{BORDER_COLOR}─" * WIDTH)
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Cược Cơ Bản:    {Colors.YELLOW}{bet_amount0} {coin_type}{Colors.RESET}")
    dashboard_lines.append(f"{Colors.TEXT_LABEL}● Hệ Số Gấp:      {Colors.YELLOW}{heso}{Colors.RESET}")
    dashboard_lines.append(f"{BORDER_COLOR}─" * WIDTH)
    dashboard_lines.append(f"{Colors.WHITE}Số Dư Hiện Tại:{Colors.RESET}")
    dashboard_lines.append(f"  {Colors.YELLOW}BUILD: {Colors.TEXT_VALUE}{wallet_asset.get('BUILD', 0.0):,.4f}{Colors.RESET}")
    dashboard_lines.append(f"  {Colors.MAGENTA}WORLD: {Colors.TEXT_VALUE}{wallet_asset.get('WORLD', 0.0):,.4f}{Colors.RESET}")
    dashboard_lines.append(f"  {Colors.GREEN}USDT:  {Colors.TEXT_VALUE}{wallet_asset.get('USDT', 0.0):,.4f}{Colors.RESET}")

    # In toàn bộ nội dung đã được xây dựng ra màn hình trong một lần duy nhất
    print('\n'.join(dashboard_lines))

# =====================================================================================
# CÁC HÀM LOGIC VÀ API (GIỮ NGUYÊN)
# =====================================================================================

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        print(f"{Colors.CYAN}Tìm thấy file dữ liệu đã lưu. Bạn có muốn sử dụng không? (y/n): {Colors.WHITE}", end='')
        if input().lower() == 'y':
            with open('data-xw-cdtd.txt', 'r', encoding='utf-8') as f: return json.load(f)
    print(f"\n{Colors.YELLOW}Hướng dẫn lấy link:\n1. Truy cập xworld.io và đăng nhập\n2. Vào game 'Chạy đua tốc độ'\n3. Copy link của trang game và dán vào đây{Colors.RESET}")
    print(f"{Colors.CYAN}📋 Vui lòng nhập link của bạn: {Colors.WHITE}", end=''); link = input()
    user_id = re.search(r'userId=(\d+)', link).group(1)
    secret_key = re.search(r'secretKey=([a-zA-Z0-9]+)', link).group(1)
    print(f"{Colors.GREEN}    ✓ Lấy thông tin thành công! User ID: {user_id}")
    json_data = {'user-id': user_id, 'user-secret-key': secret_key}
    with open('data-xw-cdtd.txt', 'w+', encoding='utf-8') as f: json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data

def populate_initial_history(s, headers):
    print(f"\n{Colors.GREEN}Đang lấy dữ liệu lịch sử ban đầu...{Colors.RESET}")
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers, timeout=5).json()
        if response and response['data']['recent_10']:
            for issue_data in reversed(response['data']['recent_10']): logic_engine.add_result(issue_data['result'][0])
            print(f"{Colors.GREEN}✓ Nạp thành công lịch sử {len(response['data']['recent_10'])} ván.{Colors.RESET}"); return True
    except Exception as e: print(f"{Colors.RED}Lỗi khi nạp lịch sử: {e}{Colors.RESET}")
    return False

def fetch_latest_issue_info(s, headers):
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers, timeout=5).json()
        if response and response['data']['recent_10']:
            latest_issue = response['data']['recent_10'][0]; return latest_issue['issue_id'], latest_issue
    except Exception: return None, None
    return None, None

def check_issue_result(s, headers, kq, ki):
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers, timeout=5).json()
        for issue in response['data']['recent_10']:
            if int(issue['issue_id']) == int(ki):
                actual_winner = issue['result'][0]; return actual_winner != kq, actual_winner
    except Exception: return None, None
    return None, None

def user_asset(s, headers):
    try:
        json_data = {'user_id': int(headers['user-id']), 'source': 'home'}
        return s.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data, timeout=5).json()['data']['user_asset']
    except Exception as e:
        print(f"{Colors.LOSS}Lỗi khi lấy số dư: {e}. Thử lại...{Colors.RESET}"); time.sleep(2); return user_asset(s, headers)

def bet_cdtd(s, headers, ki, kq, Coin, bet_amount, logs):
    try:
        json_data = {'issue_id': int(ki), 'bet_group': 'not_winner', 'asset_type': Coin, 'athlete_id': kq, 'bet_amount': bet_amount}
        response = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json=json_data, timeout=10).json()
        if not (response.get('code') == 0 and response.get('msg') == 'ok'):
            log_msg = f"{Colors.RED}Lỗi cược: {response.get('msg', 'Không rõ lỗi')}"
            add_log(logs, log_msg)
        return response
    except requests.exceptions.RequestException as e:
        add_log(logs, f"{Colors.RED}Lỗi mạng khi đặt cược: {e}")
        return None

# Vòng lặp chính của tool
def main_cdtd():
    s = requests.Session()
    data = load_data_cdtd()
    headers = {'user-id': data['user-id'], 'user-secret-key': data['user-secret-key'], 'user-agent': 'Mozilla/5.0'}

    os.system('cls' if platform.system() == "Windows" else 'clear')

    asset = user_asset(s, headers)
    print(f"\n{Colors.CYAN}Chọn loại tiền bạn muốn chơi:{Colors.RESET}\n  1. USDT\n  2. BUILD\n  3. WORLD")
    while True:
        print(f"{Colors.CYAN}Nhập lựa chọn (1/2/3): {Colors.WHITE}", end=''); x = input()
        if x in ['1', '2', '3']: Coin = ['USDT', 'BUILD', 'WORLD'][int(x)-1]; break
        else: print(f"{Colors.LOSS}Lựa chọn không hợp lệ, vui lòng nhập lại...{Colors.RESET}")
    bet_amount0 = float(input(f'{Colors.CYAN}Nhập số {Coin} muốn đặt ban đầu: {Colors.WHITE}'))
    heso = int(input(f'{Colors.CYAN}Nhập hệ số cược sau khi thua: {Colors.WHITE}'))
    delay1 = int(input(f'{Colors.CYAN}Chơi bao nhiêu ván thì nghỉ (999 nếu không nghỉ): {Colors.WHITE}'))
    delay2 = int(input(f'{Colors.CYAN}Nghỉ trong bao nhiêu ván: {Colors.WHITE}'))

    stats = {'win': 0, 'lose': 0, 'streak': 0, 'max_streak': 0, 'lose_streak': 0, 'asset_0': asset.get(Coin, 0), 'total_bet': 0.0, 'lose_streak_1': 0, 'lose_streak_2': 0, 'lose_streak_3': 0, 'lose_streak_4': 0}
    config = {'bet_amount0': bet_amount0, 'heso': heso, 'start_time': time.time()}
    htr = []; logs = deque(maxlen=10); tong_van = 0

    populate_initial_history(s, headers); time.sleep(2)

    last_known_id, _ = fetch_latest_issue_info(s, headers)
    if not last_known_id:
        print(f"{Colors.RED}Không thể lấy ID ván đầu tiên. Vui lòng kiểm tra lại mạng và API.{Colors.RESET}")
        sys.exit()

    while True:
        try:
            current_asset = user_asset(s, headers)
            status_msg = f"{Colors.YELLOW}Đang chờ ván #{last_known_id + 1} bắt đầu...{Colors.RESET}"
            display_dashboard(config, stats, current_asset, htr, logs, Coin, status_message=status_msg)

            newly_completed_id = last_known_id
            while newly_completed_id == last_known_id:
                time.sleep(1)
                newly_completed_id, newly_completed_issue_data = fetch_latest_issue_info(s, headers)
                if newly_completed_id is None: newly_completed_id = last_known_id

            last_known_id = newly_completed_id
            if newly_completed_issue_data and 'result' in newly_completed_issue_data:
                logic_engine.add_result(newly_completed_issue_data['result'][0])

            target_issue_id = last_known_id + 1; tong_van += 1
            bet_amount = bet_amount0
            if stats['lose_streak'] > 0: bet_amount = bet_amount0 * (heso ** stats['lose_streak'])

            kq = logic_engine.analyze_and_select(data['user-id'], target_issue_id)
            cycle = delay1 + delay2
            pos = (tong_van - 1) % cycle if cycle > 0 else 0
            is_resting = pos >= delay1

            if not is_resting and kq is not None:
                response = bet_cdtd(s, headers, target_issue_id, kq, Coin, bet_amount, logs)
                if response and response.get('code') == 0:
                    stats['total_bet'] += bet_amount
                    start_wait_time = time.time()
                    while True:
                        result, actual_winner = check_issue_result(s, headers, kq, target_issue_id)
                        if result is not None: break
                        elapsed = int(time.time() - start_wait_time)
                        wait_message = f"{Colors.YELLOW}⏳ Đang đợi kết quả kì #{target_issue_id}: {elapsed}s | {Colors.CYAN}Đã cược: {Colors.WHITE}{bet_amount:.4f} {Coin} (Né {NV.get(kq, kq)})"
                        display_dashboard(config, stats, current_asset, htr, logs, Coin, status_message=wait_message)
                        time.sleep(1)

                    htr.append({'kq': result, 'bet_amount': bet_amount})
                    log_msg = ""
                    if result:
                        ended_lose_streak = stats['lose_streak']
                        if ended_lose_streak == 1: stats['lose_streak_1'] += 1
                        elif ended_lose_streak == 2: stats['lose_streak_2'] += 1
                        elif ended_lose_streak == 3: stats['lose_streak_3'] += 1
                        elif ended_lose_streak >= 4: stats['lose_streak_4'] += 1

                        logic_engine.record_win(); stats['win'] += 1; stats['streak'] += 1; stats['lose_streak'] = 0
                        stats['max_streak'] = max(stats['max_streak'], stats['streak'])
                        log_msg = (f"{Colors.PROFIT}THẮNG{Colors.RESET} - Cược né {Colors.WHITE}{NV.get(kq, kq)}{Colors.RESET}, KQ về {Colors.CYAN}{NV.get(actual_winner, actual_winner)}{Colors.RESET}")
                    else:
                        logic_engine.record_loss(kq); stats['lose'] += 1; stats['lose_streak'] += 1; stats['streak'] = 0
                        log_msg = (f"{Colors.LOSS}THUA{Colors.RESET} - Cược né {Colors.WHITE}{NV.get(kq, kq)}{Colors.RESET}, KQ về {Colors.RED}{NV.get(actual_winner, actual_winner)}{Colors.RESET} (Trùng)")

                    add_log(logs, log_msg)
                    final_asset = user_asset(s, headers)
                    display_dashboard(config, stats, final_asset, htr, logs, Coin)
                    delay_next_round = random.uniform(5, 10); time.sleep(delay_next_round)
            else:
                rest_msg = ""
                if kq is None: rest_msg = f"{Colors.YELLOW}💤 Bỏ qua ván này do không đủ dữ liệu."
                else: rest_msg = f"{Colors.YELLOW}💤 Ván này tạm nghỉ. Tiếp tục sau {cycle - pos} ván nữa."

                add_log(logs, rest_msg)
                display_dashboard(config, stats, current_asset, htr, logs, Coin, status_message=rest_msg)
                time.sleep(30)

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Đã dừng tool. Cảm ơn bạn đã sử dụng!{Colors.RESET}"); sys.exit()
        except Exception as e:
            add_log(logs, f"{Colors.RED}Lỗi không xác định: {e}. Tự khởi động lại sau 10s.")
            time.sleep(10)

def show_banner():
    clear_screen()
    banner = f"""
{Colors.CYAN}
 ████████╗██████╗ ██╗  ██╗
 ╚══██╔══╝██╔══██╗██║ ██╔╝
    ██║   ██║  ██║█████╔╝
    ██║   ██║  ██║██╔═██╗
    ██║   ██████╔╝██║  ██╗
    ╚═╝   ╚═════╝ ╚═╝  ╚═╝
{Colors.RESET}
    """
    print(banner)
    print(f"{Colors.HEADER}Tool VIP V9- Khởi tạo thành công!{Colors.RESET}\n")
    time.sleep(3)

if __name__ == "__main__":
    authentication_successful = main_authentication()

    if authentication_successful:
        show_banner()
        main_cdtd()
    else:
        print(f"\n{do}Xác thực không thành công. Vui lòng chạy lại tool.{end}")
        sys.exit()
