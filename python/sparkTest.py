"""SimpleApp.py"""
from pyspark import SparkContext

#logFile = "~/neuronforest-analysis-script/main.py"  # Should be some file on your system
sc = SparkContext("local[2]", "Simple App")
#logData = sc.textFile(logFile).cache()

#numAs = logData.filter(lambda s: 'a' in s).count()
#numBs = logData.filter(lambda s: 'b' in s).count()
print "Working pyspark"
#print "Lines with a: %i, lines with b: %i" % (numAs, numBs)