import time

from app.exception.network_error import NetworkError
from app.exception.no_data_error_storage import NoDataStorageError
from app.grid_analyzer.grid_analyzer import ModbusTCPInterface
from app.storage.storage import Storage
from utils.parser import ParamParser

total_power = 5000 # Specify t o t a l power to be consumed by b att e r y and cha rging i n Watts
IP_1 = " 172.25.224.74 " # IP address of grid analyzer at charging point
IP_2 = " 172.25.224.75 " # IP address of grid analyzer at battery syste ,
IP_3 = " 172.25.224.76 "



grid_analyzer = ModbusTCPInterface(IP_1, 500)
storage = Storage(IP_1, 5000, "Battery storage")

connection_count = 0
past_time_in_s = 0

while connection_count < 10 or past_time_in_s < 150000:
    try:
        storage.initialize_client()
        grid_data = grid_analyzer.get_data()
        storage.write_data_to_storage()
        time.sleep(30000)
        past_time_in_s += 30000

    except NetworkError:
        connection_count += 1

    except NoDataStorageError:
        break






