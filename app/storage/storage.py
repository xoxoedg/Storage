from pyModbusTCP.client import ModbusClient

from app.exception.network_error import NetworkError
from app.exception.no_data_error import NoDataError
from utils.converter import PowerConverter


class Storage:

    def __init__(self, IP, grid_locations, name):
        self.name = name
        self.grid_locations = grid_locations
        self.IP = IP
        self.client = ModbusClient(host=IP, port=502)
        self.power_change_limit = 250

    def is_open(self):
        return self.client.is_open()

    def initialize_client(self):
        if self.client.open():
            return True
        else:
            raise NetworkError("Could not open a Connection to the Storage Client")

    def get_data_single_register(self, register):
        register_value = self.client.read_input_registers(register, 1)
        if register is not None:
            return register_value[0]
        else:
            raise NoDataError("No Data in Storage")

    def get_data_multiple_register(self, register):
        register_value = self.client.read_input_registers(register, 2)
        if register_value[0] > 32767:
            register_value[0] -= (2 * 32768)
            int_val = (register_value[0] * 65536 + register_value[1]) / 1000
            return int_val
        return register_value[0]

    def send_power(self, power, register):
        power_in_mw = PowerConverter.convert_to_mw(power)
        current_power_in_mw = PowerConverter.convert_to_mw(self.get_data_multiple_register(register))
        if abs(current_power_in_mw - power_in_mw) > PowerConverter.convert_to_mw(self.power_change_limit):
            power = current_power_in_mw + 100 * power_in_mw / abs(power_in_mw)
        if power < 0:
            power_in_mw += 4294967296
        return power_in_mw

    def write_data_to_storage(self, power, register, should_send_to_storage):
        power_to_send = self.send_power(power, register)
        if should_send_to_storage:
            self.client.write_multiple_registers(2000, [power_to_send // 65536, power_to_send % 65536])
        else:
            print("Data not send")









