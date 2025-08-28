import urllib.request
import ssl
import os
import time

# URL to access
url = "https://4.237.224.16"

# Certificate file (optional, since we disable verification)
cert_file = r"C:/Fortinet_CA_SSL.cer"

# Ensure the certificate file exists (optional check)
if not os.path.exists(cert_file):
    print(f"Warning: Certificate file '{cert_file}' not found. Proceeding without it.")

# Create a custom SSL context with the most lenient settings
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    context.load_verify_locations(cert_file)
except Exception as e:
    print(f"Warning: Could not load certificate (proceeding anyway): {e}")

# 增强版重试逻辑 --------------------------------------------------
max_retries = 3
retry_delay = 2
results = []

print(f"🚀 Starting {max_retries} connection attempts to {url}\n")

for attempt in range(max_retries):
    attempt_result = {"number": attempt+1, "status": "", "content": "", "error": ""}
    start_time = time.time()
    
    try:
        # 显示进度条动画
        print(f"Attempt {attempt+1}/{max_retries} [{'▒'*(attempt+1)}{' '*(max_retries-attempt-1)}]", end="\r")
        
        # 发起请求
        response = urllib.request.urlopen(url, context=context, timeout=10)
        process_time = time.time() - start_time
        
        # 读取内容
        content = response.read().decode()
        
        # 记录成功结果
        attempt_result["status"] = "success"
        attempt_result["content"] = content
        results.append(attempt_result)
        
        # 即使成功也继续后续尝试
        time.sleep(retry_delay)  # 保持请求间隔
        continue
        
    except Exception as e:
        process_time = time.time() - start_time
        attempt_result["status"] = "failed"
        attempt_result["error"] = str(e)
        results.append(attempt_result)
        
        if attempt < max_retries - 1:
            time.sleep(retry_delay)

# 最终结果分析
success_count = sum(1 for r in results if r["status"] == "success")
failure_count = max_retries - success_count

# 打印详细报告
print("\n\n📊 Connection Report:")
print(f"✅ Successful attempts: {success_count}")
print(f"❌ Failed attempts: {failure_count}")
print("─" * 50)

for idx, result in enumerate(results, 1):
    print(f"\nAttempt #{idx} ({result['status'].upper()}):")
    if result["status"] == "success":
        print(f"├─ Response preview: {result['content'][:100]}...")
    else:
        print(f"├─ Error: {result['error'][:100]}...")
    print(f"└─ Duration: {time.time() - start_time:.2f}s")

print("\n" + "═" * 50)
if success_count > 0:
    print("🎉 Final Status: AT LEAST ONE SUCCESSFUL CONNECTION")
else:
    print("💥 Final Status: ALL CONNECTION ATTEMPTS FAILED")