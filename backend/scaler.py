from typing import Sequence, Tuple, Dict


class MyStandardScaler():



    def load(self, data: Dict[str, Sequence[float]]) -> None:
        """
        Загрузка значений

        Args:
           data (dict[str, Sequence[float]]): Словарь вида {"Имя параметра": [mean, scale]}
        """
        self.data = data.copy()
    

    def scale(self, names: Sequence[str], data: Sequence[float]) -> Sequence[float]:
        """
        Нормализует значения.

        Args:
            names (Sequence[str]): Имена параметров
            data (Sequence[float]): Соответствующие именам значения

        Returns:
            Sequence[float]: Нормализованные значения
        """
        if len(names) != len(data):
            raise ValueError(f"Expected {len(names)} names, but got {len(data)} data items.")

        
        return [(d - self.data[name][0]) / self.data[name][1] for name, d in zip(names, data)]


    def unscale(self, names: Sequence[str], data: Sequence[float]) -> Sequence[float]:
        """
        Приводит нормализованные значения к исходному виду.

        Args:
            names (Sequence[str]): Имена параметров
            data (Sequence[float]): Соответствующие именам нормализованные значения

        Returns:
            Sequence[float]: Исходные значения
        """
        if len(names) != len(data):
            raise ValueError(f"Expected {len(names)} names, but got {len(data)} data items.")
        
        if not all(name in self.data for name in names): 
            raise ValueError("Not all names in self.data")
        
        return [d * self.data[name][1] + self.data[name][0] for name, d in zip(names, data)]


class MyLabelEncoder():

    def load(self, data: Dict[str, Sequence[str]]) -> None:
        self.data = data.copy()
    

    def decode(self, names: Sequence[str], data: Sequence[float]) -> Sequence[float]:
        if len(names) != len(data):
            raise ValueError(f"Expected {len(names)} names, but got {len(data)} data items.")
        
        if not all(name in self.data for name in names): 
            raise ValueError("Not all names in self.data")
        
        return [self.data[name].index(d) for name, d in zip(names, data)]


    #'owners, year, region, mileage, doors, class, body_type, mark, model, super_gen, steering_wheel, gear_type, engine, transmission, power, displacemnt, color'
    '''
[np.int64(2),
np.int64(2011),
np.int64(1062000),
'Санкт-Петербург и Ленинградская область',
np.int64(253000),
np.float64(5.0),
'D',
'ALLROAD_5_DOORS',
'Nissan',
'X-Trail',
'II Рестайлинг',
'LEFT',
'ALL_WHEEL_DRIVE',
'GASOLINE',
'VARIATOR',
np.float64(141.0),
np.float64(1997.0),
'200204']
    '''
import numpy as np
import json
names = 'owners, year, region, mileage, doors, class, body_type, mark, model, super_gen, steering_wheel, gear_type, engine, transmission, power, displacemnt, color'.split(", ")
car = [np.int64(2),
np.int64(2011),
'Санкт-Петербург и Ленинградская область',
np.int64(253000),
np.float64(5.0),
'D',
'ALLROAD_5_DOORS',
'Nissan',
'X-Trail',
'II Рестайлинг',
'LEFT',
'ALL_WHEEL_DRIVE',
'GASOLINE',
'VARIATOR',
np.float64(141.0),
np.float64(1997.0),
'200204']

if __name__ == "__main__":
    import numpy as np
    import json
    m = MyLabelEncoder()
    with open("configs.json") as f:
        data = json.load(f)["labels"]
    m.load(data)

    print(m.decode(names, car))
