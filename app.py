# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:39:23 2026

@author: bekis
"""

import streamlit as st
from assets.colors import (bialy,bialo_szary,rozowy,niebieski,zielony,czerwony,lekki_szary,lekki_czerwony,mocny_szary,fioletowy,żółty,cyjan,neon_yellow,neon_pink,neon_green,neon_orange,neon_purple)
from components.header import render_header
from utils.loaders import load_exercise_data,load_rest_data,load_resp_normal,load_resp_control,load_uploaded_file
from components.signal_range_panel import render_signal_range_panel
from analysis.ecg_analysis import filter_ecg
from components.filter_panel import render_filter_panel
from components.ecg_plot import render_ecg_plot
from analysis.r_peak_analysis import detect_r_peaks,create_rr_dataframe
from components.r_peak_panel import render_r_peak_panel
from components.hrv_panel import render_hrv_panel
from analysis.qrs_analysis import build_qrs_dataframe
from components.qrs_panel import render_qrs_panel
from analysis.emd_analysis import compute_emd
from components.emd_panel import render_emd_panel
from components.respiration_panel import render_respiration_panel
from utils.pdf_raport import generate_pdf_report

st.set_page_config(layout="wide")

render_header(bialy,lekki_szary,lekki_czerwony,mocny_szary)

uploaded_file = st.file_uploader("Załaduj własny plik",type=['txt', 'csv', 'xlsx'])

wybor_ekg = st.selectbox(
    "Wybierz rodzaj EKG",
    [
        "EKG wysiłkowe",
        "EKG spoczynkowe",
        "EKG + oddech normalny",
        "EKG + oddech kontrolowany"
    ],
    disabled=uploaded_file is not None
)

if uploaded_file is not None:

    df = load_uploaded_file(uploaded_file)
    czy_resp = True

else:

    if wybor_ekg == "EKG wysiłkowe":

        df = load_exercise_data()

        czy_resp = False

    elif wybor_ekg == "EKG spoczynkowe":

        df = load_rest_data()

        czy_resp = False

    elif wybor_ekg == "EKG + oddech normalny":

        df = load_resp_normal()

        czy_resp = True

    elif wybor_ekg == "EKG + oddech kontrolowany":

        df = load_resp_control()

        czy_resp = True

if uploaded_file is not None:

    aktualny_sygnal = uploaded_file.name

else:

    aktualny_sygnal = wybor_ekg

st.write(f"Aktualny sygnał: {aktualny_sygnal}")

if czy_resp:

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Sygnał EKG",
        "💓 Piki R/HRV",
        "🫀 Segmentacja QRS",
        "🧬 Dekompozycja Sygnału",
        "🌬️ Synchronizacja sercowo oddechowa"
    ])

else:

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Sygnał EKG",
        "💓 Piki R/HRV",
        "🟢 Segmentacja QRS",
        "🧬 Dekompozycja Sygnału"
    ])

with tab1:

    df_view, df = render_signal_range_panel(
        df,
        bialo_szary,
        lekki_czerwony
    )

    col2, window_length, polyorder = render_filter_panel(lekki_szary)

    df_view['ecg'].astype(float)

    surowy_wektor = df_view['ecg'].values

    df_view['ecg_filtrowany'] = filter_ecg(
        surowy_wektor,
        window_length,
        polyorder
    )

    render_ecg_plot(
        df_view,
        col2,
        lekki_czerwony
    )

with tab2:

    threshold_rr = 0.11
    distance_rr = 450

    sygnal = df_view['ecg_filtrowany'].values

    peaks = detect_r_peaks(
        sygnal,
        threshold_rr,
        distance_rr
    )

    df_rr, rr_intervals = create_rr_dataframe(
        df_view,
        peaks
    )

    col_right, threshold_rr, distance_rr, df_rr = render_r_peak_panel(
        df_view,
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
with tab3:

    window = 250

    df_qrs = build_qrs_dataframe(
        df_view,
        peaks,
        window
    )

    render_qrs_panel(
        df_view,
        peaks,
        df_qrs,
        zielony,
        niebieski
    )

with tab4:

    signal_emd = df_view['ecg_filtrowany'].values[:3000]

    df_imfs = compute_emd(signal_emd)

    render_emd_panel(
        df_view,
        df_imfs,
        fioletowy
    )

if czy_resp:

    with tab5:

        render_respiration_panel(
            df_view,
            lekki_czerwony,
            żółty,
            cyjan,
            neon_yellow,
            neon_pink,
            neon_green,
            neon_orange,
            neon_purple
        )


st.markdown("""
<hr style="
    margin-top:40px;
    margin-bottom:30px;
    height:3px;
    border:none;
    background-color:#5c5c5c;
">
""", unsafe_allow_html=True)

st.markdown("""
<p style="
    color:#00e5ff;
    font-size:18px;
    font-weight:700;
    margin-bottom:10px;
">
Eksport raportu PDF
</p>
""", unsafe_allow_html=True)

st.write("""
Raport zawiera podsumowanie analizy:
- Informacje o analizie 
- Parametry analizy
- Statystyki HRV
- Analiza synchronizacji fazowej 
""")

srednie_rr = rr_intervals.mean()
sdnn = rr_intervals.std()
max_rr = rr_intervals.max()
min_rr = rr_intervals.min()
liczba_R = len(rr_intervals)

signal_duration = df['czas'].max()
sample_count = len(df)
analysis_start = df['czas'].min()
analysis_end = df['czas'].max()

if st.button("Generuj raport PDF"):

    generate_pdf_report(
        output_path="raport_ekg.pdf",
        aktualny_sygnal=aktualny_sygnal,
        threshold_rr=threshold_rr,
        distance_rr=distance_rr,
        srednie_rr=srednie_rr,
        sdnn=sdnn,
        min_rr=min_rr,
        max_rr=max_rr,
        liczba_r=liczba_R,
        signal_duration=signal_duration,
        sample_count=sample_count,
        analysis_start=analysis_start,
        analysis_end=analysis_end
    )

    with open("raport_ekg.pdf", "rb") as pdf_file:

        st.download_button(
            label="Pobierz raport PDF",
            data=pdf_file,
            file_name="raport_ekg.pdf",
            mime="application/pdf"
        )