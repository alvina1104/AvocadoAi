from fastapi import FastAPI
import uvicorn
import joblib
from pydantic import BaseModel

model = joblib.load('log_model.pkl')
scaler = joblib.load('scaler.pkl')

avocado_app = FastAPI()


class AvocadoSchema(BaseModel):
    firmness: float
    hue: int
    saturation: int
    brightness: int
    sound_db: int
    weight_g: int
    size_cm3: int
    color_category: str



@avocado_app.post("/predict")
async def predict(avocado: AvocadoSchema):
    avocado_dict = avocado.dict()

    color_category = avocado_dict.pop('color_category')
    color1_0 = [
        1 if color_category == 'dark green' else 0,
        1 if color_category == 'green' else 0,
        1 if color_category == 'purple' else 0
    ]

    avocado_data = list(avocado_dict.values()) + color1_0

    scaler_data = scaler.transform([avocado_data])
    pred_index = model.predict(scaler_data)[0]

    if pred_index == 1:
        ripeness = "Hard"
    elif pred_index == 2:
        ripeness = "Pre-conditioned"
    elif pred_index == 3:
        ripeness = "Breaking"
    elif pred_index == 4:
        ripeness = "Firm-ripe"
    elif pred_index == 5:
        ripeness = "Ripe"
    else:
        ripeness = "Unknown"

    return {"predicted_ripeness": ripeness}



if __name__ == '__main__':
    uvicorn.run(avocado_app, host="127.0.0.1", port=8000)
