"""
To run:

Define the location of Spark:
export SPARK_HOME=/Users/adarshnair/spark-2.0.1-bin-hadoop2.7

Execute the  following:
$SPARK_HOME/bin/spark-submit /Users/adarshnair/Desktop/Machine_Learning_at_scale/Spark/Spark_Projects/python-spark-app/pythonapp.py
"""


from pyspark import SparkContext

# Create SparkContext variable
sc = SparkContext("local[2]", "First Spark App")

# Data location
data_path = "/Users/adarshnair/Desktop/Machine_Learning_at_scale/Spark/Spark_Projects/python-spark-app/data/UserPurchaseHistory.csv"

# Convert CSV to the form (User, Product, Price)
data = sc.textFile(data_path) \
         .map(lambda line: line.split(",")) \
         .map(lambda record: (record[0], record[1], record[2]))

# Preview data
# print "\n*** Data preview: ", data.take(5)

# Count the number of purchases(rows)
numPurchases = data.count()

# Count unique users made purchases
uniqueUsers = data.map(lambda record: record[0]) \
                  .distinct() \
                  .count()

# Sum up our total revenue
totalRevenue = data.map(lambda record: float(record[2])) \
                   .sum()

# Find  most popular product
products = data.map(lambda record: (record[1], 1.0)) \
               .reduceByKey(lambda a, b: a + b) \
               .collect()
    
mostPopular = sorted(products, 
                     key = lambda x: x[1], 
                     reverse = True)[0]

# Finally, print everything out
print "\n*** Total purchases: %d" % numPurchases
print "\n*** Unique users: %d" % uniqueUsers
print "\n*** Total revenue: %2.2f" % totalRevenue
print "\n*** Most popular product: %s with %d purchases" % (mostPopular[0], mostPopular[1])

# stop the SparkContext
sc.stop()
