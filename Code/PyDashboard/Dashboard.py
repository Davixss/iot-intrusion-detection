from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from Config import *

client = InfluxDBClient(url=Config.host_influx, token=Config.token_influx)
write_api = client.write_api(write_options=SYNCHRONOUS)

query = f'from(bucket:"{Config.bucket}") |> range(start: -30d) |> filter(fn: (r) => r["_measurement"] == "{Config.bucket}") |> sort(columns: ["_time"], desc: true)'
result = client.query_api().query(query=query, org=Config.org_influx)

print("Intrusion \t Sensortype \t Time")

for table in result:
    for record in table.records:
        time = record.values["_time"]
        intrusion = record.values["Intrusion"]
        sensortype = record.get_value()
        time = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        print(intrusion, "\t\t", sensortype, "\t\t", time)
