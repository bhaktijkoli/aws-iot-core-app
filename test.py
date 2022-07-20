from datetime import datetime

start_time = datetime.now()
process_time = (datetime.now() - start_time).microseconds
print(str(process_time))
