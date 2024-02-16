from azure.identity import DefaultAzureCredential , ClientSecretCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import RunFilterParameters
import time
from datetime import datetime, timedelta


class ADFClient:

    def __init__(self, az_subscription_id, rg_name, df_name, pipeline_name):
        self.subscription_id = az_subscription_id
        self.rg_name = rg_name
        self.df_name = df_name
        self.pipeline_name = pipeline_name
        self.adf_client = self._get_client()

    def _get_client(self):
        # When run locally, DefaultAzureCredential relies on environment variables named
        # AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_TENANT_ID.
        #credential = DefaultAzureCredential()
        credential = ClientSecretCredential(tenant_id='e3451cda-1df3-414f-8ae3-c95281662c20',
                                             client_id='e6d709f5-ac89-437e-b2fd-f1fae80b7a9a',
                                             client_secret='aGZ8Q~SbNncf2rvjEJ4tth9i1ws-uYeZ7dgkfbRN')
        adf_client = DataFactoryManagementClient(credential, self.subscription_id)
        return adf_client

    def _overwrite_default_parameters(self, pipeline_default_parameters, test_params):
        # Overwrite params with json file
        for (parameter_name, parameter_value) in test_params.items():
            pipeline_default_parameters[parameter_name] = parameter_value
        return pipeline_default_parameters

    def _trigger_pipeline(self, parameters):
        pipeline_run = self.adf_client.pipelines.create_run(self.rg_name, self.df_name, self.pipeline_name,
                                                       parameters=parameters)
        return pipeline_run

    def _get_final_pipeline_state(self, create_pipeline_run):
        pipeline_run = self.adf_client.pipeline_runs.get(self.rg_name, self.df_name, create_pipeline_run.run_id)
        while pipeline_run.status in ["Queued", "InProgress", "Canceling"]:
            pipeline_run = self.adf_client.pipeline_runs.get(self.rg_name, self.df_name, pipeline_run.run_id)
            time.sleep(5)
        return pipeline_run.status

    def _get_pipeline_default_parameters(self):
        pipeline = self.adf_client.pipelines.get(self.rg_name, self.df_name, self.pipeline_name)
        parameters = {parameter_name: parameter_value.default_value for (parameter_name, parameter_value) in
                      pipeline.parameters.items()}
        return parameters

    def _run_pipeline(self, test_parameters):
        if test_parameters:
            default_pipeline_parameters = self._get_pipeline_default_parameters()
            test_parameters = self._overwrite_default_parameters(default_pipeline_parameters, test_parameters)
        pipeline_run = self._trigger_pipeline(test_parameters)
        final_state = self._get_final_pipeline_state(pipeline_run)
        return final_state, pipeline_run.run_id

    def get_pipeline_activity_run_details(self, pipeline_run_id):
        filter_params = RunFilterParameters(last_updated_after=datetime.now() - timedelta(5),
                                            last_updated_before=datetime.now() + timedelta(5))
        query_response = self.adf_client.activity_runs.query_by_pipeline_run(self.rg_name, self.df_name,
                                                                             pipeline_run_id, filter_params)

        return query_response.value

    def run_pipeline(self, parameters={}):
        '''
        Run pipeline

        Args:
            settings: settings
            parameters: ADF parameters (optional)

        Returns: final pipeline state

        '''
        final_state, run_id = self._run_pipeline(parameters)
        return final_state, run_id
