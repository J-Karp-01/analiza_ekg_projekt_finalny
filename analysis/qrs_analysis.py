import numpy as np
import pandas as pd


def build_qrs_dataframe(
    df,
    peaks,
    window
):

    ecg_signal = df['ecg_filtrowany'].values
    qrs_dict = {}

    for i, r in enumerate(peaks):

        if r > window and r + window < len(ecg_signal):

            segment = ecg_signal[r - window : r + window].copy()

            segment = segment - np.mean(segment)

            qrs_dict[f'QRS_{i+1:02d}'] = segment

    df_qrs = pd.DataFrame(
        qrs_dict,
        index=range(-window, window)
    )

    return df_qrs