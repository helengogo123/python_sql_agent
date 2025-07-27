import requests
import json
import base64

# ==== 步骤 1：配置 ====
TENANT_ID = "f7c6a981-a51b-4dcb-b13b-6bb826519ac6"
CLIENT_ID = "50265012-fefc-4d9c-9003-bbcee43a1d34"
CLIENT_SECRET = "7D5sRGKzwZ~AA8XenS_~3fC_oJz65Y.Byn"
WORKSPACE_ID = "d2718968-7f3c-43f6-a6a5-45dd4a37df78"  # 如：d2718968-7f3c-43f6-a6a5-45dd4a37df78

# ==== 步骤 2：获取 access_token ====
token_url = f"https://login.chinacloudapi.cn/{TENANT_ID}/oauth2/v2.0/token"
payload = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://analysis.chinacloudapi.cn/powerbi/api/.default'
}

response = requests.post(token_url, data=payload)
if response.status_code != 200:
    print("❌ 获取 token 失败")
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    exit()

access_token = response.json()['access_token']
print("✅ 已获取 access_token")
# ==== 步骤 2.5：获取所有 workspace 列表，检查权限 ====
groups_url = "https://api.powerbi.cn/v1.0/myorg/groups"
groups_headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
groups_response = requests.get(groups_url, headers=groups_headers)
print("\n📡 正在获取 workspace 列表 ...")
print("状态码:", groups_response.status_code)
try:
    groups_data = groups_response.json()
    print("\n📝 可访问的 workspace 列表：")
    for group in groups_data.get("value", []):
        print(f"- 名称: {group.get('name')}, ID: {group.get('id')}")
except Exception as e:
    print("⚠️ workspace 结果解析失败:", e)
    print("响应内容:", groups_response.text)

# ==== 步骤 3：调 Power BI 报表列表 API ====
api_url = f"https://api.powerbi.cn/v1.0/myorg/groups/{WORKSPACE_ID}/reports"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

report_response = requests.get(api_url, headers=headers)
print("\n📡 正在调用 Power BI 报表列表 API ...")
print("状态码:", report_response.status_code)

try:
    report_data = report_response.json()
    print("\n📝 返回报表列表如下：")
    for report in report_data.get("value", []):
        print(f"- 📄 报表名称: {report['name']}, ID: {report['id']}")
except Exception as e:
    print("⚠️ 报表结果解析失败:", e)
    print("响应内容:", report_response.text)
