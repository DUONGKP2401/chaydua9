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
import platform
import subprocess
import hashlib
import statistics
import string
import urllib.parse

# Check và cài đặt các thư viện cần thiết
try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style, init
    import pystyle
    init(autoreset=True) # init() từ v9.py để đảm bảo màu sắc reset đúng cách
except ImportError:
    print('__Đang cài đặt các thư viện cần thiết, vui lòng chờ...__')
    os.system("pip install faker requests colorama bs4 pystyle rich")
    os.system("pip3 install requests pysocks")
    print('__Cài đặt hoàn tất, vui lòng chạy lại Tool__')
    sys.exit()


# =====================================================================================
# PHẦN 2: MÃ NGUỒN TỪ FILE banner.py (HỆ THỐNG XÁC THỰC)
# =====================================================================================

# --- Cấu hình và các biến màu sắc ---
VIP_KEY_URL = "https://raw.githubusercontent.com/DUONGKP2401/KEY-VIP.txt/main/KEY-VIP.txt"
VIP_CACHE_FILE = 'vip_cache.json'
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

# Đổi tên hàm 'banner' của file banner.py thành 'authentication_banner' để tránh xung đột
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

{vang}Admin: DUONG PHUNG
{vang}Nhóm Zalo: https://zalo.me/g/ddxsyp497
{vang}Tele: @tankeko12
{trang}══════════════════════════
"""
    for char in banner_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.0001)

# --- Các hàm lấy thông tin thiết bị ---
def get_device_id():
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
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json().get('ip')
    except Exception as e:
        print(f"{do}Lỗi khi lấy địa chỉ IP: {e}{trang}")
        return None

def display_machine_info(ip_address, device_id):
    authentication_banner() # Gọi hàm banner đã đổi tên
    if ip_address:
        print(f"{trang}[{do}<>{trang}] {do}Địa chỉ IP: {vang}{ip_address}{trang}")
    else:
        print(f"{do}Không thể lấy địa chỉ IP của thiết bị.{trang}")
    if device_id:
        print(f"{trang}[{do}<>{trang}] {do}Mã Máy: {vang}{device_id}{trang}")
    else:
        print(f"{do}Không thể lấy Mã Máy của thiết bị.{trang}")

# --- Các hàm xử lý Key Free ---
def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))
    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def kiem_tra_ip(ip):
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
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'VTD9{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://tdkvuatocdo.blogspot.com/2025/09/key-vtdv9_18.html?m={key}'
    return url, key, expiration_date

def get_shortened_link_phu(url):
    try:
        token = "6725c7b50c661e3428736919"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=5)
        return response.json() if response.status_code == 200 else {"status": "error", "message": "Lỗi kết nối dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

# =============================================================================
# BẮT ĐẦU PHẦN SỬA LỖI
# =============================================================================

def process_free_key(ip_address):
    url, key, expiration_date = generate_key_and_url(ip_address)
    yeumoney_data = get_shortened_link_phu(url)
    if yeumoney_data.get('status') == "error":
        print(yeumoney_data.get('message'))
        return False
    link_key_yeumoney = yeumoney_data.get('shortenedUrl')
    print(f'{trang}[{do}<>{trang}] {hong}Link Để Vượt Key Là {xnhac}: {link_key_yeumoney}{trang}')
    while True:
        # SỬA LỖI: Thêm .strip() để loại bỏ khoảng trắng thừa khi người dùng nhập key
        keynhap = input(f'{trang}[{do}<>{trang}] {vang}Key Đã Vượt Là: {luc}').strip()
        if keynhap == key:
            print(f'{luc}Key Đúng! Mời Bạn Dùng Tool{trang}')
            sleep(2)
            luu_thong_tin_ip(ip_address, keynhap, expiration_date)
            return True
        else:
            print(f'{trang}[{do}<>{trang}] {hong}Key Sai! Vui Lòng Vượt Lại Link {xnhac}: {link_key_yeumoney}{trang}')

# --- Các hàm xử lý Key VIP ---
def save_vip_key_info(device_id, key, expiration_date_str):
    data = {'device_id': device_id, 'key': key, 'expiration_date': expiration_date_str}
    encrypted_data = encrypt_data(json.dumps(data))
    with open(VIP_CACHE_FILE, 'w') as file:
        file.write(encrypted_data)
    print(f"{luc}Đã lưu thông tin Key VIP cho lần đăng nhập sau.{trang}")

def load_vip_key_info():
    try:
        with open(VIP_CACHE_FILE, 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return None

def display_remaining_time(expiry_date_str):
    try:
        expiry_date = datetime.strptime(expiry_date_str, '%d/%m/%Y').replace(hour=23, minute=59, second=59)
        now = datetime.now()
        if expiry_date > now:
            delta = expiry_date - now
            days, remainder = delta.days, delta.seconds
            hours, remainder = divmod(remainder, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"{xnhac}Key VIP của bạn còn lại: {luc}{days} ngày, {hours} giờ, {minutes} phút.{trang}")
        else:
            print(f"{do}Key VIP của bạn đã hết hạn.{trang}")
    except ValueError:
        print(f"{vang}Không thể xác định ngày hết hạn của key.{trang}")

def check_vip_key(machine_id, user_key):
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
                        return ('valid', key_ngay_het_han) if expiry_date.date() >= datetime.now().date() else ('expired', None)
                    except ValueError: continue
        return 'not_found', None
    except requests.exceptions.RequestException as e:
        print(f"{do}Lỗi kết nối đến server key: {e}{trang}")
        return 'error', None

# --- Luồng xác thực chính ---
def main_authentication():
    ip_address = get_ip_address()
    device_id = get_device_id()
    display_machine_info(ip_address, device_id)
    if not ip_address or not device_id:
        print(f"{do}Không thể lấy thông tin thiết bị. Vui lòng kiểm tra kết nối mạng.{trang}")
        return False, None

    cached_vip_info = load_vip_key_info()
    if cached_vip_info and cached_vip_info.get('device_id') == device_id:
        try:
            expiry_date = datetime.strptime(cached_vip_info['expiration_date'], '%d/%m/%Y')
            if expiry_date.date() >= datetime.now().date():
                print(f"{luc}Đã tìm thấy Key VIP hợp lệ, tự động đăng nhập...{trang}")
                display_remaining_time(cached_vip_info['expiration_date'])
                sleep(3)
                return True, device_id
            else:
                print(f"{vang}Key VIP đã lưu đã hết hạn. Vui lòng nhập key mới.{trang}")
        except (ValueError, KeyError):
            print(f"{do}Lỗi file lưu key. Vui lòng nhập lại key.{trang}")

    if kiem_tra_ip(ip_address):
        print(f"{trang}[{do}<>{trang}] {hong}Key free hôm nay vẫn còn hạn. Mời bạn dùng tool...{trang}")
        time.sleep(2)
        return True, device_id

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
                    return True, device_id
                elif status == 'expired': print(f"{do}Key VIP của bạn đã hết hạn. Vui lòng liên hệ admin.{trang}")
                elif status == 'not_found': print(f"{do}Key VIP không hợp lệ hoặc không tồn tại cho mã máy này.{trang}")
                else: print(f"{do}Đã xảy ra lỗi trong quá trình xác thực. Vui lòng thử lại.{trang}")
                sleep(2)
            elif choice == '2':
                if process_free_key(ip_address):
                    return True, device_id
            else:
                print(f"{vang}Lựa chọn không hợp lệ, vui lòng nhập 1 hoặc 2.{trang}")
        except KeyboardInterrupt:
            print(f"\n{trang}[{do}<>{trang}] {do}Cảm ơn bạn đã dùng Tool !!!{trang}")
            sys.exit()

# =============================================================================
# KẾT THÚC PHẦN SỬA LỖI
# =============================================================================

# =====================================================================================
# PHẦN 3: MÃ NGUỒN TỪ FILE v9.py (TOOL GAME AI)
# =====================================================================================
NV = {
    1: '⚔️ Bậc thầy tấn công', 2: '👊 Quyền sắt', 3: '🤿 Thợ lặn sâu',
    4: '⚽ Cơn lốc sân cỏ', 5: '🏇 Hiệp sĩ phi nhanh', 6: '⚾ Vua home run'
}

class SmartAI:
    def __init__(self, device_id):
        self.device_id = device_id
        # Tạo một giá trị seed duy nhất cho mỗi người dùng dựa trên device_id
        # để đảm bảo tính ngẫu nhiên khác nhau giữa các máy
        self.user_seed = int(hashlib.sha256(device_id.encode()).hexdigest(), 16) % (10**8)
        self.total_logics = 50
        self.current_logic = 0
        self.selection_history = deque(maxlen=10)
        self.result_history = deque(maxlen=20)
        self.logic_performance = {i: {'wins': 0, 'total': 0, 'win_rate': 0.0} for i in range(1, self.total_logics + 1)}
        self.all_chars = list(range(1, 7))

    def _get_user_random_choice(self, items):
        """Chọn một phần tử ngẫu nhiên từ danh sách dựa trên seed của người dùng."""
        if not items: return None
        # Kết hợp seed của người dùng với thời gian hiện tại để tăng độ ngẫu nhiên mỗi lần chạy
        current_seed = self.user_seed + int(time.time() * 1000)
        rng = random.Random(current_seed)
        return rng.choice(items)

    def add_result(self, selected, actual_winner):
        is_win = (selected != actual_winner)
        self.result_history.append({'selected': selected, 'winner': actual_winner, 'is_win': is_win, 'logic_used': self.current_logic})
        if self.current_logic in self.logic_performance:
            perf = self.logic_performance[self.current_logic]
            perf['total'] += 1
            if is_win: perf['wins'] += 1
            perf['win_rate'] = perf['wins'] / perf['total'] if perf['total'] > 0 else 0.0

    def check_triple_pattern(self):
        if len(self.selection_history) >= 3:
            last_three = list(self.selection_history)[-3:]
            if len(set(last_three)) == 1: return True, last_three[0]
        return False, None

    def get_safe_alternatives(self, avoid_char, top100_data):
        alternatives = [i for i in self.all_chars if i != avoid_char]
        try:
            win_counts = {char: top100_data[1][char - 1] for char in alternatives}
            # Sắp xếp các lựa chọn thay thế theo số lần thắng tăng dần
            sorted_alternatives = sorted(alternatives, key=lambda char: win_counts[char])
            return sorted_alternatives
        except: return alternatives

    # =============================================================================
    # BẮT ĐẦU 50 LOGIC MỚI
    # =============================================================================

    def get_logic_function(self, logic_id):
        logics = {
            1: self.logic_1, 2: self.logic_2, 3: self.logic_3, 4: self.logic_4, 5: self.logic_5,
            6: self.logic_6, 7: self.logic_7, 8: self.logic_8, 9: self.logic_9, 10: self.logic_10,
            11: self.logic_11, 12: self.logic_12, 13: self.logic_13, 14: self.logic_14, 15: self.logic_15,
            16: self.logic_16, 17: self.logic_17, 18: self.logic_18, 19: self.logic_19, 20: self.logic_20,
            21: self.logic_21, 22: self.logic_22, 23: self.logic_23, 24: self.logic_24, 25: self.logic_25,
            26: self.logic_26, 27: self.logic_27, 28: self.logic_28, 29: self.logic_29, 30: self.logic_30,
            31: self.logic_31, 32: self.logic_32, 33: self.logic_33, 34: self.logic_34, 35: self.logic_35,
            36: self.logic_36, 37: self.logic_37, 38: self.logic_38, 39: self.logic_39, 40: self.logic_40,
            41: self.logic_41, 42: self.logic_42, 43: self.logic_43, 44: self.logic_44, 45: self.logic_45,
            46: self.logic_46, 47: self.logic_47, 48: self.logic_48, 49: self.logic_49, 50: self.logic_50,
        }
        return logics.get(logic_id)

    # --- NHÓM 1: DỰA TRÊN TẦN SUẤT (TOP 100) ---
    def logic_1(self, top10, top100): # Chọn ngẫu nhiên từ 2 NV có tỷ lệ thắng thấp nhất trong top 100
        win_counts = sorted(zip(self.all_chars, top100[1]), key=lambda x: x[1])
        return self._get_user_random_choice([win_counts[0][0], win_counts[1][0]])

    def logic_2(self, top10, top100): # Tránh 2 NV có tỷ lệ thắng cao nhất trong top 100
        win_counts = sorted(zip(self.all_chars, top100[1]), key=lambda x: x[1], reverse=True)
        avoid = [win_counts[0][0], win_counts[1][0]]
        return self._get_user_random_choice([c for c in self.all_chars if c not in avoid])

    def logic_3(self, top10, top100): # Chọn NV có tỷ lệ thắng gần nhất với mức trung bình
        avg_wins = sum(top100[1]) / len(top100[1])
        closest = sorted(self.all_chars, key=lambda c: abs(top100[1][c-1] - avg_wins))
        return closest[0]

    def logic_4(self, top10, top100): # Chọn ngẫu nhiên từ các NV có tỷ lệ thắng dưới trung bình
        avg_wins = sum(top100[1]) / len(top100[1])
        below_avg = [c for c in self.all_chars if top100[1][c-1] < avg_wins]
        return self._get_user_random_choice(below_avg or self.all_chars)

    def logic_5(self, top10, top100): # Tránh NV thắng nhiều nhất và ít nhất trong top 100
        win_counts = sorted(zip(self.all_chars, top100[1]), key=lambda x: x[1])
        avoid = [win_counts[0][0], win_counts[-1][0]]
        return self._get_user_random_choice([c for c in self.all_chars if c not in avoid])

    # --- NHÓM 2: DỰA TRÊN XU HƯỚNG GẦN ĐÂY (TOP 10) ---
    def logic_6(self, top10, top100): # Tránh NV thắng ở ván gần nhất
        last_winner = top10[1][0] if top10[1] else None
        return self._get_user_random_choice([c for c in self.all_chars if c != last_winner] or self.all_chars)

    def logic_7(self, top10, top100): # Chọn NV chưa xuất hiện trong 3 ván gần nhất
        recent_3 = top10[1][:3]
        not_in_recent_3 = [c for c in self.all_chars if c not in recent_3]
        return self._get_user_random_choice(not_in_recent_3 or self.all_chars)

    def logic_8(self, top10, top100): # Tránh NV xuất hiện nhiều nhất trong 5 ván gần nhất
        if len(top10[1]) < 5: return self.logic_6(top10, top100)
        most_common = Counter(top10[1][:5]).most_common(1)[0][0]
        return self._get_user_random_choice([c for c in self.all_chars if c != most_common] or self.all_chars)

    def logic_9(self, top10, top100): # Chọn NV xuất hiện ít nhất trong 10 ván gần nhất
        if not top10[1]: return self._get_user_random_choice(self.all_chars)
        counts = Counter(top10[1])
        min_count = min(counts.values())
        least_common = [c for c, count in counts.items() if count == min_count]
        return self._get_user_random_choice(least_common)

    def logic_10(self, top10, top100): # Tránh 2 NV thắng ở 2 ván gần nhất (nếu khác nhau)
        if len(top10[1]) < 2: return self.logic_6(top10, top100)
        avoid = list(set(top10[1][:2]))
        return self._get_user_random_choice([c for c in self.all_chars if c not in avoid] or self.all_chars)
    
    # --- NHÓM 3: KẾT HỢP DỮ LIỆU TOP 10 VÀ TOP 100 ---
    def logic_11(self, top10, top100): # Chọn NV có tỷ lệ thắng thấp (top 100) và chưa thắng trong 3 ván gần nhất (top 10)
        win_counts = sorted(zip(self.all_chars, top100[1]), key=lambda x: x[1])
        low_perf = [c[0] for c in win_counts[:3]]
        recent_winners = top10[1][:3]
        candidates = [c for c in low_perf if c not in recent_winners]
        return self._get_user_random_choice(candidates or low_perf)

    def logic_12(self, top10, top100): # Tránh NV thắng nhiều nhất (top 100) và NV thắng gần nhất (top 10)
        max_winner_100 = max(zip(self.all_chars, top100[1]), key=lambda x: x[1])[0]
        last_winner_10 = top10[1][0] if top10[1] else None
        avoid = list(set([max_winner_100, last_winner_10]))
        return self._get_user_random_choice([c for c in self.all_chars if c not in avoid] or self.all_chars)

    def logic_13(self, top10, top100): # Chọn từ 2 NV có tỷ lệ thắng cao nhất (top 100) nếu chúng không thắng trong 2 ván gần nhất (top 10)
        win_counts = sorted(zip(self.all_chars, top100[1]), key=lambda x: x[1], reverse=True)
        top_perf = [win_counts[0][0], win_counts[1][0]]
        recent_winners = top10[1][:2]
        candidates = [c for c in top_perf if c not in recent_winners]
        return self._get_user_random_choice(candidates or [c for c in self.all_chars if c not in recent_winners])

    def logic_14(self, top10, top100): # Phân tích "độ nóng": Chọn NV có tỷ lệ thắng cao (top 100) nhưng lại ít xuất hiện gần đây (top 10)
        win_counts_100 = {c: count for c, count in zip(self.all_chars, top100[1])}
        counts_10 = Counter(top10[1])
        scores = {c: win_counts_100.get(c, 0) - counts_10.get(c, 0) * 10 for c in self.all_chars}
        best_char = max(scores, key=scores.get)
        return best_char
        
    def logic_15(self, top10, top100): # Đảo ngược logic 14: Chọn NV có tỷ lệ thắng thấp (top 100) nhưng xuất hiện nhiều gần đây (top 10)
        win_counts_100 = {c: count for c, count in zip(self.all_chars, top100[1])}
        counts_10 = Counter(top10[1])
        scores = {c: counts_10.get(c, 0) * 10 - win_counts_100.get(c, 0) for c in self.all_chars}
        best_char = max(scores, key=scores.get)
        return best_char

    # --- NHÓM 4: DỰA TRÊN LỊCH SỬ CỦA AI ---
    def logic_16(self, top10, top100): # Tránh NV mà AI đã chọn ở lượt trước
        if not self.selection_history: return self._get_user_random_choice(self.all_chars)
        last_selected = self.selection_history[-1]
        return self._get_user_random_choice([c for c in self.all_chars if c != last_selected] or self.all_chars)

    def logic_17(self, top10, top100): # Nếu AI thua ở lượt trước, tránh cả NV đã chọn và NV đã thắng
        if not self.result_history or self.result_history[-1]['is_win']: return self.logic_16(top10, top100)
        last_result = self.result_history[-1]
        avoid = [last_result['selected'], last_result['winner']]
        return self._get_user_random_choice([c for c in self.all_chars if c not in avoid] or self.all_chars)

    def logic_18(self, top10, top100): # Tránh NV mà AI đã chọn và bị thua nhiều nhất
        losses = [r['selected'] for r in self.result_history if not r['is_win']]
        if not losses: return self._get_user_random_choice(self.all_chars)
        most_lost_char = Counter(losses).most_common(1)[0][0]
        return self._get_user_random_choice([c for c in self.all_chars if c != most_lost_char] or self.all_chars)
        
    def logic_19(self, top10, top100): # Lặp lại lựa chọn gần nhất đã mang lại chiến thắng cho AI
        wins = [r['selected'] for r in reversed(self.result_history) if r['is_win']]
        if wins: return wins[0]
        return self.logic_1(top10, top100) # Fallback

    def logic_20(self, top10, top100): # Tránh chọn lặp lại 1 NV 3 lần liên tiếp
        if len(self.selection_history) >= 2 and self.selection_history[-1] == self.selection_history[-2]:
            avoid = self.selection_history[-1]
            return self._get_user_random_choice([c for c in self.all_chars if c != avoid] or self.all_chars)
        return self.logic_1(top10, top100) # Fallback

    # --- NHÓM 5: LOGIC DỰA TRÊN MÃ MÁY (USER-SPECIFIC) ---
    def logic_21(self, top10, top100): # Chọn NV dựa trên một phép toán đơn giản với mã máy
        return (self.user_seed % 6) + 1

    def logic_22(self, top10, top100): # Tạo một danh sách ưu tiên cá nhân dựa trên mã máy và chọn NV đầu tiên không phải là người thắng cuối cùng
        shuffled_chars = sorted(self.all_chars, key=lambda x: (x + self.user_seed) % 7)
        last_winner = top10[1][0] if top10[1] else None
        for char in shuffled_chars:
            if char != last_winner: return char
        return shuffled_chars[0]

    def logic_23(self, top10, top100): # Dịch chuyển lựa chọn từ NV ít thắng nhất dựa trên mã máy
        min_winner = min(zip(self.all_chars, top100[1]), key=lambda x: x[1])[0]
        offset = (self.user_seed // 100) % 6
        return ((min_winner - 1 + offset) % 6) + 1
        
    def logic_24(self, top10, top100): # Tránh NV thắng nhiều nhất, sau đó chọn từ các NV còn lại dựa trên mã máy
        max_winner = max(zip(self.all_chars, top100[1]), key=lambda x: x[1])[0]
        candidates = [c for c in self.all_chars if c != max_winner]
        return self._get_user_random_choice(candidates)

    def logic_25(self, top10, top100): # Chọn NV dựa trên tổng số của top 10 kết quả gần nhất và mã máy
        if not top10[1]: return self.logic_21(top10, top100)
        total = sum(top10[1])
        return ((total + self.user_seed) % 6) + 1
        
    # --- THÊM 25 LOGIC ĐA DẠNG KHÁC ---
    def logic_26(self, top10, top100): # Theo chuỗi: nếu 1-2-1-2, tránh 1
        if len(top10[1]) >= 4 and top10[1][0] == top10[1][2] and top10[1][1] == top10[1][3]:
            return self._get_user_random_choice([c for c in self.all_chars if c != top10[1][1]])
        return self.logic_7(top10, top100)

    def logic_27(self, top10, top100): # Chọn NV có độ lệch so với trung bình lớn nhất (cả trên và dưới)
        avg_wins = sum(top100[1]) / len(top100[1])
        deviations = {c: abs(top100[1][c-1] - avg_wins) for c in self.all_chars}
        return max(deviations, key=deviations.get)

    def logic_28(self, top10, top100): # Tránh NV vừa thắng và NV có tỷ lệ thắng thấp nhất trong top 100
        last_winner = top10[1][0] if top10[1] else None
        min_winner_100 = min(zip(self.all_chars, top100[1]), key=lambda x: x[1])[0]
        avoid = list(set([last_winner, min_winner_100]))
        return self._get_user_random_choice([c for c in self.all_chars if c not in avoid] or self.all_chars)

    def logic_29(self, top10, top100): # Phản logic: Chọn ngẫu nhiên từ 2 NV thắng nhiều nhất top 100
        win_counts = sorted(zip(self.all_chars, top100[1]), key=lambda x: x[1], reverse=True)
        return self._get_user_random_choice([win_counts[0][0], win_counts[1][0]])

    def logic_30(self, top10, top100): # Chọn NV chưa thắng trong 5 ván gần nhất
        recent_5 = set(top10[1][:5])
        candidates = [c for c in self.all_chars if c not in recent_5]
        return self._get_user_random_choice(candidates or self.all_chars)

    def logic_31(self, top10, top100): # Dựa trên số ván thắng của chính AI: chẵn chọn NV ít thắng, lẻ chọn NV nhiều thắng (top 100)
        win_counts = sorted(zip(self.all_chars, top100[1]), key=lambda x: x[1])
        my_wins = len([r for r in self.result_history if r['is_win']])
        if my_wins % 2 == 0:
            return self._get_user_random_choice([win_counts[0][0], win_counts[1][0]])
        else:
            return self._get_user_random_choice([win_counts[-1][0], win_counts[-2][0]])

    def logic_32(self, top10, top100): # Tránh các NV tạo thành một cặp gần đây (ví dụ: 1-2, 1-2)
        if len(top10[1]) >= 4 and top10[1][:2] == top10[1][2:4]:
            avoid = top10[1][:2]
            return self._get_user_random_choice([c for c in self.all_chars if c not in avoid] or self.all_chars)
        return self.logic_8(top10, top100)

    def logic_33(self, top10, top100): # Chọn NV đối diện trên vòng tròn (1-4, 2-5, 3-6) với NV thắng cuối
        last_winner = top10[1][0] if top10[1] else self._get_user_random_choice(self.all_chars)
        opposite = (last_winner + 2) % 6 + 1
        return opposite

    def logic_34(self, top10, top100): # Nếu ván trước AI thắng, chọn NV khác với lựa chọn trước. Nếu thua, giữ nguyên logic cũ.
        if self.result_history and self.result_history[-1]['is_win']:
             last_selected = self.result_history[-1]['selected']
             return self._get_user_random_choice([c for c in self.all_chars if c != last_selected] or self.all_chars)
        return self.logic_17(top10, top100) # Fallback

    def logic_35(self, top10, top100): # Dựa vào số chẵn/lẻ của kỳ hiện tại (nếu có) và mã máy
        current_issue = top10[0][0] + 1 if top10[0] else int(time.time())
        seed = current_issue + self.user_seed
        if seed % 2 == 0:
            return self.logic_1(top10, top100) # Chọn NV ít thắng
        else:
            return self.logic_2(top10, top100) # Tránh NV nhiều thắng

    def logic_36(self, top10, top100): # Chọn NV có số lần thắng là số nguyên tố
        win_counts = top100[1]
        def is_prime(n):
            if n <= 1: return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0: return False
            return True
        prime_win_chars = [i+1 for i, count in enumerate(win_counts) if is_prime(count)]
        return self._get_user_random_choice(prime_win_chars or self.all_chars)
        
    def logic_37(self, top10, top100): # Dựa vào Markov chain đơn giản: dự đoán NV tiếp theo và tránh nó
        if len(top10[1]) < 2: return self.logic_6(top10, top100)
        transitions = defaultdict(list)
        for i in range(len(top10[1]) - 1, 0, -1):
            transitions[top10[1][i]].append(top10[1][i-1])
        last_winner = top10[1][0]
        if last_winner in transitions:
            predictions = Counter(transitions[last_winner]).most_common(1)
            if predictions:
                avoid = predictions[0][0]
                return self._get_user_random_choice([c for c in self.all_chars if c != avoid] or self.all_chars)
        return self.logic_6(top10, top100)

    def logic_38(self, top10, top100): # Tránh 3 NV có tần suất xuất hiện cao nhất trong top 10
        if len(top10[1]) < 3: return self.logic_10(top10, top100)
        counts = Counter(top10[1]).most_common(3)
        avoid = [item[0] for item in counts]
        return self._get_user_random_choice([c for c in self.all_chars if c not in avoid] or self.all_chars)

    def logic_39(self, top10, top100): # Chọn 1 NV từ 3 NV có tần suất xuất hiện thấp nhất trong top 100
        win_counts = sorted(zip(self.all_chars, top100[1]), key=lambda x: x[1])
        candidates = [c[0] for c in win_counts[:3]]
        return self._get_user_random_choice(candidates)

    def logic_40(self, top10, top100): # Logic "hồi quy về trung bình": Chọn NV có tỷ lệ thắng xa nhất bên dưới mức trung bình
        avg_wins = sum(top100[1]) / len(top100[1])
        below_avg = {c: avg_wins - top100[1][c-1] for c in self.all_chars if top100[1][c-1] < avg_wins}
        if not below_avg: return self.logic_3(top10, top100)
        return max(below_avg, key=below_avg.get)

    def logic_41(self, top10, top100): # Chọn NV cách NV thắng cuối 2 bước (ví dụ: thắng 1 -> chọn 4)
        last_winner = top10[1][0] if top10[1] else self._get_user_random_choice(self.all_chars)
        return ((last_winner - 1 + 3) % 6) + 1

    def logic_42(self, top10, top100): # Kết hợp logic 21 và 6: Chọn NV dựa trên mã máy, nhưng nếu trùng với NV thắng cuối thì chọn NV kế tiếp
        choice = (self.user_seed % 6) + 1
        last_winner = top10[1][0] if top10[1] else None
        if choice == last_winner:
            return ((choice % 6) + 1)
        return choice

    def logic_43(self, top10, top100): # Tránh các NV chẵn nếu kỳ là chẵn, và ngược lại.
        current_issue = top10[0][0] + 1 if top10[0] else int(time.time())
        if current_issue % 2 == 0: # Kỳ chẵn
            return self._get_user_random_choice([1, 3, 5])
        else: # Kỳ lẻ
            return self._get_user_random_choice([2, 4, 6])

    def logic_44(self, top10, top100): # Tránh NV mà AI đã chọn thắng ở lượt trước
        wins = [r['selected'] for r in self.result_history if r['is_win']]
        if not wins: return self.logic_1(top10, top100)
        last_win_selection = wins[-1]
        return self._get_user_random_choice([c for c in self.all_chars if c != last_win_selection] or self.all_chars)

    def logic_45(self, top10, top100): # Dựa trên sự thay đổi thứ hạng: Chọn NV có sự tăng hạng lớn nhất về số lần thắng so với 10 ván trước (giả lập)
        # Vì không có dữ liệu quá khứ, ta sẽ so sánh top 100 với top 10
        win_counts_100_normalized = [c / sum(top100[1]) for c in top100[1]]
        counts_10 = Counter(top10[1])
        win_counts_10_normalized = [counts_10.get(c, 0) / (len(top10[1]) or 1) for c in self.all_chars]
        momentum = {c: win_counts_10_normalized[c-1] - win_counts_100_normalized[c-1] for c in self.all_chars}
        # Chọn NV có momentum âm nhất (tụt dốc, có thể sắp bật lại)
        return min(momentum, key=momentum.get)

    def logic_46(self, top10, top100): # "Bão hòa": Tránh NV đã thắng 2 lần trong 4 ván gần nhất
        if len(top10[1]) < 4: return self.logic_6(top10, top100)
        counts = Counter(top10[1][:4])
        saturated = [c for c, count in counts.items() if count >= 2]
        if saturated:
             return self._get_user_random_choice([c for c in self.all_chars if c not in saturated] or self.all_chars)
        return self.logic_7(top10, top100)
        
    def logic_47(self, top10, top100): # Logic "cân bằng": Chọn NV sẽ làm cho độ lệch chuẩn của top 100 giảm nhiều nhất
        stdevs = {}
        for char_to_add in self.all_chars:
            temp_wins = list(top100[1])
            temp_wins[char_to_add-1] += 1
            stdevs[char_to_add] = statistics.stdev(temp_wins)
        return min(stdevs, key=stdevs.get)

    def logic_48(self, top10, top100): # Logic "ngẫu nhiên có trọng số ngược": Tỷ lệ chọn càng cao khi số lần thắng càng thấp
        win_counts = top100[1]
        total_wins = sum(win_counts)
        weights = [(total_wins - count) for count in win_counts]
        total_weight = sum(weights)
        if total_weight == 0: return self._get_user_random_choice(self.all_chars)
        
        # Tạo seed ngẫu nhiên kết hợp để đảm bảo tính nhất quán và đa dạng
        rng = random.Random(self.user_seed + int(time.time()))
        return rng.choices(self.all_chars, weights=weights, k=1)[0]

    def logic_49(self, top10, top100): # Chọn NV có số lần thắng (top 100) gần nhất với một số trong dãy Fibonacci
        fib = [1, 2, 3, 5, 8, 13, 21, 34, 55] # Dãy Fibonacci
        win_counts = top100[1]
        closest_char = -1
        min_dist = float('inf')
        for i, count in enumerate(win_counts):
            dist = min([abs(count - f) for f in fib])
            if dist < min_dist:
                min_dist = dist
                closest_char = i + 1
        return closest_char

    def logic_50(self, top10, top100): # Logic "hỗn loạn": Kết hợp mã máy, thời gian và kết quả gần nhất
        last_winner = top10[1][0] if top10[1] else 1
        timestamp = int(time.time())
        result = (self.user_seed + timestamp + last_winner) % 6 + 1
        return result
    
    # =============================================================================
    # KẾT THÚC 50 LOGIC MỚI
    # =============================================================================

    def next_logic(self):
        self.current_logic = (self.current_logic % self.total_logics) + 1
        return self.current_logic

    def analyze_and_select(self, top10_data, top100_data):
        try:
            is_triple, repeated_char = self.check_triple_pattern()
            if is_triple:
                safe_alternatives = self.get_safe_alternatives(repeated_char, top100_data)
                selected = self._get_user_random_choice(safe_alternatives) if safe_alternatives else self._get_user_random_choice(self.all_chars)
                logic_name = f"🛡️ ANTI-PATTERN (tránh {NV.get(repeated_char, 'N/A')})"
            else:
                current_logic_id = self.next_logic()
                logic_function = self.get_logic_function(current_logic_id)
                if logic_function:
                    selected = logic_function(top10_data, top100_data)
                else: # Fallback nếu logic không tồn tại
                    selected = self.logic_50(top10_data, top100_data)

                logic_name = f"🧠 LOGIC_{current_logic_id}"
            
            selected = int(selected)
            if not (1 <= selected <= 6): selected = self._get_user_random_choice(self.all_chars)
            self.selection_history.append(selected)
            return selected, logic_name
        except Exception as e:
            prints(255, 0, 0, f'❌ Lỗi AI: {e}')
            fallback = self._get_user_random_choice(self.all_chars)
            self.selection_history.append(fallback)
            return fallback, "🚨 FALLBACK_MODE"

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    print("\033[38;2;{};{};{}m{}\033[0m".format(r, g, b, text), end=end)

# Đổi tên hàm 'banner' của file v9.py thành 'game_banner' để tránh xung đột
def game_banner(game):
    banner_txt = """
████████╗██████╗ ██╗  ██╗
╚══██╔══╝██╔══██╗██║ ██╔╝
   ██║   ██████╔╝█████╔╝ 
   ██║   ██╔═══╝ ██╔═██╗ 
   ██║   ██║     ██║  ██╗
   ╚═╝   ╚═╝     ╚═╝  ╚═╝  
    """
    for i in banner_txt.split('\n'):
        x, y, z = 200, 255, 255
        for j in range(len(i)):
            prints(x, y, z, i[j], end='')
            x -= 4; time.sleep(0.001)
        print()
    prints(247, 255, 97, "✨" + "═" * 45 + "✨")
    prints(32, 230, 151, f"🌟 XWORLD AI - {game} v9.0🌟".center(47))
    prints(247, 255, 97, "═" * 47)
    prints(255, 215, 0, "🧠 50 NEW LOGIC AI SYSTEM 🧠".center(47))
    prints(255, 100, 100, "🛡️ ANTI-DETECTION & USER-UNIQUE 🛡️".center(47))
    prints(100, 255, 100, "🎯 DYNAMIC & UNPREDICTABLE 🎯".center(47))
    prints(247, 255, 97, "═" * 47)
    prints(7, 205, 240, "📱 Telegram: @tankeko12")
    prints(7, 205, 240, "👥 Nhóm Zalo: https://zalo.me/g/ddxsyp497 ")
    prints(7, 205, 240, "👨‍💼 Admin: Duong Phung ")
    prints(247, 255, 97, "═" * 47)

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        prints(0, 255, 243, 'Bạn có muốn sử dụng thông tin đã lưu hay không? (y/n): ', end='')
        if input().lower() == 'y':
            with open('data-xw-cdtd.txt', 'r', encoding='utf-8') as f:
                return json.load(f)
        prints(247, 255, 97, "═" * 47)
    guide = "Huướng dẫn lấy link:\n1.Truy cập xworld.io\n2.Đăng nhập\n3.Vào Chạy đua tốc độ\n4.Nhấn 'Lập tức truy cập'\n5.Copy link và dán vào đây"
    prints(218, 255, 125, guide)
    prints(247, 255, 97, "═" * 47)
    prints(125, 255, 168, '📋Nhập link của bạn: ', end=' ')
    link = input()
    user_id = link.split('?userId=')[1].split('&')[0]
    user_secretkey = link.split('secretKey=')[1].split('&')[0]
    prints(218, 255, 125, f'    User id: {user_id}')
    prints(218, 255, 125, f'    User secret key: {user_secretkey}')
    json_data = {'user-id': user_id, 'user-secret-key': user_secretkey}
    with open('data-xw-cdtd.txt', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data

def top_100_cdtd(s):
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_100_issues', headers={'user-agent': 'Mozilla/5.0'}).json()
        return list(range(1, 7)), [response['data']['athlete_2_win_times'][str(i)] for i in range(1, 7)]
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy top 100: {e}'); time.sleep(2); return top_100_cdtd(s)

def top_10_cdtd(s, headers):
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers).json()
        data = response['data']['recent_10']
        return [i['issue_id'] for i in data], [i['result'][0] for i in data]
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy top 10: {e}'); time.sleep(2); return top_10_cdtd(s, headers)

def kiem_tra_kq_cdtd(s, headers, kq, ki, smart_ai_instance):
    start = time.time()
    prints(0, 255, 37, f'⏰ Đang đợi kết quả của kì #{ki}...')
    while True:
        data_top10_cdtd = top_10_cdtd(s, headers)
        if int(data_top10_cdtd[0][0]) == int(ki):
            actual_winner = data_top10_cdtd[1][0]
            prints(0, 255, 30, f'🏆 Kết quả kì {ki}: {NV[int(actual_winner)]}')
            smart_ai_instance.add_result(kq, actual_winner)
            if actual_winner == kq:
                prints(255, 0, 0, '😔 Bạn đã thua. Chúc bạn may mắn lần sau!'); return False
            else:
                prints(0, 255, 37, '🎉 Xin chúc mừng! Bạn đã thắng!'); return True
        prints(0, 255, 197, f'⏳ Đang đợi kết quả... {time.time() - start:.0f}s', end='\r')
        time.sleep(2)

def user_asset(s, headers):
    try:
        response = s.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json={'user_id': int(headers['user-id']), 'source': 'home'}).json()
        asset_data = response.get('data', {}).get('user_asset', {})
        return {'USDT': float(asset_data.get('USDT', 0)), 'WORLD': float(asset_data.get('WORLD', 0)), 'BUILD': float(asset_data.get('BUILD', 0))}
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy số dư: {e}'); return {'USDT': 0.0, 'WORLD': 0.0, 'BUILD': 0.0}

def print_stats_cdtd(stats, s, headers, Coin, smart_ai_instance):
    try:
        asset = user_asset(s, headers)
        prints(70, 240, 234, '📊 Thống kê AI Performance:')
        win_rate = stats["win"] / (stats["win"] + stats["lose"]) * 100 if (stats["win"] + stats["lose"]) > 0 else 0
        prints(50, 237, 65, f'🎯 Tỷ lệ thắng: {stats["win"]}/{stats["win"]+stats["lose"]} ({win_rate:.1f}%)')
        prints(50, 237, 65, f'🔥 Chuỗi thắng: {stats["streak"]} (Max: {stats["max_streak"]})')
        loi = asset.get(Coin, 0) - stats.get('asset_0', 0)
        color, symbol = ((0, 255, 20), "📈") if loi >= 0 else ((255, 100, 100), "📉")
        prints(*color, f"{symbol} P&L: {loi:+.2f} {Coin}")
        best_logic = max(smart_ai_instance.logic_performance.items(), key=lambda x: x[1]['win_rate'] if x[1]['total'] > 0 else -1)
        if best_logic[1]['total'] > 0:
            prints(150, 255, 150, f"🧠 Best Logic: #{best_logic[0]} ({best_logic[1]['win_rate']:.1%})")
    except Exception as e: prints(255, 0, 0, f'❌ Lỗi thống kê: {e}')

def print_wallet(asset):
    prints(23, 232, 159, f'💰 USDT: {asset.get("USDT", 0):.2f} | 🌍 WORLD: {asset.get("WORLD", 0):.2f} | 🏗️ BUILD: {asset.get("BUILD", 0):.2f}'.center(60))

def bet_cdtd(s, headers, ki, kq, Coin, bet_amount):
    prints(255, 255, 0, f'💸 Đang đặt {bet_amount:.2f} {Coin} cho kì #{ki}...')
    try:
        json_data = {'issue_id': int(ki), 'bet_group': 'not_winner', 'asset_type': Coin, 'athlete_id': int(kq), 'bet_amount': float(bet_amount)}
        response = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json=json_data).json()
        if response.get('code') == 0 and response.get('msg') == 'ok':
            prints(0, 255, 19, f'✅ Đặt cược thành công vào "Ai không là quán quân"')
            prints(100, 255, 100, f'🎯 Target: Tránh {NV[int(kq)]}')
        else:
            prints(255, 100, 0, f'⚠️ Lỗi đặt cược: {response.get("msg", "Không rõ lỗi")}')
    except Exception as e:
        prints(255, 0, 0, f'❌ Lỗi hệ thống khi đặt cược: {e}')

def main_cdtd(device_id):
    s = requests.Session()
    smart_ai = SmartAI(device_id) # Khởi tạo AI với device_id
    game_banner("CHẠY ĐUA TỐC ĐỘ") # Gọi hàm banner đã đổi tên
    data = load_data_cdtd()
    headers = {'user-id': data['user-id'], 'user-secret-key': data['user-secret-key'], **{'accept': '*/*','user-agent': 'Mozilla/5.0','origin': 'https://xworld.info','referer': 'https://xworld.info/'}}
    asset = user_asset(s, headers)
    print_wallet(asset)
    prints(219, 237, 138, "💰 Chọn loại tiền:\n    1️⃣ USDT\n    2️⃣ BUILD\n    3️⃣ WORLD")
    while True:
        x = input('Nhập lựa chọn (1/2/3): ')
        if x in ['1', '2', '3']: Coin = ['USDT', 'BUILD', 'WORLD'][int(x)-1]; break
        else: prints(247, 30, 30, 'Nhập sai!', end='\r')
    bet_amount0 = float(input(f'Nhập số {Coin} muốn đặt: '))
    heso = float(input('Nhập hệ số cược sau thua: '))
    delay1 = int(input('Chơi bao nhiêu ván thì nghỉ (999 nếu không nghỉ): '))
    delay2 = int(input(f'Nghỉ bao nhiêu ván sau {delay1} ván chơi: '))
    stats = {'win': 0, 'lose': 0, 'streak': 0, 'max_streak': 0, 'asset_0': asset.get(Coin, 0)}
    clear_screen(); game_banner('CHẠY ĐUA TỐC ĐỘ')
    htr = []; tong = 0
    while True:
        tong += 1; prints(247, 255, 97, "═" * 47)
        print_wallet(user_asset(s, headers))
        data_top10, data_top100 = top_10_cdtd(s, headers), top_100_cdtd(s)
        bet_amount = (heso * htr[-1]['bet_amount']) if htr and not htr[-1]['kq'] else bet_amount0
        kq, logic_name = smart_ai.analyze_and_select(data_top10, data_top100)
        print_stats_cdtd(stats, s, headers, Coin, smart_ai)
        prints(0, 246, 255, f'🤖 AI V9 CHỌN: {NV.get(int(kq), "N/A")} ({logic_name})')
        
        pos = (tong - 1) % (delay1 + delay2) if (delay1 + delay2) > 0 else 0
        stop = pos >= delay1
        if not stop:
            bet_cdtd(s, headers, data_top10[0][0] + 1, kq, Coin, bet_amount)
        else:
            prints(255, 255, 0, 'Ván này tạm nghỉ theo lịch...'); bet_amount = bet_amount0
        
        result = kiem_tra_kq_cdtd(s, headers, kq, data_top10[0][0] + 1, smart_ai)
        if not stop:
            htr.append({'kq': result, 'bet_amount': bet_amount})
            if result: stats['win'] += 1; stats['streak'] += 1; stats['max_streak'] = max(stats['max_streak'], stats['streak'])
            else: stats['lose'] += 1; stats['streak'] = 0
        time.sleep(10)

# =====================================================================================
# PHẦN 4: ĐIỂM KHỞI ĐỘNG CHÍNH CỦA CHƯƠNG TRÌNH
# =====================================================================================
if __name__ == "__main__":
    try:
        # Bước 1: Chạy quy trình xác thực
        authentication_successful, device_id = main_authentication()

        # Bước 2: Nếu xác thực thành công, chạy tool game
        if authentication_successful:
            print("\n" + luc + "✅ Xác thực thành công! Đang khởi động tool game..." + trang)
            time.sleep(2)
            main_cdtd(device_id) # Truyền device_id vào tool game
        else:
            print("\n" + do + "❌ Xác thực không thành công. Không thể khởi động tool." + trang)
            time.sleep(3)
            sys.exit()
    except KeyboardInterrupt:
        print(f"\n{vang}Đã dừng tool theo yêu cầu người dùng. Tạm biệt!{trang}")
        sys.exit()
    except Exception as e:
        print(f"\n{do}Lỗi không xác định: {e}{trang}")
        # Ghi log lỗi để debug
        with open("error_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {str(e)}\n")
        sys.exit()

