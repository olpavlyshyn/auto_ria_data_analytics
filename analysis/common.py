import pandas as pd
import numpy as np
import os
import glob


def read_cars_data(folder):
    data_files = glob.glob(os.path.join(folder, "*.csv"))
    columns = ["Brand", "Model", "Year", "Url", "Currency", "Price", "Mileage", "Location", "Fuel", "Gearbox",
               "Vin", "Num", "Accident", "Created", "Modified", "Sold"]
    df = pd.concat(
        map(lambda file: pd.read_csv(file, delimiter=';', encoding="windows=1251", names=columns), data_files))
    df["Mileage"] = df["Mileage"].str[:-8].astype(int)
    df['FuelType'] = df['Fuel'].str.split(',').str[0]
    df['EngineСapacity'] = df['Fuel'].str.split(',').str[1]
    fuel_types = ['Дизель', 'Газ / Бензин', 'Бензин', 'Гібрид', 'Електро', 'Газ', 'Інше', 'Газ пропан-бутан']
    df['FuelType'] = df['FuelType'].map(lambda x: x if x in fuel_types else np.nan)
    df['EngineСapacity'] = df['EngineСapacity'].str[:-3].astype(np.float)
    return df
