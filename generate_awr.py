__author__ = 'rakesh.varma'

import threading, time, os, sys
from functools import wraps
from configfactory import ConfigFactory
from oraclefactory import *
from kafka import SimpleProducer, KafkaClient, KeyedProducer

config = ConfigFactory()
oracleFactory = OracleFactory(config = config)
kafka = KafkaClient(config.kafkaconnection)
producer = KeyedProducer(kafka)

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print ("@timefn:" + fn.func_name + " took " + str(t2 - t1) + " seconds")
        return result
    return measure_time



def save_awr(snap):
    results = oracleFactory.save_awr(snap)
    key = "AWR_{0}_{1}_{2}".format(config.database,snap['snap_id'], snap['snap_end_time'])
    for result in results:
        result = str(result)
        producer.send_messages(config.kafkatopic, key, result)

@timefn
def main():
    snapshots = oracleFactory.get_snapshots()
    threads = []
    for snapshot in snapshots:
        t = threading.Thread(target = save_awr, args=(snapshot,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
