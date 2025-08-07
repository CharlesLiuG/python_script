import requests
import time
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL警告（因为访问的是IP地址，证书可能不匹配）
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def visit_url(url, max_attempts=10):
    success_count = 0
    failure_count = 0
    
    print(f"开始循环访问 {url} - 共 {max_attempts} 次尝试")
    print("-" * 40)
    
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"尝试 #{attempt}: 正在访问 {url}...", end=' ', flush=True)
            
            # 发送GET请求（禁用SSL验证）
            response = requests.get(url, verify=False, timeout=10)
            
            print(f"成功! 状态码: {response.status_code}")
            success_count += 1
            
        except Exception as e:
            print(f"失败: {str(e)}")
            failure_count += 1
        
        # 如果不是最后一次尝试，则添加延迟
        if attempt < max_attempts:
            time.sleep(0.5)  # 500毫秒延迟
    
    print("\n" + "-" * 40)
    print("访问完成!")
    print(f"成功次数: {success_count}")
    print(f"失败次数: {failure_count}")
    print(f"总尝试次数: {max_attempts}")

if __name__ == "__main__":
    target_url = "https://4.237.224.16"
    visit_url(target_url)