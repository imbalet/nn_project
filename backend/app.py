from sanic import Sanic
from sanic.response import json as s_json
from sanic.response import file
import asyncio
import time
from sanic_cors import CORS
import json
import tensorflow as tf
from decoder import Decoder
import numpy as np

# ---------------------------------

MODEL_PATH = "backend/my_model.keras"

# ---------------------------------

app = Sanic(__name__)
CORS(app)
app.static('/', 'frontend')

model = tf.keras.models.load_model(MODEL_PATH)
decoder = Decoder()

with open("backend/configs.json") as f:
    data = json.load(f)
    l: dict = data["labels"]
    l.update(data["scalers"])
decoder.load(l)


with open("backend/params.json") as f:
    params = json.load(f)

with open("backend/variants.json") as f:
    variants = json.load(f)


@app.get("/")
async def home(request):
    return await file('frontend/index.html')


@app.get("/params")
def get_params(request):
    return s_json(params)


@app.get("/marks")
async def get_marks(request):
    return s_json({"mark": list(variants["mark"].keys())})


@app.get("/models")
async def get_model(request):
    mark = request.json["mark"]
    return s_json({"model": list(variants["mark"].get(mark, {}).keys())})


@app.get("/gens")
async def get_gen(request):
    mark = request.json["mark"]
    model = request.json["model"]
    return s_json({"gen": list(variants["mark"].get(mark, {}).get(model, {}).keys())})


@app.get("/otherCarCharacteristics")
async def get_other_car_characteristics(request):
    mark = request.json["mark"]
    model = request.json["model"]
    gen = request.json["gen"]
    return s_json(
        {
            "transmission": variants["mark"].get(mark, {}).get(model, {}).get(gen, {}).get("transmisson", ""),
            "engine": variants["mark"].get(mark, {}).get(model, {}).get(gen, {}).get("engine", ""),
            "body_type": variants["mark"].get(mark, {}).get(model, {}).get(gen, {}).get("body_type", ""),
            "year": variants["mark"].get(mark, {}).get(model, {}).get(gen, {}).get("year", ""),
        }
    )


@app.get("/otherCarInfo")
async def get_other_car_info(request):
    return s_json(
        {
            "owners": variants["owners"],
            "region": variants["region"],
            "steering_wheel": variants["steering_wheel"],
            "gear_type": variants["gear_type"],
            "color": variants["color"],
        }
    )
# @app.get("/owners")
# async def get_owners(request):
#     return s_json({"owners": variants["owners"]})


# @app.get("/regions")
# async def get_regions(request):
#     return s_json({"region": variants["region"]})


# @app.get("/body_type")
# async def get_body_type(request):
#     return s_json({"body_type": variants["body_type"]})



@app.post("/predict")
async def predict(request):
    decoded = decoder.encode(request.json)
    prediction = model.predict(np.array(decoded).reshape(1, -1))
    return s_json({"predicted": decoder.decode({"price": float(prediction[0][0])})[0]})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1488)
