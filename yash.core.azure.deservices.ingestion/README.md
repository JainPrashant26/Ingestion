NOTE - For testing purpose , initially , we have used default parameters .

Some modifications done are mentioned as below.

1.) We have used ClientSecretCredential() instead of DefaultAzureCredential() in adf_client.py file.

For using ClientSecretCredential() , we need ${CLIENT_ID} , ${CLIENT_SECRET} , ${TENANT_ID} .
For these parameters , kindly register an app and assign contributor role in rg/subs .

2.) Since we are using default parameters for testing , we are using only adf client fixture in conftest.py.

Variables used -

{CLIENT_ID} - CLIENT_ID of App
{CLIENT_SECRET} - CLIENT_SECRET of App
{TENANT_ID} - TENANT_ID of App
{SUBSCRIPTION_ID} - SUBSCRIPTION_ID
{RG_NAME} - RESOURCE_GROUP_NAME
{DF_NAME} - DATA_FACTORY_NAME
{PIPELINE_NAME} - DATA_FACTORY_PIPELINE_NAME
