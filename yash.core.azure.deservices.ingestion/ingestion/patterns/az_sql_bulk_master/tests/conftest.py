import pytest
from pathlib import Path

from yash.core.azure.data.engineering.helpers.settings_helper import SettingsHelper
from yash.core.azure.data.engineering.helpers.adf_client import ADFClient


@pytest.fixture
def settings():
    adf_config_file_path = Path(__file__).parents[1] / "development.variables.yml"
    test_config_file_path = Path(__file__).parent / "test_param_az_sql_bulk_master.json"
    settings = SettingsHelper(adf_config_file_path, test_config_file_path, "SINK-LS-KEYVAULT-NAME")
    return settings


@pytest.fixture
def adf_client(settings):
    adf_client = ADFClient(settings.get_setting("az-subscription-id"),
                           settings.get_setting("adf-rg-name"),
                           settings.get_setting("adf-name"),
                           settings.get_setting("pipeline_name"))
    return adf_client
