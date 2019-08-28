import pandas as pd
import datetime

#different dataframes for all of our data

stop_time_data = pd.read_csv('./CS370data/stop_times.txt', sep=",", header=None)
stop_time_data.columns = ["trip_id", "arrival_time" , "departure_time" , "stop_id" ," stop_sequence" ,"pickup_type" ,"drop_off_type", "shape_dist_traveled"]

stops_data = pd.read_csv('./CS370data/stops.txt', sep=",", header=None)
stops_data.columns = ["stop_id","stop_code","stop_name","stop_desc","stop_lat","stop_lon","zone_id"]

trips_data = pd.read_csv('./CS370data/trips.txt', sep=",", header=None)
trips_data.columns = ["route_id","service_id","trip_id","trip_headsign","direction_id","block_id","shape_id"]

#time



#maybe try to combine all my tables into one and do my looping on there
def get_dest_info(starting, ending, direction):
    for (idx,row) in stops_data.iterrows():
        if row.loc['stop_name'] == starting.upper():#determining if we have data for the inputs
            val = get_times(row.loc["stop_id"], direction)
            return val

def get_times(stop_id, direction):
    train_times = []
    for (idx,row) in stop_time_data.iterrows():
        if row.loc['stop_id'] == stop_id:
             val = get_trips(row.loc['trip_id'], direction)
             now = datetime.datetime.now()#might have to check if time is greater than hour 24
             if row.loc["arrival_time"] < "23:59:59":
                 if val == 1 and pd.to_datetime(row.loc["arrival_time"])>now:
                    train_times.append(row.loc["arrival_time"])
    return train_times


def get_trips(trip_id, direction):
    for (idx,row) in trips_data.iterrows():
        if row.loc['trip_id'] == trip_id:
            if direction == row.loc['direction_id']:
                return 1
            else:
                return 0
                
lst=[]
lst = get_dest_info("new brunswick","newark penn station", "0")
lst=list(set(lst))
lst.sort()

print(','.join(lst))

#print(stop_time_data.iloc[:,1:4])
#print(stops_data)
#print(trips_data)
