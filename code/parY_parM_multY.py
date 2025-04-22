import cdsapi 
import geopandas as gpd
import os
from timeit import timeit
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool, current_process
import pandas as pd

ecmw_dir =  "D:\\CAFE_DATA_MANAGEMENT\\ERA5_Python\\downloading_benchmark"

variable_list = ["2m_dewpoint_temperature",
                 "2m_temperature",
                 "skin_temperature", 
                 "surface_net_solar_radiation",
                 "surface_net_thermal_radiation",
                 "surface_solar_radiation_downwards",
                 "surface_thermal_radiation_downwards",
                 "10m_u_component_of_wind"]

kenya_shape =  gpd.read_file(os.path.join(ecmw_dir, "Kenya_GADM\\gadm41_KEN.gpkg"), layer = "ADM_ADM_0")

kenya_bbox = kenya_shape.total_bounds

kenya_bbox[0] = round(kenya_bbox[0], 1) - 0.1
kenya_bbox[1] = round(kenya_bbox[1], 1) - 0.1
kenya_bbox[2] = round(kenya_bbox[2], 1) + 0.1
kenya_bbox[3] = round(kenya_bbox[3], 1) + 0.1

query_area = [kenya_bbox[0], kenya_bbox[1], kenya_bbox[2], kenya_bbox[3]]

query_years = list(range(2000, 2002))
query_years_str = [str(x) for x in query_years]

query_months = list(range(1, 13))
query_months_str = [str(x).zfill(2) for x in query_months]

def process_task(zips):
    variables, year_str, month_str = zips

    dataset = "reanalysis-era5-land"
    request = {
                "product_type": "reanalysis",
                "variable": variables, 
                "year": year_str,
                "month": month_str,
                "day": [  
                        "01", "02", "03",
                        "04", "05", "06",
                        "07", "08", "09",
                        "10", "11", "12",
                        "13", "14", "15",
                        "16", "17", "18",
                        "19", "20", "21",
                        "22", "23", "24",
                        "25", "26", "27",
                        "28", "29", "30",
                        "31"],
                "time": [
                        "00:00", "01:00", "02:00",
                        "03:00", "04:00", "05:00",
                        "06:00", "07:00", "08:00",
                        "09:00", "10:00", "11:00",
                        "12:00", "13:00", "14:00",
                        "15:00", "16:00", "17:00",
                        "18:00", "19:00", "20:00",
                        "21:00", "22:00", "23:00"],
                "data_format": "netcdf",
                "download_format": "unarchived",
                "area": query_area
    }

    client = cdsapi.Client()
    try:
        client.retrieve(dataset, request).download(os.path.join(ecmw_dir,
                                                                "ERA5_Out_Parallel_2", 
                                                                "{}_{}_{}.nc".format(year_str, month_str, len(variables))))
    except:
        time.sleep(10)
        client.retrieve(dataset, request).download(os.path.join(ecmw_dir,
                                                                "ERA5_Out_Parallel_2", 
                                                                "{}_{}_{}.nc".format(year_str, month_str, len(variables))))
    
    print(f'running on process: {current_process()._identity[0]}', variables, year_str, month_str)


def give_input(variables, years_str, months_str):
    print('# of variables: {}'.format(len(variables)))
    variables_repeat = [variables] * len(months_str)
    zippedObject = list()
    for year_str in years_str:
        year_repeat = [year_str] * len(months_str)
        zipped = list(zip(variables_repeat, year_repeat, months_str))
        zippedObject.extend(zipped)
    # Download data both over years and over months in a given year in parallel
    with Pool(processes=8) as pool:
        try:
            pool.map(process_task, zippedObject)
        except:
            time.sleep(10)
            pool.map(process_task, zippedObject)
        pool.close()
        pool.join()
    print("All tasks completed.")


if __name__ == '__main__':
    benchmarks = list()
    for i in range(len(variable_list)):
        variables = variable_list[0: i+1]
        # benchmark the task
        result = timeit(lambda: give_input(variables, query_years_str, query_months_str), setup='from __main__ import give_input', number=1)
        # report the result
        print('Time: {} seconds'.format(result))
        benchmarks.append(result)

    benchmarks_parallel = pd.DataFrame(benchmarks)
    benchmarks_parallel.to_csv('D:\\CAFE_DATA_MANAGEMENT\\ERA5_Python\\downloading_benchmark\\ERA5_Out_Parallel_2\\benchmarks_parallel.csv')
    
    numVariables = range(1, len(variable_list) + 1)

    plt.plot(numVariables, benchmarks, 'b')
    plt.xlabel('# of Variables')
    plt.ylabel('Time (seconds)')
    plt.show()





