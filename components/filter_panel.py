import streamlit as st


def render_filter_panel(
    lekki_czerwony
):

    col1, col2 = st.columns([2, 7])

    with col1:

        st.markdown("###### Filtrowanie")

        st.markdown(f"""
            <div style="background-color: {lekki_czerwony};
                border-radius: 10px;
                padding: 40px;
                margin-bottom: -420px;
                height: 270px;
                border: 0px solid rgba(100,100,100,1);
            ">
            </div>
        """, unsafe_allow_html=True)

        lewy, srodek, prawy = st.columns([0.1, 0.8, 0.1])

        with srodek:

            window_length = st.slider(
                "Długość okna filtra:",
                min_value=1,
                max_value=102,
                value=43,
                step=1
            )

            polyorder = st.slider(
                "Stopień wielomianu:",
                min_value=1,
                max_value=6,
                value=2,
                step=1
            )

    return col2, window_length, polyorder