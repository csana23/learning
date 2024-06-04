import pyspark

conf = pyspark.SparkConf().setAppName('MyApp').setMaster('spark://host.docker.internal:7077')
sc = pyspark.SparkContext(conf=conf)
