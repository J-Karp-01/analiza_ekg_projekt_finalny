import numpy as np
import pandas as pd
from scipy.signal import find_peaks



def detect_resp_cycles(
    respiration_signal,
    fs=1000
):

    peaks, _ = find_peaks(
        respiration_signal,
        distance=fs*2
    )

    return peaks



def compute_resp_phase(
    r_peaks,
    resp_peaks
):

    phases = []

    cycle_numbers = []

    for r in r_peaks:

        for i in range(len(resp_peaks)-1):

            start = resp_peaks[i]
            end = resp_peaks[i+1]

            if start <= r < end:

                phase = 2 * np.pi * ((r - start) / (end - start))

                phases.append(phase)

                cycle_numbers.append(i)

                break

    return np.array(phases), np.array(cycle_numbers)

def build_synchrogram_dataframe(
    r_peaks,
    phases,
    cycle_numbers,
    fs=1000
):

    df_sync = pd.DataFrame({

        "r_peak": r_peaks[:len(phases)],

        "czas":
            r_peaks[:len(phases)] / fs,

        "faza":
            phases,

        "faza_deg":
            np.degrees(phases),

        "cykl":
            cycle_numbers
    })

    df_sync['beat'] = (
        df_sync.groupby('cykl')
        .cumcount() + 1
    )

    df_sync = df_sync[
        df_sync['beat'] <= 6
    ]

    return df_sync