from model.all_data import AllData

all_data: AllData = AllData()
print(all_data.data_range(21, 21, "31-05-2025", "31-05-2025"))  # For testing purposes, prints the data range from the database