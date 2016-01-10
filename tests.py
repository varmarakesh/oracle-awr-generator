__author__ = 'rakesh.varma'
import unittest
import cx_Oracle
import time
from configfactory import *
from oraclefactory import *
from kafka import KafkaClient

class tests(unittest.TestCase):

    def setUp(self):
        self.user = 'system'
        self.password = 'manager'

    def test_oracle_pool(self):
        pool = cx_Oracle.SessionPool(self.user, self.password, 'DLINK_SAC', 1,5,1, threaded = True)
        conn1 = pool.acquire()
        conn2 = pool.acquire()
        self.assertEqual(pool.opened,2)
        pool.drop(conn1)
        self.assertEqual(pool.opened,1)
        conn1.close()
        conn2.close()

    def test_oracle_pool_limit(self):
        pool = cx_Oracle.SessionPool(self.user, self.password, 'DLINK_SAC', 1,3,1, threaded = True)
        conn1 = pool.acquire()
        conn2 = pool.acquire()
        conn3 = pool.acquire()
        conn4 = pool.acquire()
        self.assertEqual(pool.opened,2)
        pool.drop(conn1)
        self.assertEqual(pool.opened,1)
        conn1.close()
        conn2.close()
        conn3.close()
        conn4.close()

    def test_config(self):
        config = ConfigFactory()
        self.assertEqual(config.username.upper(), 'SYSTEM')

    def test_snapshots(self):
        config = ConfigFactory()
        oracleFactory = OracleFactory(config)
        snapshots = oracleFactory.get_snapshots()
        self.assertGreaterEqual(len(snapshots),1)

    def test_kafka_topic_exists(self):
        config = ConfigFactory()
        client = KafkaClient(config.kafkaconnection)
        self.assertTrue(config.kafkatopic in client.topics)

