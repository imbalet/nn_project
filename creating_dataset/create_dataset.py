import json
import os

os.chdir(os.path.dirname(__file__))

lst = []

l = len(os.listdir("data"))

for ind, i in enumerate(os.listdir("data")):
    print(f"{ind} / {l}")
    with open(os.path.join("data", i), encoding="utf8") as f:
        data = json.load(f)

        for ind, el in enumerate(data):
            reg = eval(el["region"])
            data[ind]["region"] = {"name": reg["region_info"]["name"], "id": reg["geobase_id"]}

        lst.extend(data)


with open("new.json", 'w', encoding="utf8") as f:
    json.dump(lst, f, ensure_ascii=False)
