import pandas as pd
import streamlit as st


@st.cache_data
def load_exercise_data():

    path = path = "data/ekg/ekg_wysilkowe_AlisaSel.txt"

    with open(path, 'r') as f:
        lines = f.readlines()

    data_start = next(
        i for i, line in enumerate(lines)
        if line.strip().startswith("0,")
    )

    df = pd.read_csv(
        path,
        skiprows=data_start,
        sep=r"\s+",
        header=None,
        names=["czas", "ecg1", "ecg2"],
        engine="python"
    )

    df = df.replace(',', '.', regex=True)

    df = df.astype(float)

    df = df.dropna()

    df = df.rename(
        columns={"ecg1": "ecg"}
    )

    df = df[["czas", "ecg"]]

    df = df.apply(
        pd.to_numeric,
        errors='coerce'
    )

    df = df.dropna()

    return df


@st.cache_data
def load_rest_data():

    path = path = "data/ekg/ekg_spoczynkowe_Alisa.txt"

    with open(path, 'r') as f:
        lines = f.readlines()

    data_start = next(
        i for i, line in enumerate(lines)
        if line.strip().startswith("0,")
    )

    df = pd.read_csv(
        path,
        skiprows=data_start,
        sep=r"\s+",
        header=None,
        names=["czas", "ecg1", "ecg2"],
        engine="python"
    )

    df = df.replace(',', '.', regex=True)

    df = df.astype(float)

    df = df.dropna()

    df = df.rename(
        columns={"ecg1": "ecg"}
    )

    df = df[["czas", "ecg"]]

    df = df.apply(
        pd.to_numeric,
        errors='coerce'
    )

    df = df.dropna()

    return df