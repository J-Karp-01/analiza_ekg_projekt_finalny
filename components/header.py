import streamlit as st


def render_header(
    bialy,
    lekki_szary,
    lekki_czerwony,
    mocny_szary
):

    st.markdown(f"""
        <style>

        .stApp {{
            color: {bialy};
        }}

        h1, h2, h3, [data-testid="stHeader"] {{
            color: {bialy} !important;
        }}

        p, .stText, [data-testid="stWidgetLabel"] {{
            color: {bialy};
            font-size: 16px;
        }}

        [data-testid="stMetricValue"] {{
            font-size: 18px !important;
            color: {bialy} !important;
        }}

        [data-testid="stMetricLabel"] p {{
            color: {mocny_szary} !important;
        }}

        .moja-ramka {{

            border-radius: 10px;
            padding: 20px;
            background-color: {lekki_szary};
            text-align: center;
            height: 120px;
        }}

        .moja-ramka h4 {{
            color: {lekki_czerwony};
            margin: 0;
        }}

        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="moja-ramka">
            <h4>Analiza HRV sygnału EKG</h4>
            <p style="color: {bialy};">
                Zaawansowane laboratorium fizyki medycznej
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <hr style="
            margin-top: 10px;
            height:5px;
            border:none;
            color:{lekki_szary};
            background-color:#444444;"
        />
    """, unsafe_allow_html=True)
