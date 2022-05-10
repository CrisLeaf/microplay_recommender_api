import numpy as np
import pandas as pd
import pytest
from app import create_app
from flask import json


def test_app():
    df = pd.read_csv("train_data.csv")

    app = create_app()
    c = app.test_client()
    c.get("/train")

    for i in np.random.randint(0, df.shape[0], 100):
        url = df["url"].iloc[i]
        response = c.get(f"/reco?url={url}")
        data = json.loads(response.get_data())["recommendations"]

        for d in data:
            assert d[0] in df["url"].values
            assert d[1] in df["name_original"].values
            assert d[2] in df["image"].values
