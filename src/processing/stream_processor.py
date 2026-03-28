from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import from_json, col, when

class SparkStreamProcessor:
    def __init__(self, kafka_bootstrap_servers: str = 'localhost:9092', topic: str = 'loan-performance'):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.topic = topic
        
        # Initialize Spark Session with Kafka integration package
        #self.spark = SparkSession.builder.appName("CreditRiskStreamProcessor").config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1").getOrCreate()
        self.spark = SparkSession.builder.appName("CreditRiskStreamProcessor").master("local[*]").config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1").getOrCreate()
            
        # Suppress overly verbose Spark logs
        self.spark.sparkContext.setLogLevel("WARN")

        # Define the schema matching our generator's output
        self.schema = StructType([
            StructField("LoanId", StringType(), True),
            StructField("PerformanceMonth", StringType(), True),
            StructField("MonthOnBooks", IntegerType(), True),
            StructField("PrincipalBalance", DoubleType(), True),
            StructField("EndingBalance", DoubleType(), True),
            StructField("DelinquentDays", IntegerType(), True),
            StructField("DelinquentFlag", IntegerType(), True),
            StructField("PrepayFlag", IntegerType(), True)
        ])

    def process_stream(self):
        """Reads from Kafka, parses JSON, engineers features, and outputs to console."""
        print(f"Connecting PySpark to Kafka topic: {self.topic}...")
        
        # 1. Read the stream from Kafka
        raw_stream_df = self.spark.readStream.format("kafka").option("kafka.bootstrap.servers", self.kafka_bootstrap_servers).option("subscribe", self.topic) \
                        .option("startingOffsets", "latest").load()

        # 2. Parse the JSON 'value' column into individual columns
        parsed_df = raw_stream_df.select(from_json(col("value").cast("string"), self.schema).alias("data")).select("data.*")

        # 3. Feature Engineering on the fly
        # Example: Calculate a real-time 'RiskIndicator' based on balance and delinquency

        enriched_df = parsed_df.withColumn("RiskIndicator",when(col("DelinquentDays") > 30, "HIGH RISK").when(col("DelinquentDays") > 0, "MEDIUM RISK")
                      .otherwise("LOW RISK")).withColumn("LiveRiskScore",(col("DelinquentDays") * 1.5) + (col("PrincipalBalance") * 0.0001))

        # 4. Write the processed stream to the console (for local testing/portfolio display)
        print("Starting stream processing. Waiting for data...")

        query = enriched_df.writeStream.outputMode("append").format("console").option("truncate", "false").start()
        query.awaitTermination()