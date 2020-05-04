#!/usr/bin/python
import psycopg2
from config import config
from postgreshandler import *

if __name__ == '__main__':
    postgres = postgressql()
    postgres.create_tables()
    # postgres.insert_vendor_list([
    #     ('AKM Semiconductor Inc.',),
    #     ('Asahi Glass Co Ltd.',),
    #     ('Daikin Industries Ltd.',),
    #     ('Dynacast International Inc.',),
    #     ('Foster Electric Co. Ltd.',),
    #     ('Murata Manufacturing Co. Ltd.',)
    # ])
    # postgres.update_vendor('1', "3M Corp")
    # postgres.add_part('SIM Tray', (1, 2))
    # postgres.add_part('Speaker', (3, 4))
    # postgres.add_part('Vibrator', (5, 6))
    # postgres.add_part('Antenna', (6, 7))
    # postgres.add_part('Home Button', (1, 5))
    # postgres.add_part('LTE Modem', (1, 5))
    # postgres.get_vendors()
    # postgres.get_parts()
    # postgres.get_part_vendors()
    # deleted_rows = postgres.delete_part('1')
    # print('The number of deleted rows: ', deleted_rows)