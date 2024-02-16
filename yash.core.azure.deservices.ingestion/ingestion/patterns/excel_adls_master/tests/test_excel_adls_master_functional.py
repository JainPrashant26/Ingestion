import pytest

from yash.core.azure.data.engineering.helpers.adls_client import *
pytest.mark.usefixtures("adf_client")


def test_e2e_run_excel_ingestion_master(adf_client, settings):
    # Run the pipeline with default parameters & assert pipeline run is successful # noqa
    pipeline_result, run_id = adf_client.run_pipeline(settings.test_config)
    assert pipeline_result == 'Succeeded'
# excel_adls_master