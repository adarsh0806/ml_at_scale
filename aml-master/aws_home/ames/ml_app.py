import boto3
import time
import json


def name_id_generation(prefix, mode, trial):
    '''
    This function sets the names and Ids of the different objects
    Input: prefix, mode and trial are all string to differentiate between runs
    Output: a dictionary with the name and ID of the object
    '''
    Id      = '_'.join([prefix, mode, "%02d"%int(trial)])
    name    = "[%s] %s %02d"% (prefix, mode, int(trial)  )
    return {'Name':name, 'Id':Id}

# Define the service you want to interact with
client = boto3.client('machinelearning')

# ---------------------------------------------------------------------------
#  Initialization
# ---------------------------------------------------------------------------

# Location of schemas and files, adapt to your own account and bucket names
data_s3     = 's3://adarshames/data/ames_housing_shuffled.csv'
schema_s3   = 's3://adarshames/data/ames_housing.csv.schema'
recipe_s3   = 's3://adarshames/data/recipe_ames_housing_001.json'

# Define the algorithm parameters: regularization and number of passes
sgd_params = {
    "sgd.shuffleType": "auto",
    "sgd.l1RegularizationAmount": "1.0E-04",
    "sgd.maxPasses": "100"
}

# Set the number of the current trial
trial = 1

# ---------------------------------------------------------------------------
#  Create datasource for training
# ---------------------------------------------------------------------------
resource = name_id_generation('DS3', 'training', trial)
print("Creating datasources for training (%s)"% resource['Name'] )
response = client.create_data_source_from_s3(
    DataSourceId    = resource['Id'] ,
    DataSourceName  = resource['Name'],
    DataSpec = {
        'DataLocationS3'        : data_s3,
        'DataSchemaLocationS3'  : schema_s3,
        'DataRearrangement':'{\"splitting\":{\"percentBegin\":0,\"percentEnd\":70}}'
    },
    ComputeStatistics = True
)

# ---------------------------------------------------------------------------
#  Create datasource for validation
# ---------------------------------------------------------------------------
resource = name_id_generation('DS3', 'validation', trial)
print("Creating datasources for validation (%s)"% resource['Name'] )
response = client.create_data_source_from_s3(
    DataSourceId    = resource['Id'] ,
    DataSourceName  = resource['Name'],
    DataSpec = {
        'DataLocationS3': data_s3,
        'DataSchemaLocationS3': schema_s3,
        'DataRearrangement':'{\"splitting\":{\"percentBegin\":70,\"percentEnd\":100}}'
    },
    ComputeStatistics = True
)
# ---------------------------------------------------------------------------
#  Train model with existing recipe
# ---------------------------------------------------------------------------
# resource = name_id_generation('MDL2', '', trial)
# print("Training model (%s) with params:\n%s"% (resource['Name'], json.dumps(sgd_params, indent=4)) )
# response = client.create_ml_model(
#     MLModelId   = resource['Id'],
#     MLModelName = resource['Name'],
#     MLModelType = 'REGRESSION',
#     Parameters  = sgd_params,
#     TrainingDataSourceId= name_id_generation('DS3', 'training', trial)['Id'],
#     RecipeUri   = recipe_s3
# )

# ---------------------------------------------------------------------------
#  Create evaluation
# ---------------------------------------------------------------------------
# resource = name_id_generation('EVAL', '', trial)
# print("Launching evaluation (%s) "% resource['Name'] )
# response = client.create_evaluation(
#     EvaluationId    = resource['Id'],
#     EvaluationName  = resource['Name'],
#     MLModelId       = name_id_generation('MDL2', '', trial)['Id'],
#     EvaluationDataSourceId = name_id_generation('DS3', 'validation', trial)['Id']
# )

