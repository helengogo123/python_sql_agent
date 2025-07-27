import requests
import json
import base64

# ✅ 替换为你自己的配置项
TENANT_ID = "f7c6a981-a51b-4dcb-b13b-6bb826519ac6"
CLIENT_ID = "50265012-fefc-4d9c-9003-bbcee43a1d34"
CLIENT_SECRET = "7D5sRGKzwZ~AA8XenS_~3fC_oJz65Y.Byn"

# ✅ token请求地址（中国区）
token_url = f"https://login.chinacloudapi.cn/{TENANT_ID}/oauth2/v2.0/token"

# ✅ 请求参数
payload = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://analysis.chinacloudapi.cn/powerbi/api/.default'
}

# ✅ 请求 token
response = requests.post(token_url, data=payload)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data["access_token"]
    print("✅ 成功获取 token")

    # ✅ 打印 token 前 100 字符
    print("\n🔑 Access Token (前100位):", access_token[:100] + "...")

    # ✅ 解码 token payload 查看 roles 是否包含
    parts = access_token.split(".")
    payload_base64 = parts[1] + '==='  # 补足 base64 padding
    payload_bytes = base64.urlsafe_b64decode(payload_base64)
    payload_json = json.loads(payload_bytes.decode('utf-8'))

    print("\n📦 解码后的 Token Payload:")
    print(json.dumps(payload_json, indent=2, ensure_ascii=False))

    # ✅ 检查是否有 roles 权限
    if "roles" in payload_json:
        print("\n✅ 包含权限 roles：", payload_json["roles"])
    else:
        print("\n❌ 没有 roles，说明 token 权限未生效（scope 配置错误或未管理员同意）")

else:
    print("❌ 获取 token 失败")
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
