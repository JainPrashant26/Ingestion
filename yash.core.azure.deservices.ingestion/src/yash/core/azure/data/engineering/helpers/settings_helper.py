from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import yaml
import json
import os


class SettingsHelper():

    def __init__(self, config_file_path, test_file_path, keyvault_name):
        self.test_config = self._load_test_config(test_file_path)
        self.yaml_config = self._load_yaml_config(config_file_path)
        self.kv_client = self._get_kv_client(self.yaml_config[keyvault_name])

    @staticmethod
    def _load_test_config(test_file_path):
        with open(test_file_path) as f:
            test_config = json.load(f)
        return test_config

    @staticmethod
    def _load_yaml_config(yaml_file_path):
        with open(yaml_file_path) as f:
            parsed_yaml_file = yaml.load(f, Loader=yaml.FullLoader)
            config = parsed_yaml_file["variables"]
        return config

    @staticmethod
    def _get_kv_client(kv_name):
        kv_uri = f"https://{kv_name}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kv_uri, credential=credential)
        return client

    def get_setting(self, setting_name):
        '''
        Get the given setting name from Environment Variable, Test config file, Yaml configuration file, Key Vault in this order.

        Args:
            setting_name: The name of the setting

        Returns: The setting value if found. Otherwise, raise an Exception.

        '''
        try:
            setting_value = os.getenv(setting_name)
            if setting_value:
                return setting_value

            setting_value = self.test_config.get(setting_name, None)
            if setting_value:
                return setting_value

            setting_value = self.yaml_config.get(setting_name, None)
            if setting_value:
                return setting_value

            setting_value = self.kv_client.get_secret(setting_name)
            if setting_value:
                return setting_value

        except Exception:
            raise Exception(f"Setting '{setting_name}' not found")
