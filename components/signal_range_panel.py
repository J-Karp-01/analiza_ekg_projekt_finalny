import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render_signal_range_panel(
    df,
    bialo_szary,
    lekki_czerwony
):

    col1, col2, col3 = st.columns([2.0, 1.5, 5])

    with col1:

        st.dataframe(
            df,
            height=265,
            use_container_width=True
        )

    with col2:

        min_czas = float(df['czas'].min())
        max_czas = float(df['czas'].max())

        zakres_czasu = st.slider(
            "Wybierz zakres czasu do analizy [s]:",
            min_value=min_czas,
            max_value=max_czas,
            value=(min_czas, max_czas),
            step=0.1
        )

        df_stary = df.copy()

        df = df[
            (df['czas'] >= zakres_czasu[0]) &
            (df['czas'] <= zakres_czasu[1])
        ].copy()

        ile_zostalo = len(df)

        ile_wycieto = len(df_stary) - ile_zostalo

        dane_pie = {
            "Status": [
                "Fragment do analizy",
                "Pozostała część"
            ],
            "Liczba próbek": [
                ile_zostalo,
                ile_wycieto
            ]
        }

        fig_pie = px.pie(
            dane_pie,
            values='Liczba próbek',
            names='Status',
            hole=0.4,
            color_discrete_sequence=[
                '#e74c3c',
                '#7e7e7e'
            ]
        )

        fig_pie.update_layout(
            height=200,
            margin=dict(
                l=20,
                r=20,
                t=0,
                b=20
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    with col3:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_stary['czas'],
            y=df_stary['ecg'],
            mode='lines',
            name='Pozostała część',
            line=dict(
                color=bialo_szary,
                width=2
            )
        ))

        fig.add_trace(go.Scatter(
            x=df['czas'],
            y=df['ecg'],
            mode='lines',
            name='Fragment do analizy',
            line=dict(
                color=lekki_czerwony,
                width=3
            )
        ))

        fig.update_layout(
            height=230,
            margin=dict(
                l=0,
                r=0,
                t=10,
                b=0
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            ),
            xaxis_title="Czas [s]",
            yaxis_title="Amplituda [mV]"
        )

        with st.container(border=True):

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.markdown("""
        <hr style="margin-top: -10px;height:5px; border:none; color:#444444; background-color:#444444;" />
    """, unsafe_allow_html=True)

    return df