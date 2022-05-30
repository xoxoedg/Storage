import os
from typing import Union, Optional
import socket
import numpy as np
import time
import pyModbusTCP.client as pmc
from pyModbusTCP.client import ModbusClient
import struct

from app.exception.network_error import NetworkError


class ModbusTCPInterface:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = ModbusClient(self.ip, self.port)

    def is_open(self):
        return self.client.is_open()

    def connect(self):
        if self.client.open():
            return True
        else:
            raise NetworkError("Could not open a Connection to the Grid Analyzer Client")

    def register_converter(self, content, data_format, data_type):
        return self.convert_register_content(content, data_format, data_type)

    def get_data(self, register, width, data_format, data_type):
        if self.is_open():
            register_content = self.client.read_holding_registers(register, width)
            return self.register_converter(register_content, data_format, data_type) if register_content else print("Register Content is empty")
        return "You have to connect to client first"

    def get_success_perc(self, time_list, iterations, register, width, data_format, data_type):
        percs = dict()

        for tm in time_list:

            results = list()

            for i in range(iterations):
                results.append(self.get_data(register, width, data_format, data_type))
                time.sleep(tm)

            perc = results.count(None) / len(results)
            err = results.count('ValueError') / len(results)

            percs[tm] = (perc, err)

        return percs

    def convert_register_content(self, register_content, data_format, data_type):

        out_val = None

        if data_format.lower() == 'raw':
            out_val = register_content
        else:
            hexValue = str(hex(register_content[1]))[2:] + str(hex(register_content[0]))[2:]
            out_val = struct.unpack('!f', bytes.fromhex(hexValue))[0]

        return out_val

if __name__ == '__main__':
    connection = ModbusTCPInterface("172.25.224.74", 502)
    print(connection.is_open())
    connection.connect()
    print(connection.is_open())

    register = 1010
    width = 2
    data_format = 'raw'  # 'BE'
    data_type = 'int'
    print(connection.get_data(register, width, data_format, data_type))

time_recorder = list()
    #interfacer = ModbusTCPInterface()
def_params = dict(register = 1010,
                  width = 2,
                  data_format = 'BE',
                  data_type = 'int')

for i in range(100):

     t = time.process_time()
     val = connection.get_data(**def_params) #wie mache ich hier call get data(parameter)?
     print(val)
     t1 = time.process_time() - t
     time_recorder.append(t1)


     print(val)

print('Average time: {:.6f}'.format(np.average(time_recorder)))
print('Maximum time: {:.6f}'.format(max(time_recorder)))
print('Minimum time: {:.6f}'.format(min(time_recorder)))

perc_dict = connection.get_success_perc([0.1, 0.5, 0.7, 0.9], 100, **def_params)
#
# for k, v in perc_dict.items():
#     print('{} s:  {:.4f} % no value,    {:.4f} % conversion errors'.format(k, v[0] * 100, v[1] * 100))
#
# import pandas as pd
# perc_df = pd.DataFrame({'time_s': perc_dict.keys(),
#                         'no_response': [v[0] for v in perc_dict.values()],
#                         'conversion_error': [v[1] for v in perc_dict.values()]})
#
# print(perc_df)
# perc_df.to_csv(sep=';', decimal=',', encoding='cp1252')
