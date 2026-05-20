import neurokit2 as nk
import numpy as np
from scipy.signal import savgol_filter, find_peaks


def filter_ecg(signal):

    filtered = savgol_filter(
        signal,
        window_length=31,
        polyorder=3
    )

    return filtered


def detect_r_peaks(signal, sampling_rate=1000):

    peaks, _ = find_peaks(
        signal,
        distance=sampling_rate * 0.5,
        prominence=np.std(signal) * 0.5
    )

    return peaks


def calculate_hrv(r_peaks, sampling_rate=1000):

    rr_intervals = np.diff(r_peaks) / sampling_rate

    mean_rr = np.mean(rr_intervals)
    mean_hr = 60 / mean_rr

    sdnn = np.std(rr_intervals)

    return {
        "RR": rr_intervals,
        "HR": mean_hr,
        "SDNN": sdnn
    }