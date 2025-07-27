import msal
import requests
import time

TENANT_ID = "f7c6a981-a51b-4dcb-b13b-6bb826519ac6"
CLIENT_ID = '50265012-fefc-4d9c-9003-bbcee43a1d34'
CLIENT_SECRET = 'WQSp~fyMyX~B.6M6Yg_023upcQ8PP7~B.5'
WORKSPACE_ID = 'd2718968-7f3c-43f6-a6a5-45dd4a37df78'
REPORT_ID = '0607e987-ca79-43e9-806e-b1364bba22a5/ReportSection'
# 获取 Token
authority_url = f"https://login.microsoftonline.com/{TENANT_ID}"
app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=authority_url, client_credential=CLIENT_SECRET
)
token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
access_token = token_response["access_token"]

# 导出报表为 PNG
export_url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/exportTo"
export_body = {
    "format": "PNG",
    "powerBIReportConfiguration": {
        "pages": [{"pageName": "ReportSection1"}]  # 可自定义页面
    }
}
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
res = requests.post(export_url, json=export_body, headers=headers)
export_id = res.json()["id"]

# 轮询直到导出完成
status_url = f"https://api.powerbi.com/v1.0/myorg/reports/exportTo/{export_id}"
while True:
    res = requests.get(status_url, headers=headers)
    if res.json()["status"] == "Succeeded":
        file_url = res.json()["resourceLocation"]
        break
    time.sleep(3)

# 下载图片
img_data = requests.get(file_url, headers=headers).content
with open("report.png", "wb") as f:
    f.write(img_data)
