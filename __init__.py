from kafka.admin import KafkaAdminClient, NewTopic
import config


def kafka_setup(broker: str, client_id: str):
    """
    Creates all topics. There's no idempotency so be careful. Basic settings for topics
    :param broker:
    :param client_id:
    :return:
    """
    admin_client = KafkaAdminClient(
        bootstrap_servers=broker,
        client_id=client_id
    )
    topic_list = [NewTopic(name=config.raw_topic, num_partitions=1, replication_factor=1),
                  NewTopic(name=config.clean_data_topic, num_partitions=1, replication_factor=1),
                  NewTopic(name=config.transform_data_topic, num_partitions=1, replication_factor=1),
                  NewTopic(name=config.reporting_topic, num_partitions=1, replication_factor=1),
                  NewTopic(name=config.ml_pipeline_topic, num_partitions=1, replication_factor=1),
                  NewTopic(name=config.events_topic, num_partitions=1, replication_factor=1),
                  NewTopic(name=config.dead_queue_topic, num_partitions=1, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)


if __name__ == '__main__':
    kafka_setup(config.bootstrap_server, 'zenpli')
