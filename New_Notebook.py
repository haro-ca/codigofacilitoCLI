# Databricks notebook source
# MAGIC %md
# MAGIC # PySpark Tutorial
# MAGIC
# MAGIC This notebook covers the fundamentals of PySpark for data processing and analysis.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Introduction to Spark Session
# MAGIC
# MAGIC The SparkSession is the entry point to programming with Spark. In Databricks, it's automatically created as `spark`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Creating DataFrames
# MAGIC
# MAGIC DataFrames are distributed collections of data organized into named columns.

# COMMAND ----------

# Create a DataFrame from a list
data = [
    ("Alice", 34, "Engineering"),
    ("Bob", 45, "Sales"),
    ("Charlie", 28, "Engineering"),
    ("Diana", 32, "Marketing"),
    ("Eve", 29, "Sales")
]

columns = ["name", "age", "department"]
df = spark.createDataFrame(data, columns)

# Display the DataFrame
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Basic DataFrame Operations

# COMMAND ----------

# Show schema
df.printSchema()

# COMMAND ----------

# Select specific columns
df.select("name", "age").show()

# COMMAND ----------

# Filter rows
df.filter(df.age > 30).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. DataFrame Transformations

# COMMAND ----------

from pyspark.sql.functions import col, upper, lower

# Add a new column
df_with_uppercase = df.withColumn("name_upper", upper(col("name")))
display(df_with_uppercase)

# COMMAND ----------

# Rename columns
df_renamed = df.withColumnRenamed("age", "employee_age")
display(df_renamed)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Aggregations and Grouping

# COMMAND ----------

from pyspark.sql.functions import avg, count, max, min

# Group by department and calculate statistics
dept_stats = df.groupBy("department").agg(
    count("name").alias("employee_count"),
    avg("age").alias("avg_age"),
    min("age").alias("min_age"),
    max("age").alias("max_age")
)

display(dept_stats)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Sorting Data

# COMMAND ----------

# Sort by age (descending)
df.orderBy(col("age").desc()).show()

# COMMAND ----------

# Sort by multiple columns
df.orderBy("department", col("age").desc()).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Working with SQL

# COMMAND ----------

# Register DataFrame as a temporary view
df.createOrReplaceTempView("employees")

# Query using SQL
result = spark.sql("""
    SELECT department, COUNT(*) as count, AVG(age) as avg_age
    FROM employees
    GROUP BY department
    ORDER BY count DESC
""")

display(result)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Working with Larger Datasets

# COMMAND ----------

# Create a larger sample dataset
from pyspark.sql.functions import rand, randn

large_df = spark.range(0, 10000).select(
    col("id"),
    (rand() * 100).cast("int").alias("score"),
    (randn() * 50 + 100).cast("int").alias("value")
)

display(large_df.limit(10))

# COMMAND ----------

# Calculate summary statistics
large_df.describe().show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Window Functions

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank

# Create window specification
windowSpec = Window.partitionBy("department").orderBy(col("age").desc())

# Apply window functions
df_with_rank = df.withColumn("rank", rank().over(windowSpec))
display(df_with_rank)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Handling Null Values

# COMMAND ----------

# Create DataFrame with null values
data_with_nulls = [
    ("Alice", 34, "Engineering"),
    ("Bob", None, "Sales"),
    ("Charlie", 28, None),
    (None, 32, "Marketing")
]

df_nulls = spark.createDataFrame(data_with_nulls, ["name", "age", "department"])
display(df_nulls)

# COMMAND ----------

# Drop rows with any null values
df_nulls.dropna().show()

# COMMAND ----------

# Fill null values
df_nulls.fillna({"age": 0, "department": "Unknown", "name": "Anonymous"}).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11. Joins

# COMMAND ----------

# Create another DataFrame for joining
salaries = [
    ("Alice", 95000),
    ("Bob", 87000),
    ("Charlie", 78000),
    ("Diana", 82000)
]

df_salaries = spark.createDataFrame(salaries, ["name", "salary"])

# Inner join
df_joined = df.join(df_salaries, on="name", how="inner")
display(df_joined)

# COMMAND ----------

# Left join
df_left_join = df.join(df_salaries, on="name", how="left")
display(df_left_join)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12. User-Defined Functions (UDFs)

# COMMAND ----------

from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Define a UDF
def categorize_age(age):
    if age < 30:
        return "Young"
    elif age < 40:
        return "Middle"
    else:
        return "Senior"

# Register UDF
age_category_udf = udf(categorize_age, StringType())

# Apply UDF
df_with_category = df.withColumn("age_category", age_category_udf(col("age")))
display(df_with_category)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 13. Reading and Writing Data

# COMMAND ----------

# Write DataFrame to Parquet (example - commented out)
# df.write.mode("overwrite").parquet("/tmp/employees.parquet")

# Read from Parquet (example - commented out)
# df_read = spark.read.parquet("/tmp/employees.parquet")
# display(df_read)

# COMMAND ----------

# Write to Delta format (recommended for Databricks)
# df.write.format("delta").mode("overwrite").save("/tmp/delta/employees")

# Read from Delta
# df_delta = spark.read.format("delta").load("/tmp/delta/employees")
# display(df_delta)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 14. Performance Optimization Tips

# COMMAND ----------

# Cache DataFrame for repeated operations
df_cached = df.cache()
df_cached.count()  # Trigger caching

# COMMAND ----------

# Check execution plan
df.filter(col("age") > 30).explain()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 15. Practice Exercises
# MAGIC
# MAGIC Try these exercises:
# MAGIC 1. Create a DataFrame with 5 different products and their prices
# MAGIC 2. Filter products with price > 50
# MAGIC 3. Add a column with 10% discount applied
# MAGIC 4. Group by category and find average price
# MAGIC 5. Sort results by average price descending

# COMMAND ----------

# Your practice code here
# Exercise solution space

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC You've learned:
# MAGIC - Creating and manipulating DataFrames
# MAGIC - Filtering, selecting, and transforming data
# MAGIC - Aggregations and grouping
# MAGIC - SQL queries in Spark
# MAGIC - Window functions
# MAGIC - Handling null values
# MAGIC - Joins
# MAGIC - User-defined functions
# MAGIC - Reading and writing data
# MAGIC - Performance optimization
# MAGIC
# MAGIC **Next Steps:**
# MAGIC - Explore Delta Lake for ACID transactions
# MAGIC - Learn about Spark MLlib for machine learning
# MAGIC - Study Spark Streaming for real-time data processing