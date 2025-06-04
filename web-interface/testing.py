# from model.all_data import AllData
# from services.app_service import AppService
# from flask import Flask, render_template, request, jsonify, url_for, current_app
# from model.raspi import get_info_raspi
# # all_data: AllData = AllData()
# # print(all_data.data_range(21, 3, "31-05-2025", "01-06-2025"))  # For testing purposes, prints the data range from the database
# # print(len(all_data.data_range(21, 3, "31-05-2025", "01-06-2025")["temp"]))
from model.raspi import RaspiSsh
# app_service = AppService()
# app_service.get_all_data(21, 3, "31-05-2025", "01-06-2025")



# print(type(range(0, 10)))

# help(range)




# a = get_info_raspi()
# print(a["ip"])  # Prints the IP and SSID of the Raspberry Pi

raspi: RaspiSsh = RaspiSsh()

raspi.run_script()