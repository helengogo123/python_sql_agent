from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient

def get_secret_from_key_vault(key_vault_name: str, secret_name: str) -> str:
    """
    从 Azure Key Vault 获取指定 secret。

    参数:
        key_vault_name: Key Vault 的名称（不含 https:// 和 .vault.azure.cn）
        secret_name: Secret 在 Vault 中的名称

    返回:
        Secret 的值（字符串）
    """
    key_vault_url = f"https://{key_vault_name}.vault.azure.cn/"
    credential = AzureCliCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    
    retrieved_secret = client.get_secret(secret_name)
    return retrieved_secret.value
