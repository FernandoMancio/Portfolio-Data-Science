import streamlit as st
import pandas as pd
import plotly.express as px


### page config
st.set_page_config(page_title="Dashboard Titanic", page_icon= ":anchor:",
                   layout="wide")

### dashboard title
st.title(':ship: :blue[_Dashboard Titanic_] :anchor:')
st.markdown("---")

##@st.cache_data

### importing dataset
df = pd.read_excel(r'C:/Users/fmanc/Desktop/Project/Perspective_Analytics/Portfolio/titanic.xlsx')

def fares(df):
    if df["Fare"] <= 8:
        return "1) 0.000 - 8.000"
    elif df["Fare"] <= 15:
        return "2) 8.001 - 15.000"
    elif df["Fare"] <= 32:
        return "3) 15.001 - 32.000"
    else:
        return "4) over 32.001"
df["Fare_Range"] = df.apply(fares, axis=1)

df["Embarked"] = df["Embarked"].fillna("N/A")

### FILTERS
st.sidebar.header("**FILTERS:**")

# sex filter
valores_unicos = sorted(df['Sex'].unique())
options = ["All"] + list(valores_unicos)
filtro_sexo = st.sidebar.multiselect("**Gender**", options, default=options[0])
if len(filtro_sexo) == 0:
    filtro_sexo = ["All"]
if "All" in filtro_sexo and len(filtro_sexo) > 1:
    filtro_sexo.remove("All")
if "All" in filtro_sexo:
    filtro_sexo = list(valores_unicos)

# embarked filter
valores_unicos2 = sorted(df['Embarked'].unique())
options2 = ["All"] + list(valores_unicos2)
filtro_embark = st.sidebar.multiselect("**Embarked in**",options2, default=options2[0])
if len(filtro_embark) == 0:
    filtro_embark = ["All"]
if "All" in filtro_embark and len(filtro_embark) > 1:
    filtro_embark.remove("All")
if "All" in filtro_embark:
    filtro_embark = list(valores_unicos2)


# Fare Range Filter
valores_unicos1 = sorted(df["Fare_Range"].unique())
options1 = ["All"] + list(valores_unicos1)
filtro_fare = st.sidebar.multiselect("**Fare Range**", options1, default=options1[0])
if len(filtro_fare) == 0:
    filtro_fare = ["All"]
if "All" in filtro_fare and len(filtro_fare) > 1:
    filtro_fare.remove("All")
if "All" in filtro_fare:
    filtro_fare = list(valores_unicos1)


# Class Filter
valores_unicos3 = sorted(df["Pclass"].unique())
options3 = ["All"] + list(valores_unicos3)
filtro_class = st.sidebar.multiselect("**Class**", options3, default=options3[0])
if len(filtro_class) == 0:
    filtro_class = ["All"]
if "All" in filtro_class and len(filtro_class) > 1:
    filtro_class.remove("All")
if "All" in filtro_class:
    filtro_class = list(valores_unicos3)

df_selection = df.query("Sex == @filtro_sexo & Embarked == @filtro_embark & \
Fare_Range == @filtro_fare & Pclass == @filtro_class")

with st.sidebar:
    st.container()
    st.write("_By Mâncio_")

### CARDS
col1, col2, col3 = st.columns([3,3,3], gap="large")

# Card1
tot_pass = df_selection.shape[0]
tot_pass1 = f"{tot_pass:,}"
perc = tot_pass / tot_pass
perc = "{:.2%}".format(perc)
col1.metric("**Total Passangers**", tot_pass1,perc, delta_color="off")

# Card2
alive = df_selection["Survived"].value_counts()[1]
perc1 = alive / tot_pass
perc1 = "{:.2%}".format(perc1)
col2.metric("**Total Alive**", alive, perc1)

# Card3
dead = df_selection["Survived"].value_counts()[0]
perc2 = dead / tot_pass * (-1)
perc2 = "{:.2%}".format(perc2)
col3.metric("**Total Dead**", dead, perc2)

with col1:
    st.markdown("---")

with col2:
    st.markdown("---")

with col3:
    st.markdown("---")

st.markdown("---")


### GRAPHS
### Graph1 Title
sex_count = df_selection['Sex'].value_counts().reset_index()
sex_count.columns = ['Sex', 'Count']
fig = px.pie(sex_count, values='Count', names='Sex', color='Sex',
             color_discrete_map={'male': '#4f9cd7', 'female': '#dd7047'}, 
             hole=0.3, 
             labels={'Sex': ''},  # Remover o rótulo do eixo x
             title='Gender Distribution')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=20), width=320, height=320)
col1.plotly_chart(fig)


### Graph2 Title
fig = px.histogram(df_selection, x='Fare', nbins=30, 
                   labels={'Fare': 'Fare', 'count': 'Frequency'},
                   title='Fare Distribution')
fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=30),width=350, height=350,
                  xaxis_title='Fare', yaxis_title='Frequency')
col2.plotly_chart(fig)


### Graph3 Title
embarked_count = df_selection['Embarked'].value_counts().reset_index()
embarked_count.columns = ['Embarked', 'Count']
fig = px.pie(embarked_count, values='Count', names='Embarked', 
             color='Embarked', color_discrete_map={'C': 'green', 'Q': 'orange', 'S': '#6fa8dc'}, 
             hole=0.3, 
             labels={'Embarked': ''},  # Remover o rótulo do eixo x
             title='Embarked Distribution')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=20), width=320, height=320)
col3.plotly_chart(fig)

try:
    st.markdown("**DATASET**")
    st.dataframe(df_selection)
except:
    st.dataframe(df)

    
