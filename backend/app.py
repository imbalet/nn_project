from sanic import Sanic
from sanic.response import json as s_json
# from sanic.response import file
from sanic_cors import CORS
import json
import tensorflow as tf
import numpy as np

from tools.json_db import Db
from tools.decoder import Decoder

# ---------------------------------

MODEL_PATH = "backend/files/my_model.h5"

# ---------------------------------

app = Sanic(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.static('/', 'frontend')

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
model = tf.keras.models.load_model(MODEL_PATH)
decoder = Decoder()
db = Db("backend/files/labels.json", "backend/files/d.json")


with open("backend/files/configs.json") as f:
    data = json.load(f)
    l: dict = data["labels"]
    l.update(data["scalers"])
decoder.load(l)


with open("backend/files/params.json") as f:
    params = json.load(f)

# -------------ROUTES--------------


# @app.get("/")
# async def home(request):
#     return await file('frontend/index.html')


@app.get("/api/params")
def get_params(request):
    return s_json(params)


@app.get("/api/marks")
async def get_marks(request):
    return s_json(db.get_marks())


@app.get("/api/steering_wheels")
async def get_steering_wheels(request):
    return s_json(db.get_steering_wheel())


@app.get("/api/owners")
async def get_owners(request):
    return s_json(db.get_owners())


@app.get("/api/regions")
async def get_regions(request):
    return s_json(db.get_regions())


@app.get("/api/gear_types")
async def get_gear_type(request):
    return s_json(db.get_gear_type())


@app.get("/api/colors")
async def get_color(request):
    return s_json(db.get_colors())


@app.post("/api/models")
async def get_models(request):
    mark = request.json["mark"]
    return s_json(db.get_models_car(mark))


@app.post("/api/gens")
async def get_gens(request):
    mark = request.json["mark"]
    model = request.json["model"]
    return s_json(db.get_super_gen_names_car(mark, model))


@app.post("/api/bodies")
async def get_bodies(request):
    mark = request.json["mark"]
    model = request.json["model"]
    gen = request.json["gen"]
    return s_json(db.get_body_types_car(mark, model, gen))


@app.post("/api/complectations")
async def get_complectations(request):
    mark = request.json["mark"]
    model = request.json["model"]
    gen = request.json["gen"]
    return s_json(db.get_complectations_car(mark, model, gen))


@app.post("/api/transmission")
async def get_ctransmission(request):
    mark = request.json["mark"]
    model = request.json["model"]
    gen = request.json["gen"]
    return s_json(db.get_transmissions_car(mark, model, gen))


@app.post("/api/engines")
async def get_transmission(request):
    mark = request.json["mark"]
    model = request.json["model"]
    gen = request.json["gen"]
    return s_json(db.get_engines_car(mark, model, gen))


@app.post("/api/years")
async def get_year(request):
    mark = request.json["mark"]
    model = request.json["model"]
    gen = request.json["gen"]
    return s_json(db.get_years_car(mark, model, gen))


@app.post("/api/predict")
async def predict(request):
    decoded = decoder.encode(request.json)
    prediction = model.predict(np.array(decoded).reshape(1, -1))
    return s_json({"predicted": decoder.decode({"price": float(prediction[0][0])})[0]})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
