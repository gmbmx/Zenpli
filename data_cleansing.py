from confluent_kafka.serialization import StringSerializer, StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from confluent_kafka import SerializingProducer, DeserializingConsumer
from uuid import uuid4
from protobuf import data_pb2, raw_data_pb2
import config
import utils
import cat_enum


def clean_missing(message):
    """
    Pipeline for cleaning missing values
    :param message: Protobuf message with raw data
    :return: Cleansed Data in protobuf message with raw data format
    """
    message.disc_6 = utils.clean_numeric_missing_values(message.disc_6, cat_enum.Missing)
    message.cont_10 = utils.clean_numeric_missing_values(message.cont_10, cat_enum.Missing)
    return message


def validate_schema(message) -> bool:
    """
    Pipeline for validating Schema
    :param message: Protobuf message with raw data
    :return: True or False if all validations are ok
    """
    validation = [utils.validate_date(message.date_2),
                  utils.validate_float(message.cont_3),
                  utils.validate_float(message.cont_4),
                  utils.validate_discrete(message.disc_5),
                  utils.validate_float(message.disc_6),
                  utils.validate_float(message.cont_9),
                  utils.validate_float(message.cont_10)]
    print(validation)
    if all(validation):
        return True
    else:
        return False


def apply_schema(message):
    """
    Assigns schema to protobuf message. Used together with schema validation
    :param message: Protobuf message with raw data
    :return: Protobuf message with data format
    """
    data = data_pb2.data(key_1=message.key_1,
                         date_2=message.date_2,
                         cont_3=float(message.cont_3),
                         cont_4=float(message.cont_4),
                         disc_5=int(str(message.disc_5)),
                         disc_6=float(message.disc_6),
                         cat_7=message.cat_7,
                         cat_8=message.cat_8,
                         cont_9=float(message.cont_9),
                         cont_10=float(message.cont_10))
    return data


def find_anomalies(message):
    """
    Pipeline for anomaly detection
    :param message: Message in protobuf data format. Data already has schema and is clean.
    :return: True if no anomalies are found, otherwise False
    """
    anomalies = [utils.range_anomalies(message.cont_3, 215, 2300),
                 utils.range_anomalies(message.cont_4, -90, 160),
                 utils.range_anomalies(message.disc_5, 0, 7),
                 utils.range_anomalies(message.disc_6, 0, 17),
                 utils.categorical_value_anomalies(message.cat_7, cat_enum.ValuesCat7),
                 utils.categorical_value_anomalies(message.cat_8, cat_enum.ValuesCat8),
                 utils.range_anomalies(message.cont_9, -1.5, 2.6)]
    if all(anomalies):
        return True
    else:
        return False


def main():
    schema_registry = config.schema_registry
    consumer_topic = config.raw_topic
    dead_queue_topic = config.dead_queue_topic
    success_topic = config.clean_data_topic
    group = 'data_clean_group'
    protobuf_deserializer = ProtobufDeserializer(raw_data_pb2.rawdata,
                                                 {'use.deprecated.format': True})
    string_deserializer = StringDeserializer('utf_8')

    consumer_conf = {'bootstrap.servers': config.bootstrap_server,
                     'key.deserializer': string_deserializer,
                     'value.deserializer': protobuf_deserializer,
                     'group.id': group,
                     'auto.offset.reset': "earliest"}

    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe([consumer_topic])

    schema_registry_conf = {'url': schema_registry}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    # Producer config for sending clean, standardized data to clean-data topic in protobuf
    protobuf_serializer = ProtobufSerializer(data_pb2.data,
                                             schema_registry_client,
                                             {'use.deprecated.format': True})

    producer_conf = {'bootstrap.servers': config.bootstrap_server,
                     'key.serializer': StringSerializer('utf_8'),
                     'value.serializer': protobuf_serializer}

    producer = SerializingProducer(producer_conf)

    # Start consuming messages and apply: clean missing -> validate schema -> find anomalies
    while True:
        try:
            message = consumer.poll(1.0)
            if message is None:
                print("Waiting...")
            elif message.error():
                print("ERROR: %s".format(message.error()))
            else:
                data = message.value()
                clean_data = clean_missing(data)
                validation = validate_schema(clean_data)
                if validation is False:
                    print(f"Schema Validation Failed: {clean_data}")
                    # producer.produce(topic=dead_queue_topic, value=data)
                else:
                    std_data = apply_schema(clean_data)
                    anomalies = find_anomalies(std_data)
                    if anomalies is False:
                        print(f"Anomalies found: {clean_data}")
                    # producer.produce(topic=dead_queue_topic, value=data)
                    # If no anomalies found and schema is ok send data to clean-data topic for future processing
                    if validation is True and anomalies is True:
                        producer.produce(topic=success_topic, key=str(uuid4()), value=std_data)
                        producer.flush()
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    main()
