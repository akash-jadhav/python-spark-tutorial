import sys
sys.path.insert(0, '.')
from pyspark import SparkContext, SparkConf
import re

def splitComma(line):
    COMMA_DELIMITER = re.compile(''',(?=(?:[^"]*"[^"]*")*[^"]*$)''')
    splits = COMMA_DELIMITER.split(line)
    return "{}, {}".format(splits[1], splits[2])

if __name__ == "__main__":
    conf = SparkConf().setAppName("airports").setMaster("local[*]")
    sc = SparkContext(conf = conf)

    airports = sc.textFile("in/airports.text")
    COMMA_DELIMITER = re.compile(''',(?=(?:[^"]*"[^"]*")*[^"]*$)''')
    airportsInUSA = airports.filter(lambda line : COMMA_DELIMITER.split(line)[3] == "\"United States\"")

    airportsNameAndCityNames = airportsInUSA.map(splitComma)
    airportsNameAndCityNames.saveAsTextFile("out/airports_in_usa.text")