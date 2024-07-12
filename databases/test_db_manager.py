from db_manager import DatabaseManager
db_manager = DatabaseManager()
last_data = db_manager.get_last_water_quality_and_potability()
if last_data:
    print("Last row data:", last_data)
else:
    print("No data found.")
   
    