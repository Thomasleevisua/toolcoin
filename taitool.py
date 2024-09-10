import requests
import os
import zipfile
import tarfile

# Đường dẫn các repo GitHub
XMRIG_URL = "https://api.github.com/repos/xmrig/xmrig/releases/latest"
SRBMiner_URL = "https://api.github.com/repos/doktor83/SRBMiner-Multi/releases/latest"

# Lấy thư mục hiện tại (nơi đang chạy tool)
DOWNLOAD_DIR = os.getcwd()

# Hàm tải về file từ GitHub
def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    local_filename = os.path.join(dest_folder, url.split("/")[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# Hàm giải nén file ZIP
def extract_zip(file_path, dest_folder):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)

# Hàm giải nén file TAR
def extract_tar(file_path, dest_folder):
    with tarfile.open(file_path, 'r:gz') as tar_ref:
        tar_ref.extractall(dest_folder)

# Lấy link tải phù hợp dựa trên hệ điều hành người dùng chọn
def get_download_link(release_data, miner_name, os_choice):
    assets = release_data['assets']
    for asset in assets:
        if os_choice in asset['name'].lower():
            return asset['browser_download_url']
    raise Exception(f"Không tìm thấy file tải về cho {miner_name} cho hệ điều hành {os_choice}")

# Tải phiên bản mới nhất của XMRig
def download_xmrig(os_choice):
    print(f"Đang tải về XMRig cho hệ điều hành {os_choice}...")
    response = requests.get(XMRIG_URL)
    response.raise_for_status()
    release_data = response.json()
    download_url = get_download_link(release_data, "XMRig", os_choice)
    file_path = download_file(download_url, DOWNLOAD_DIR)
    
    # Giải nén file .zip hoặc .tar.gz
    if file_path.endswith(".zip"):
        extract_zip(file_path, DOWNLOAD_DIR)
    elif file_path.endswith(".tar.gz"):
        extract_tar(file_path, DOWNLOAD_DIR)
    
    print("XMRig đã được tải về và giải nén thành công.")

# Tải phiên bản mới nhất của SRBMiner-MULTI
def download_srbminer(os_choice):
    print(f"Đang tải về SRBMiner-MULTI cho hệ điều hành {os_choice}...")
    response = requests.get(SRBMiner_URL)
    response.raise_for_status()
    release_data = response.json()
    download_url = get_download_link(release_data, "SRBMiner-MULTI", os_choice)
    file_path = download_file(download_url, DOWNLOAD_DIR)
    
    # Giải nén file .zip hoặc .tar.gz
    if file_path.endswith(".zip"):
        extract_zip(file_path, DOWNLOAD_DIR)
    elif file_path.endswith(".tar.gz"):
        extract_tar(file_path, DOWNLOAD_DIR)
    
    print("SRBMiner-MULTI đã được tải về và giải nén thành công.")

# Hỏi người dùng chọn tool khai thác
def ask_for_tool():
    while True:
        print("Bạn muốn tải tool khai thác nào?")
        print("1: XMRig")
        print("2: SRBMiner-MULTI")
        choice = input("Chọn số 1 hoặc 2: ")
        if choice == '1':
            return 'xmrig'
        elif choice == '2':
            return 'srbminer'
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

# Hỏi người dùng chọn hệ điều hành
def ask_for_os():
    while True:
        print("Bạn cần tải tool cho hệ điều hành nào?")
        print("1: Linux")
        print("2: Windows")
        os_choice = input("Chọn số 1 hoặc 2: ")
        if os_choice == '1':
            return 'linux'
        elif os_choice == '2':
            return 'windows'
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    # Hỏi người dùng chọn tool và hệ điều hành
    miner_choice = ask_for_tool()
    os_choice = ask_for_os()

    # Tải và giải nén dựa trên lựa chọn của người dùng
    if miner_choice == 'xmrig':
        download_xmrig(os_choice)
    elif miner_choice == 'srbminer':
        download_srbminer(os_choice)

    print(f"Tất cả các miner đã được tải về tại: {os.path.abspath(DOWNLOAD_DIR)}")
