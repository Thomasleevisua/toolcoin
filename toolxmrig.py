import psutil
import requests
import subprocess
import time

# Cấu hình thông tin pool và ví Monero
pool = "pool.supportxmr.com:3333"
wallet_address = "YOUR_MONERO_WALLET_ADDRESS"  # Thay bằng địa chỉ ví Monero của bạn
worker_name = "my_worker"
threads = 4  # Số luồng CPU bạn muốn sử dụng

# Cấu hình Telegram Bot
telegram_token = 'YOUR_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'

# Cấu hình thời gian gửi báo cáo (đơn vị: giây)
report_interval = 3600  # 3600 giây = 1 giờ

# Cấu hình lệnh chạy XMRig
xmrig_command = (f'./xmrig -o {pool} -u {wallet_address} -p {worker_name} '
                 f'--cpu-max-threads-hint={threads} --donate-level=1')

def send_telegram_message(text):
    """Gửi tin nhắn tới bot Telegram"""
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, data=payload)

def get_system_usage():
    """Lấy thông tin về CPU, RAM và mạng"""
    cpu_usage = psutil.cpu_percent(interval=1)  # Lấy phần trăm sử dụng CPU
    ram_usage = psutil.virtual_memory().percent  # Lấy phần trăm sử dụng RAM
    
    # Lấy thông tin mạng (tốc độ download và upload)
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent / (1024 * 1024)  # Đổi từ bytes sang MB
    bytes_recv = net_io.bytes_recv / (1024 * 1024)  # Đổi từ bytes sang MB
    
    return cpu_usage, ram_usage, bytes_sent, bytes_recv

def start_miner():
    """Khởi động quá trình đào coin"""
    print("Starting XMRig miner...")
    process = subprocess.Popen(xmrig_command, shell=True)
    return process

def monitor_miner(process):
    """Theo dõi và kiểm tra trạng thái của miner"""
    last_report_time = time.time()  # Lấy thời gian hiện tại khi bắt đầu
    try:
        while True:
            time.sleep(60)  # Kiểm tra mỗi phút
            if process.poll() is not None:
                send_telegram_message("Miner stopped. Restarting...")
                print("Miner stopped. Restarting...")
                process = start_miner()

            # Kiểm tra xem có cần gửi báo cáo hay không
            if time.time() - last_report_time >= report_interval:
                cpu_usage, ram_usage, bytes_sent, bytes_recv = get_system_usage()
                message = (f"📊 CPU Usage: {cpu_usage}%\n"
                           f"💾 RAM Usage: {ram_usage}%\n"
                           f"📤 Data Sent: {bytes_sent:.2f} MB\n"
                           f"📥 Data Received: {bytes_recv:.2f} MB")
                send_telegram_message(message)
                last_report_time = time.time()  # Cập nhật thời gian gửi báo cáo
    except KeyboardInterrupt:
        print("Stopping miner...")
        process.terminate()

if __name__ == "__main__":
    miner_process = start_miner()
    monitor_miner(miner_process)
