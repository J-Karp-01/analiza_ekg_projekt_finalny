import streamlit as st


def render_header(
    bialy,
    lekki_szary,
    lekki_czerwony,
    mocny_szary
):

    st.markdown(f"""
        <style>
                
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

            html, body, [class*="css"], [class*="st-"] {{
                font-family: 'Poppins', sans-serif !important;
            }}

            h1, h2, h3, h4, h5, h6 {{
                font-family: 'Poppins', sans-serif !important;
            }}

                
        .stApp {{
            color: {bialy};
        }}

        h2, h3, [data-testid="stHeader"] {{
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

        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #161b22, #1e293b);
        border-radius: 18px;
        padding: 38px;
        text-align: center;
        border: 1px solid rgba(56,189,248,0.18);
        box-shadow: 0 0 25px rgba(56,189,248,0.08);
        margin-bottom: 18px;
    ">

    <h1 style="
        color:#00e5ff;
        margin:0;
        font-size:38px;
        font-weight:500;
        letter-spacing:0.3px;
    ">
    Analiza HRV sygnału EKG oraz Synchronizacja sercowowo oddechowa
    </h1>

    <p style="
        color:#00e5ff;
        font-size:18px;
        margin-top:14px;
        margin-bottom:4px;
    ">
    Zaawansowane laboratorium Fizyki Medycznej
    </p>

    <p style="
        color:#00e5ff;
        font-size:14px;
        margin:0;
    ">
    Jolanta Karp
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
