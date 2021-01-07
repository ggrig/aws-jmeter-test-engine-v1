from influxdb import InfluxDBClient
from create_stack import Config
from datetime import datetime, timedelta
from create_stack import Config


# Connect to influx database, check if tests database exists. If it does not, create it.


def connect_to_influxdb(config):
    client = InfluxDBClient(host=Config.influx_host, port=8086)

    # This will create a database called "tests" if it does not exist. If it already exists, this does nothing.
    client.create_database('tests')
    client.switch_database("tests")
    return client

    # resp = client.write_points(
    #     [{"measurement": "runningTests", "fields": {"duration": 101, "startTime": 102, "endTime": 103}}])
    #
    # results = client.query('SELECT * from "tests"."autogen"."runningTests"')
    # print(results.raw)
    #
    # # here you can get the data in rows and print them one by one, or print specific fields from within.
    # points = results.get_points()
    # for p in points:
    #     print(p)


def insert_dummy_data(config):
    client = connect_to_influxdb(Config)

    # for i in range(0, 10):
    #     start_time = datetime.now() + timedelta(seconds=int(10 + i))
    #     load_type = "Proxy" if i % 2 == 0 else "Direct"
    #     prefix = "test{0}".format(i)
    #     client.write_points([
    #         {"measurement": "TestRun",
    #          "fields": {"StartTime": str(start_time), "Prefix": prefix, "RunId": i, "RunTime": 100 * i, "RampUp": 10 * i + 1, "Threads": 10 * i + 2,
    #                     "TotalRequests": 10 * i + 3, "SuccessfulRequests": 10 * i + 4, "FailedRequests": 10 * i + 5, "AverageResponseTime": 10 * i + 6,
    #                     "MaxConcurrentPods": 10 * i + 7, "Status": i % 2, "LoadType": load_type}}])

    client.write_points([
        {"measurement": "TestRun",
         "fields": {"StartTime": str(datetime.now()), "Prefix": "aj", "RunId": "9bc04c12-911f-46be-b36e-5ac9a202272a", "RunTime": 100 , "RampUp": 10, "Threads": 11,
                    "TotalRequests": 13, "SuccessfulRequests": 14, "FailedRequests": 15, "AverageResponseTime": 16,
                    "MaxConcurrentPods": 17, "Status": 0, "LoadType": "Direct"}}])

    client.write_points([
        {"measurement": "TestRun",
         "fields": {"StartTime": str(datetime.now() + timedelta(seconds=int(10))), "Prefix": "aj2", "RunId": "e88f826b-c9ed-4e66-a793-bb156c2997d2",
                    "RunTime": 200, "RampUp": 20, "Threads": 21,
                    "TotalRequests": 23, "SuccessfulRequests": 24, "FailedRequests": 25, "AverageResponseTime": 26,
                    "MaxConcurrentPods": 27, "Status": 1, "LoadType": "Proxy"}}])

    client.write_points([
        {"measurement": "TestRun",
         "fields": {"StartTime": str(datetime.now() + timedelta(seconds=int(20))), "Prefix": "aj3", "RunId": "5860e3dc-4490-4f49-870b-b070b555bfa8",
                    "RunTime": 300, "RampUp": 30, "Threads": 31,
                    "TotalRequests": 33, "SuccessfulRequests": 34, "FailedRequests": 35, "AverageResponseTime": 36,
                    "MaxConcurrentPods": 37, "Status": 1, "LoadType": "Direct"}}])



# inserts additional info for use in conjunction with other table containing test run results
def database_insert_test(run_id, grafana_uid, duration):
    run_id = str(run_id)
    print("Values to insert into DB: {0} {1} {2}".format(run_id, grafana_uid, duration))
    client = connect_to_influxdb(Config)
    client.write_points([{"measurement": "TestsInfo", "fields": {"RunId": run_id, "Duration": duration, "GrafanaUid": grafana_uid}}])

    print("DB contains: ")
    results = client.query('SELECT * from "tests"."autogen"."TestsInfo"')
    points = results.get_points()
    for p in points:
        print(p)


def retrieve_test_results():
    client = connect_to_influxdb(Config)
    results = client.query('SELECT * from "tests"."autogen"."TestRun"')
    return results.raw


def retrieve_test_info():
    client = connect_to_influxdb(Config)
    results = client.query('SELECT * from "tests"."autogen"."TestsInfo"')
    return results.raw


if __name__ == "__main__":
    pass
    client = connect_to_influxdb(Config)
    print(client.get_list_database())
    # client.drop_database("tests")
    insert_dummy_data(Config)
    results = client.query('SELECT * from "tests"."autogen"."TestRun"')
    # results1 = client.query('SELECT * from "tests"."autogen"."TestRun" ORDER BY time DESC') <-- good for when you want latest data
    # results2 = client.query('SELECT * from "tests"."autogen"."TestRun"')
    # print(results1.raw)
    # print(results2.raw)
    points = results.get_points()
    for p in points:
        print(p)
