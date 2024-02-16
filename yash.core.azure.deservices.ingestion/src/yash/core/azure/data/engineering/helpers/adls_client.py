from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class ADLSClient:

    def __init__(self, storage_account_name, kv_name, kv_secret_name, file_system, file_path):
        self.storage_account_name = storage_account_name
        self.kv_name = kv_name
        self.kv_secret_name = kv_secret_name
        self.file_system = file_system
        self.file_path = file_path

    def _get_keyvault_secret(self):
        client = SecretClient(vault_url=f"https://{self.kv_name}.vault.azure.net",
                              credential=DefaultAzureCredential())
        retrieved_secret = client.get_secret(self.kv_secret_name)
        return retrieved_secret.value

    def _get_adls_client(self, storage_account_key):
        adls_client = DataLakeServiceClient(account_url=f"https://{self.storage_account_name}.dfs.core.windows.net/",
                                            credential=storage_account_key)
        return adls_client

    def get_file_client(self):
        '''
        Get the ADLS file client

        Args:
            storage_account_name: ADLS storage account name
            kv_name: KV name
            kv_secret_name: KV secret name for ADLS storage account key
            file_system: container name
            file_path: file path

        Returns: the ADLS file client

        '''
        secret_value = self._get_keyvault_secret()
        adls_client = self._get_adls_client(secret_value)
        return adls_client.get_file_client(file_system=self.file_system, file_path=self.file_path)

    def download_file(self, dest_path):
        '''
        Download file from ADLS to destination path

        Args:
            storage_account_name: ADLS storage account name
            kv_name: KV name
            kv_secret_name: KV secret name for ADLS storage account key
            file_system: container name
            file_path: file path
            dest_path: destination file path

        '''
        file = self.get_file_client()
        with open(dest_path, "wb") as my_file:
            download = file.download_file()
            download.readinto(my_file)
