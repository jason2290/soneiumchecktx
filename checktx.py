import requests
import csv

# 設定代理（格式: "http://帳號:密碼@IP:PORT"）
proxy = "http://"
proxies = {"http": proxy, "https": proxy}

# API 地址
API_BASE = "https://soneium.blockscout.com/api/v2/addresses"

# 讀取地址
with open("address.txt", "r") as file:
    addresses = [line.strip() for line in file if line.strip()]

# 定義 CSV 檔案
csv_file = "result.csv"

# 寫入 CSV 標題
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["address", "transactions_count", "gas_usage_count", "token_transfers_count", "validations_count"])

# 逐個請求 API
for address in addresses:
    url = f"{API_BASE}/{address}/counters"
    
    try:
        response = requests.get(url, headers={"accept": "application/json"}, proxies=proxies, timeout=10)
        data = response.json()

        # 提取數據，避免 KeyError
        transactions_count = data.get("transactions_count", "0")
        gas_usage_count = data.get("gas_usage_count", "0")
        token_transfers_count = data.get("token_transfers_count", "0")
        validations_count = data.get("validations_count", "0")

        # 寫入 CSV
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([address, transactions_count, gas_usage_count, token_transfers_count, validations_count])

        print(f"已處理: {address}")
    
    except Exception as e:
        print(f"錯誤: {address} - {e}")

print(f"所有地址處理完成，結果保存在 {csv_file}")
