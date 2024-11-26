from typing import Sequence, Dict



class Decoder:

    def load(self, data: Dict[str, Sequence[float | str]]) -> None:
        """
        Загрузка значений

        Args:
           data (dict[str, Sequence[float]]): Словарь вида {"Имя параметра": [mean, scale]}
        """
        self.data = data.copy()
    

    def decode(self, data:Dict):
        if not all(name in self.data for name in data): 
            raise ValueError("Not all names in self.data")

        return []

    def encode(self, data:Dict):
        if not all(name in self.data for name in data): 
            raise ValueError("Not all names in self.data")

        return [self.data[name].index(d) if isinstance(d, str) else ((d - self.data[name][0]) / self.data[name][1]) for name, d in data.items()]



import numpy as np
import json
names = 'owners, year, region, mileage, doors, class, body_type, mark, model, super_gen, steering_wheel, gear_type, engine, transmission, power, displacemnt, color'.split(", ")
car = [np.int64(2),
"2011",
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
    m = Decoder()
    with open("configs.json") as f:
        data = json.load(f)
    l:dict = data["labels"]
    l.update(data["scalers"])

    m.load(l)

    print(m.encode({item: car[ind] for ind, item in enumerate(names)}))

    # with open("test.json", 'w') as f:
    #     json.dump({item: car[ind] if isinstance(car[ind], str) else float(car[ind]) for ind, item in enumerate(names)}, f, ensure_ascii=False)