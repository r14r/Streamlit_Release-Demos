import streamlit as st
import altair as alt
import inspect
from vega_datasets import data

@st.experimental_memo
def get_chart_67358(use_container_width: bool):
    import altair as alt
    from vega_datasets import data
    
    source = data.seattle_weather()
    
    scale = alt.Scale(domain=['sun', 'fog', 'drizzle', 'rain', 'snow'],
                      range=['#e7ba52', '#a7a7a7', '#aec7e8', '#1f77b4', '#9467bd'])
    color = alt.Color('weather:N', scale=scale)
    
    # We create two selections:
    # - a brush that is active on the top panel
    # - a multi-click that is active on the bottom panel
    brush = alt.selection_interval(encodings=['x'])
    click = alt.selection_multi(encodings=['color'])
    
    # Top panel is scatter plot of temperature vs time
    points = alt.Chart().mark_point().encode(
        alt.X('monthdate(date):T', title='Date'),
        alt.Y('temp_max:Q',
            title='Maximum Daily Temperature (C)',
            scale=alt.Scale(domain=[-5, 40])
        ),
        color=alt.condition(brush, color, alt.value('lightgray')),
        size=alt.Size('precipitation:Q', scale=alt.Scale(range=[5, 200]))
    ).properties(
        width=550,
        height=300
    ).add_selection(
        brush
    ).transform_filter(
        click
    )
    
    # Bottom panel is a bar chart of weather type
    bars = alt.Chart().mark_bar().encode(
        x='count()',
        y='weather:N',
        color=alt.condition(click, color, alt.value('lightgray')),
    ).transform_filter(
        brush
    ).properties(
        width=550,
    ).add_selection(
        click
    )
    
    chart = alt.vconcat(
        points,
        bars,
        data=source,
        title="Seattle Weather: 2012-2015"
    )
    
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])
    
    with tab1:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    with tab2:
        st.altair_chart(chart, theme=None, use_container_width=True)

try:
    st.expander("See code").code(inspect.getsource(get_chart_67358))
    get_chart_67358(use_container_width=True)
except Exception as e:
    st.exception(e)

