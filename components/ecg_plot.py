import streamlit as st
import plotly.graph_objects as go


def render_ecg_plot(
    df,
    col2,
    lekki_czerwony
):

    with col2:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df['czas'],
            y=df['ecg'],
            mode='lines',
            name='Surowy',
            line=dict(
                color='rgba(52, 152, 219, 0.5)',
                width=1
            )
        ))

        fig.add_trace(go.Scatter(
            x=df['czas'],
            y=df['ecg_filtrowany'],
            mode='lines',
            name='Savgol Filter',
            line=dict(
                color=lekki_czerwony,
                width=3
            )
        ))

        fig.update_layout(
            height=232,
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

        st.markdown("###### Filtracja sygnału")

        with st.container(border=True):

            st.plotly_chart(
                fig,
                use_container_width=True
            )