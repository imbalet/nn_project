from typing import Sequence, Dict

order = ['owners', 'year', 'region', 'mileage', 'mark', 'model', 'complectation', 'steering_wheel', 'gear_type', 'engine', 'transmission', 'power', 'displacement', 'color', 'body_type_type', 'super_gen_name']

class Decoder:

    def load(self, data: Dict[str, Sequence[float | str]]) -> None:
        """
        Загрузка значений

        Args:
            data (dict[str, Sequence[float]]):
                Словарь вида {"Имя параметра": [mean, scale]}
        """
        self.data = data.copy()

    def decode(self, data: Dict):
        if not all(name in self.data for name in data):
            raise ValueError("Not all names in self.data")

        return [self.data[name][d] if isinstance(d, str)
                else (d * self.data[name][1] + self.data[name][0])
                for name, d in data.items()]

    def encode(self, data: Dict):
        if not all(name in self.data for name in data):
            raise ValueError("Not all names in self.data")

        data = {key: data[key] for key in order}
        
        dd = []
        for name, d in data.items():
            if isinstance(self.data[name][0], str):
                dd.append(self.data[name].index(d))
            else:
                dd.append((float(d) - self.data[name][0]) / self.data[name][1])

        return dd


def main():
    import json

    decoder = Decoder()

    with open("test.json") as f:
        data = json.load(f)

    with open("configs.json") as f:
        d: dict = json.load(f)
        l: dict = d["labels"]
        l.update(d["scalers"])
    decoder.load(l)

    print(decoder.encode(data))
    print(decoder.decode({"price": 0.4}))


if __name__ == "__main__":
    main()
