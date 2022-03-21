# Configuration settings for Zenpli Challenge. Can be ported to a YAML in the future
# If config variables are modified, streaming engine must be stopped in order for changes to apply
# This config settings should not be implemented in production

# Variables for Red panda broker access
schema_registry = 'http://localhost:8081'
bootstrap_server = 'localhost:9092'

# Location of data is kept in local in order to protect data privacy
input_file = 'C:/Users/Willy/Documents/Zophia/zenpli/backend-dev-data-dataset.txt'

# Variables related to topic, producers and consumers
raw_topic = 'raw-data'
events_topic = 'events'
clean_data_topic = 'clean-data'
transform_data_topic = 'transform-data'
reporting_topic = 'aggregation-metrics'
ml_pipeline_topic = 'ml-metrics'
dead_queue_topic = 'dead-queue'

# Variables for transformation and aggregation control
normalize_column = 'cont_3'
filter_column = 'cat_8'
filter_column_value = 'scared'
group_column = 'date_2'
