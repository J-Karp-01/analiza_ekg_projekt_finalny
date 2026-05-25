# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:39:23 2026

@author: bekis
"""

import streamlit as st
from assets.colors import (
    bialy,
    bialo_szary,
    rozowy,
    niebieski,
    zielony,
    czerwony,
    lekki_szary,
    lekki_czerwony,
    mocny_szary
)

from components.header import render_header
from utils.loaders import load_exercise_data,load_rest_data
from components.signal_range_panel import render_signal_range_panel
from analysis.ecg_analysis import filter_ecg
from components.filter_panel import render_filter_panel
from components.ecg_plot import render_ecg_plot
from analysis.r_peak_analysis import detect_r_peaks,create_rr_dataframe
from components.r_peak_panel import render_r_peak_panel
from components.hrv_panel import render_hrv_panel
from analysis.qrs_analysis import build_qrs_dataframe
from components.qrs_panel import render_qrs_panel


st.set_page_config(
    layout="wide"
)


render_header(
    bialy,
    lekki_szary,
    lekki_czerwony,
    mocny_szary
)


wybor_ekg = st.selectbox(
    "Wybierz rodzaj EKG",
    [
        "EKG wysiłkowe",
        "EKG spoczynkowe"
    ]
)


if wybor_ekg == "EKG wysiłkowe":

    df = load_exercise_data()

else:

    df = load_rest_data()


st.write(
    f"Aktualny sygnał: {wybor_ekg}"
)

df = render_signal_range_panel(
    df,
    bialo_szary,
    lekki_czerwony
)


col2, window_length, polyorder = render_filter_panel(
    lekki_czerwony
)


df['ecg'].astype(float)

surowy_wektor = df['ecg'].values

df['ecg_filtrowany'] = filter_ecg(
    surowy_wektor,
    window_length,
    polyorder
)


render_ecg_plot(
    df,
    col2,
    lekki_czerwony
)

threshold_rr = 0.11
distance_rr = 450

sygnal = df['ecg_filtrowany'].values

peaks = detect_r_peaks(
    sygnal,
    threshold_rr,
    distance_rr
)

df_rr, rr_intervals = create_rr_dataframe(
    df,
    peaks
)

col2 = render_r_peak_panel(
    df,
    peaks,
    threshold_rr,
    distance_rr,
    df_rr,
    niebieski,
    lekki_szary,
    bialy
)

render_hrv_panel(
    col2,
    df_rr,
    rr_intervals,
    niebieski,
    lekki_szary
)

window = 250

df_qrs = build_qrs_dataframe(
    df,
    peaks,
    window
)

render_qrs_panel(
    df,
    peaks,
    df_qrs,
    zielony,
    niebieski
)