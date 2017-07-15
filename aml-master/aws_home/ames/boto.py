import boto3

# init client
s3 = boto3.resource('s3')

# List all the buckets in our acount
for bucket in s3.buckets.all():
	print bucket.name

# load the file
data = open('data/ames_housing_nohead.csv', 'rb')
s3.Object('adarshames', 'data/ames_housing_nohead.csv').put(Body=data)

schema = open('data/ames_housing.csv.schema', 'rb')
s3.Object('adarshames', 'data/ames_housing.csv.schema').put(Body=schema)

recipe = open('data/recipe_ames_housing_001.json', 'rb')
s3.Object('adarshames', 'data/recipe_ames_housing_001.json').put(Body=recipe)

data_shuffled = open('data/ames_housing_shuffled.csv', 'rb')
s3.Object('adarshames', 'data/ames_housing_shuffled.csv').put(Body=data_shuffled)