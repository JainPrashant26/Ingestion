import pytest

from yash.core.azure.data.engineering.helpers.adls_client import *
pytest.mark.usefixtures("adf_client")


def test_e2e_run_sql_cdc_master_ingestion(adf_client, settings):
    # Run the pipeline with default parameters & assert pipeline run is successful # noqa
    pipeline_result, run_id = adf_client.run_pipeline(settings.test_config)
    assert pipeline_result == 'Succeeded'
