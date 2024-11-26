from typing import Sequence, Dict


class StandardUnscaler():
    
    def load(self, data: Dict[str, Sequence[float, float]]) -> None:
        """
        Загрузка значений

        Args:
           data (dict[str, Sequence[float]]): Словарь вида {"Имя параметра": [mean, scale]}
        """
        self.data = data.copy()


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


class LabelDecoder():
    def load(self, data: Dict[str, Sequence[str]]) -> None:
        self.data = data.copy()
    

    def decode(self, names: Sequence[str], data: Sequence[float]) -> Sequence[float]:
        if len(names) != len(data):
            raise ValueError(f"Expected {len(names)} names, but got {len(data)} data items.")
        
        if not all(name in self.data for name in names): 
            raise ValueError("Not all names in self.data")
        
        return [self.data[name][d] for name, d in zip(names, data)]