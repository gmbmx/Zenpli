from uuid import uuid4
import config
from protobuf import raw_data_pb2
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
import pandas as pd

schema_registry = config.schema_registry
bootstrap_server = config.bootstrap_server
topic = config.raw_topic
input_file = config.input_file


def main():
    schema_registry_conf = {'url': schema_registry}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    protobuf_serializer = ProtobufSerializer(raw_data_pb2.rawdata,
                                             schema_registry_client,
                                             {'use.deprecated.format': True})

    producer_conf = {'bootstrap.servers': bootstrap_server,
                     'key.serializer': StringSerializer('utf_8'),
                     'value.serializer': protobuf_serializer}

    producer = SerializingProducer(producer_conf)
    print("Producing user records to topic {}.".format(topic))

    data = pd.read_csv(input_file, dtype=str)
    data_dict = data.to_dict('records')

    for row in data_dict:
        protobuf_message = raw_data_pb2.rawdata(key_1=row['key_1'],
                                                date_2=row['date_2'],
                                                cont_3=row['cont_3'],
                                                cont_4=row['cont_4'],
                                                disc_5=row['disc_5'],
                                                disc_6=row['disc_6'],
                                                cat_7=row['cat_7'],
                                                cat_8=row['cat_8'],
                                                cont_9=row['cont_9'],
                                                cont_10=row['cont_10'])
        #print(protobuf_message)
        producer.produce(topic=topic, key=str(uuid4()), value=protobuf_message)
        producer.flush()


if __name__ == '__main__':
    main()
