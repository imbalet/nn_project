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


@app.get("/api/params")
def get_params(request):
    return s_json(params)


@app.get("/marks")
async def get_marks(request):
    return s_json({"mark": list(variants["mark"].keys())})


@app.get("/api/marks")
async def get_marks(request):
    marks = [] # db request
    return marks


@app.get("/api/models")
async def get_models(request):
    mark_id = request.json["mark_id"]
    models = [] # db request
    return models


@app.get("/api/gens")
async def get_gens(request):
    model_id = request.json["model_id"]
    gens = [] # db request
    return gens


# @app.get("/api/bodies")
# async def get_bodies(request):
#     gen_id = request.json["gen_id"]
#     bodies = [] # db request
#     return bodies


@app.get("/api/otherCharactestics")
async def get_other_charactestics(request):
    gen_id = request.json["gen_id"]
    other_charactestics = [] # db request
    return other_charactestics




# @app.get("/models")
# async def get_model(request):
#     mark = request.json["mark"]
#     return s_json({"model": variants["mark"][mark]})


# @app.get("/gens")
# async def get_gen(request):
#     mark = request.json["mark"]
#     model = request.json["model"]
#     return s_json({"gen": variants["mark"][mark][model]})


# @app.get("/otherCarInfo")
# async def get_other_car_info(request):
#     mark = request.json["mark"]
#     model = request.json["model"]
#     gen = request.json["gen"]
#     return s_json({"gen": variants["mark"][mark][model]})


@app.post("/predict")
async def predict(request):
    decoded = decoder.encode(request.json)
    prediction = model.predict(np.array(decoded).reshape(1, -1))
    return s_json({"predicted": decoder.decode({"price": float(prediction[0][0])})[0]})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1488)
