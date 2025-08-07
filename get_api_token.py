import paramiko
import time
import json
import warnings
from paramiko.ssh_exception import SSHException, AuthenticationException



# FortiGate 设备列表（确保每个元素是字典）
fortigates = [
    {
        "host": "59.110.142.139",
        "port": 22,
        "username": "admin",
        "password": "fortinet@123",
        "api_user": "api1"
    },

]

def configure_fortigate_api_user(device):
    """
    通过SSH登录FortiGate，配置API用户并生成API Key
    :param device: 设备配置（host, port, username, password, api_user）
    :return: API Key（字符串），失败返回 None
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            device["host"],
            port=device["port"],
            username=device["username"],
            password=device["password"],
            timeout=10
        )
        shell = client.invoke_shell()
        shell.settimeout(5)
        time.sleep(1)
        output = shell.recv(65535).decode()
        
        # 配置API用户
        shell.send("config system api-user\n")
        time.sleep(1)
        shell.send(f"edit {device['api_user']}\n")
        time.sleep(1)
        shell.send("set accprofile \"super_admin\"\n")
        time.sleep(1)
        shell.send("set comments \"Automated API User\"\n")
        time.sleep(1)
        shell.send("next\n")
        time.sleep(1)
        shell.send("end\n")
        time.sleep(1)
        
        # 生成API Key
        shell.send(f"execute api-user generate-key {device['api_user']}\n")
        time.sleep(2)
        output = shell.recv(65535).decode()
        
        if "New API key:" in output:
            api_key_line = [line for line in output.split('\n') if "New API key:" in line][0]
            api_key = api_key_line.split(":")[1].strip()
        else:
            print(f"生成API Key失败: {device['host']} - 输出: {output}")
            return None
        
        client.close()
        return api_key
    
    except (SSHException, AuthenticationException, TimeoutError) as e:
        print(f"SSH连接失败: {device['host']} - 错误: {str(e)}")
        return None

if __name__ == "__main__":
    api_keys = {}
    
    # 确保遍历的是字典列表
    for fgt in fortigates:
        print(f"\n===== 正在配置设备: {fgt['host']} =====")  # 确保fgt是字典
        key = configure_fortigate_api_user(fgt)
        if key:
            api_keys[fgt["host"]] = {
                "api_user": fgt["api_user"],
                "api_key": key
            }
            print(f"成功生成 API Key: {key}")
        else:
            print("配置失败")
    
    # 保存到JSON文件
    with open("fortigate_api_keys.json", "w") as f:
        json.dump(api_keys, f, indent=2)
    print("\n===== API Key 已保存至 fortigate_api_keys.json =====")