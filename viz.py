import streamlit as st
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import io
from io import StringIO, BytesIO
import base64

from PIL import Image
st.set_page_config(layout="wide")
st.write(" ## Testing Plot Generation and Exports for PA-X Data")

df=pd.read_csv("data/pax.csv")
#extract year from date
df['Dat']=pd.to_datetime(df['Dat'])
df['year']=pd.DatetimeIndex(df['Dat']).year

#groupby x axis value
groupby_options=["year", "stage_label", "agt_type", "Reg", "Con"]

#button for groupby options
selected_x=st.selectbox("Show the number of agreements in PA-X database by:", groupby_options)

grouped_df=df.groupby(selected_x)
nr_agts=pd.DataFrame(grouped_df['AgtId'].nunique()).rename(columns={'AgtId':'Nr Agts'}).reset_index()


fig = px.bar(nr_agts, x=selected_x, y="Nr Agts", text_auto=True)
Logo = Image.open("data/PeaceRep-Logo-480x151.png")

fig.add_layout_image(
    dict(
        source=Logo,  x=0.95, y=1.0,
        sizex=0.1, sizey=0.1,
        xref="paper", yref="paper",
        xanchor="right", yanchor="bottom"
    )
)
fig.update_layout(
    width=1280,
    height=720,
    title=("PA-X Peace Agreements Database<br>" +
           "<i>Number of Agreements</i>"),
)
fig.update_traces(marker_color='rgb(9, 31, 64)')

#fig.show()

st.plotly_chart(fig)

#export=fig.write_image('peacerep_chart.png')

#st.download_button(label="Download as a PNG", data=export)

st.write(nr_agts)


mybuff = StringIO()
fig.write_html(mybuff, include_plotlyjs='cdn')
mybuff = BytesIO(mybuff.getvalue().encode())
b64 = base64.b64encode(mybuff.read()).decode()
href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download chart as HTML</a>'
st.markdown(href, unsafe_allow_html=True)

# Convert the Plotly figure to PNG format
img_bytes = pio.to_image(fig, format="png")
    
# Provide a download link for the PNG image
b64 = base64.b64encode(img_bytes).decode()
href = f'<a href="data:image/png;base64,{b64}" download="plot.png">Download chart as PNG</a>'
st.markdown(href, unsafe_allow_html=True)


csv = nr_agts.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to base64
href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download data as CSV</a>'
st.markdown(href, unsafe_allow_html=True)
