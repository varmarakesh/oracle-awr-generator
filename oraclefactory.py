__author__ = 'rakesh.varma'
import cx_Oracle
import sys, os
import time, platform

class OracleFactory:
    config = None
    pool = None

    def __init__(self, config):
        self.config = config
        self.pool = cx_Oracle.SessionPool(config.username, config.password, config.database, 1, int(config.poolsize),1, threaded = True)

    def getOracleConnection(self):
        if self.pool.opened == self.config.poolsize:
            print 'Max pool size reached...waiting for 10 seconds and trying.'
            time.sleep(10)
            self.getOracleConnection()
        connection = self.pool.acquire()
        return connection

    def getDirectoryPath(self):
        if platform.system() == 'Darwin':
            return os.getcwd() + '/'
        else:
            conn = self.getOracleConnection()
            q_dir = '''SELECT DIRECTORY_PATH FROM DBA_DIRECTORIES WHERE DIRECTORY_NAME = :DIRECTORY_NAME'''
            cursor = conn.cursor()
            cursor.execute(q_dir, [self.config.directory])
            dir = cursor.fetchone()
            if dir is None:
                print 'Directory Object {0} does not exist in {1}'.format(self.config.directory, sys.argv[1])
                print 'Exiting......'
                exit()
            conn.close()
            return dir[0] + '/'

    def get_snapshots(self):
        snapshots = []
        conn = self.getOracleConnection()
        q_awr_snap = ''' SELECT distinct SNAP_ID, to_char(END_INTERVAL_TIME, 'hh24mi_dd_mon_yy') FROM DBA_HIST_SNAPSHOT WHERE TRUNC(END_INTERVAL_TIME) = TRUNC(SYSDATE) ORDER BY SNAP_ID'''
        cursor = conn.cursor()
        cursor.execute(q_awr_snap)
        for c in cursor:
            snapshots.append({'snap_id' : c[0], 'snap_end_time' : c[1]})
        cursor.close()
        self.pool.drop(conn)
        return snapshots

    def save_awr(self, snap):
        q_awr = ''' SELECT
                     D.NAME,
                     SS.SNAP_ID,
                     SS.INSTANCE_NUMBER,
                     SS.SQL_ID,
                     ST.SQL_TEXT,
                     SH.MACHINE,
                     SS.MODULE,
                     SS.ACTION,
                     SS.PARSING_SCHEMA_NAME,
                     SS.FETCHES_TOTAL,
                     SS.SORTS_TOTAL,
                     SS.EXECUTIONS_TOTAL,
                     SS.LOADS_TOTAL,
                     SS.PARSE_CALLS_TOTAL,
                     SS.DISK_READS_TOTAL,
                     SS.BUFFER_GETS_TOTAL,
                     SS.ROWS_PROCESSED_TOTAL,
                     SS.CPU_TIME_TOTAL,
                     SS.IOWAIT_TOTAL,
                     SS.ELAPSED_TIME_TOTAL
                    FROM
                     DBA_HIST_SQLSTAT SS,
                     DBA_HIST_SNAPSHOT SP,
                     DBA_HIST_SQLTEXT ST,
                     DBA_HIST_ACTIVE_SESS_HISTORY SH,
                     V$DATABASE D
                    WHERE
                     SS.SNAP_ID = SP.SNAP_ID AND
                     SS.DBID = SP.DBID AND
                     SS.DBID = D.DBID AND
                     SS.INSTANCE_NUMBER = SP.INSTANCE_NUMBER AND
                     SS.DBID = ST.DBID AND
                     SS.SQL_ID = ST.SQL_ID AND
                     SS.SNAP_ID = SH.SNAP_ID AND
                     SS.DBID = SH.DBID AND
                     SS.INSTANCE_NUMBER = SH.INSTANCE_NUMBER AND
                     SS.SQL_ID = SH.SQL_ID AND
                     SS.SNAP_ID = :SNAP_ID'''


        conn = self.getOracleConnection()
        cursor = conn.cursor()
        cursor.execute(q_awr, [snap['snap_id']])
        results = cursor.fetchall()
        cursor.close()
        self.pool.drop(conn)
        return results
