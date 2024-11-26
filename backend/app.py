from sanic import Sanic
from sanic.response import json as s_json
import asyncio
import time
from sanic_cors import CORS
import json
import tensorflow as tf
from decoder import Decoder

MODEL_PATH = "my_model.keras"
app = Sanic("MyApp")
model = tf.keras.models.load_model(MODEL_PATH)
decoder = Decoder()
with open("configs.json") as f:
    data = json.load(f)
    l: dict = data["labels"]
    l.update(data["scalers"])
decoder.load(l)

CORS(app)


@app.post("/predict")
async def predict(request):
    decoded = decoder.decode(request.json)
    pass


if __name__ == '__main__':
    app.run(debug=True)


