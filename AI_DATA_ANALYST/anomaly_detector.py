import numpy as np

def detect_anomalies(df):

    numeric = df.select_dtypes(include=np.number)

    if numeric.shape[1] == 0:
        return None

    z_scores = ((numeric - numeric.mean()) / numeric.std()).abs()

    anomalies = df[(z_scores > 3).any(axis=1)]

    return anomalies