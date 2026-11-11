from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="London Property Pulse Pro",page_icon="🏙️",layout="wide",initial_sidebar_state="expanded")
ROOT=Path(__file__).resolve().parent
PURPLE="#E2A76F"; TEAL="#39C7E6"; BLUE="#638BFF"; GOLD="#F0C77B"
COLORS=[TEAL,BLUE,PURPLE,GOLD]
COORDS={
"Barking and Dagenham":(51.537,0.080),"Barnet":(51.625,-0.151),"Bexley":(51.456,0.146),"Brent":(51.559,-0.281),
"Bromley":(51.405,0.015),"Camden":(51.542,-0.143),"Croydon":(51.372,-0.101),"Ealing":(51.513,-0.308),
"Enfield":(51.653,-0.081),"Greenwich":(51.482,0.005),"Hackney":(51.545,-0.055),
"Hammersmith and Fulham":(51.492,-0.225),"Haringey":(51.590,-0.110),"Harrow":(51.579,-0.337),
"Havering":(51.581,0.183),"Hillingdon":(51.544,-0.476),"Hounslow":(51.468,-0.361),
"Islington":(51.541,-0.103),"Kensington and Chelsea":(51.503,-0.192),"Kingston upon Thames":(51.409,-0.306),
"Lambeth":(51.457,-0.121),"Lewisham":(51.462,-0.009),"Merton":(51.411,-0.190),
"Newham":(51.530,0.031),"Redbridge":(51.559,0.074),"Richmond upon Thames":(51.447,-0.326),
"Southwark":(51.503,-0.080),"Sutton":(51.361,-0.194),"Tower Hamlets":(51.520,-0.029),
"Waltham Forest":(51.590,-0.014),"Wandsworth":(51.456,-0.191),"Westminster":(51.498,-0.135)}
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 85% 4%,rgba(35,113,175,.17),transparent 32%),#090F1B;color:#F4F7FF}
[data-testid="stHeader"]{background:rgba(9,15,27,.92)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#13243A,#0B1728);border-right:1px solid #2E4A60}
[data-testid="stSidebar"] *{color:#E5E9FF}
.block-container{max-width:1540px;padding-top:1.6rem}
.hero{padding:32px 36px;border-radius:21px;background:radial-gradient(circle at 87% 16%,rgba(57,199,230,.19),transparent 31%),linear-gradient(110deg,#173A58,#16324E 65%,#155A67);border:1px solid #3B6A7E;margin-bottom:16px}
.hero h1{font-size:2.6rem;font-weight:800;letter-spacing:-.055em;color:white;margin:10px 0 6px}
.hero p{color:#DCE6F6;font-size:.98rem;margin:0}
.kicker{color:#81E6F8;font-size:.75rem;letter-spacing:.17em;font-weight:800}
.pill{display:inline-block;background:#16364C;border:1px solid #34768C;border-radius:30px;padding:6px 12px;color:#C3F4FF;font-size:.76rem;margin:0 8px 12px 0}
[data-testid="stMetric"]{background:linear-gradient(140deg,#1B344D,#14283D);border:1px solid #38546D;border-radius:16px;padding:17px;box-shadow:0 12px 24px rgba(0,0,0,.12)}
[data-testid="stMetricLabel"]{color:#C7D0E9!important}
[data-testid="stMetricValue"]{color:#FFFFFF!important;font-weight:800}
[data-testid="stMetricDelta"]{color:#7BE8D9}
div[data-testid="stPlotlyChart"]{border:1px solid #344D65;border-radius:17px;background:linear-gradient(130deg,#182E45,#12253B);padding:10px}
h2,h3{color:#F7F8FF!important;letter-spacing:-.035em}
[data-testid="stWidgetLabel"] p, label p{color:#DFE6FA!important}
[data-testid="stAlert"]{color:#F5E3AE}
[data-baseweb="select"]>div{background:#1D354D!important;color:#F4F7FF!important}
[data-baseweb="tag"]{background:#245A76!important}

/* Sidebar controls and buttons: strong contrast across themes */
[data-testid="stSidebar"] [data-testid="stLinkButton"] a,
[data-testid="stSidebar"] a[kind="primary"],
[data-testid="stSidebar"] button[kind="primary"]{
 background:#267FA2!important;color:#FFFFFF!important;border:1px solid #61BEDA!important;
 font-weight:700!important;border-radius:10px!important;
}
[data-testid="stSidebar"] [data-testid="stLinkButton"] a:hover,
[data-testid="stSidebar"] a[kind="primary"]:hover{background:#3298BB!important;color:#FFFFFF!important}
[data-testid="stSidebar"] [data-testid="stLinkButton"] a *{color:#FFFFFF!important}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#DDEBFA!important}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{color:#B3C7D9!important}
[data-baseweb="popover"],[data-baseweb="menu"]{background:#1B3148!important;color:#FFFFFF!important}
[data-baseweb="menu"] li{color:#F4F7FF!important}
[data-baseweb="menu"] li:hover{background:#2C526C!important}
[data-testid="stSidebar"] [data-baseweb="select"] input{color:#FFFFFF!important}
footer{visibility:hidden}
</style>""",unsafe_allow_html=True)

@st.cache_data
def load():
    return pd.read_csv(ROOT/"data"/"london_house_prices_synthetic.csv")

def chart(fig,height=350):
    fig.update_layout(template="plotly_dark",height=height,margin=dict(l=12,r=12,t=20,b=10),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E1E9FA",family="DM Sans"),legend_title_text="",
        colorway=COLORS)
    fig.update_xaxes(showgrid=False,zeroline=False)
    fig.update_yaxes(gridcolor="rgba(220,230,255,.12)",zeroline=False)
    st.plotly_chart(fig,use_container_width=True)

df=load()
st.sidebar.markdown("## ◈ Property Pulse")
st.sidebar.caption("LONDON HOUSING INTELLIGENCE")
st.sidebar.divider()
view=st.sidebar.radio("Explore",["Executive overview","London price map","Affordability explorer","Borough comparison","Data & methodology"])
st.sidebar.divider()
years=st.sidebar.slider("Year range",int(df.year.min()),int(df.year.max()),(2018,2026))
property_types=st.sidebar.multiselect("Property types",sorted(df.property_type.unique()),default=sorted(df.property_type.unique()))
boroughs=st.sidebar.multiselect("Boroughs",sorted(df.borough.unique()),default=sorted(df.borough.unique()))
st.sidebar.divider()
st.sidebar.caption("⚠ SYNTHETIC DATA · EDUCATIONAL DEMO")
st.sidebar.markdown("**Portfolio**")
st.sidebar.link_button("↗ Open GitHub profile","https://github.com/diegoallanalves",use_container_width=True,type="primary")
d=df[df.year.between(*years)&df.property_type.isin(property_types)&df.borough.isin(boroughs)].copy()
if d.empty:
    st.info("Select at least one borough and property type.");st.stop()
last_year=int(d.year.max())
latest=d[d.year==last_year].copy()
st.markdown("""<div class="hero"><div class="kicker">◈ LONDON PROPERTY PULSE / ANALYTICS STUDIO</div>
<h1>Discover London's<br>property landscape.</h1>
<p>Explore house prices, compare boroughs and investigate affordability with interactive visual analytics.</p></div>
<div><span class="pill">● Synthetic demo</span><span class="pill">▣ Borough intelligence</span><span class="pill">◇ Interactive maps</span><span class="pill">✦ Affordability insights</span></div>""",unsafe_allow_html=True)
st.caption("Illustrative synthetic data only. Borough markers use approximate centre coordinates, not actual property locations. No real market statistics are represented.")
median=latest.median_price_gbp.median()
ratio=latest.price_to_earnings_ratio.median()
a,b,c,e=st.columns(4)
a.metric("Synthetic median price",f"£{median:,.0f}")
b.metric("Price-to-earnings",f"{ratio:.1f}×")
c.metric("Boroughs selected",f"{latest.borough.nunique()}")
e.metric("Simulated transactions",f"{int(latest.transactions.sum()):,}")

if view=="Executive overview":
    left,right=st.columns([1.5,1])
    with left:
        st.subheader("House price evolution")
        trend=d.groupby(["year","property_type"],as_index=False).median_price_gbp.median()
        fig=px.line(trend,x="year",y="median_price_gbp",color="property_type",markers=True,
            color_discrete_sequence=COLORS,labels={"median_price_gbp":"Median price (£)","property_type":"Property type","year":"Year"})
        fig.update_traces(line=dict(width=3))
        chart(fig)
    with right:
        st.subheader("Property mix")
        mix=latest.groupby("property_type",as_index=False).transactions.sum()
        fig=px.pie(mix,names="property_type",values="transactions",hole=.66,color_discrete_sequence=COLORS)
        fig.update_traces(marker=dict(line=dict(color="#172038",width=3)))
        chart(fig)
    st.subheader("London price hotspots")
    geo=latest.groupby("borough",as_index=False).agg(median_price_gbp=("median_price_gbp","median"),transactions=("transactions","sum"))
    geo["lat"]=geo.borough.map(lambda x:COORDS.get(x,(None,None))[0])
    geo["lon"]=geo.borough.map(lambda x:COORDS.get(x,(None,None))[1])
    fig=px.scatter_map(geo,lat="lat",lon="lon",size="transactions",color="median_price_gbp",
        hover_name="borough",hover_data={"median_price_gbp":":,.0f","transactions":True,"lat":False,"lon":False},
        color_continuous_scale=["#39C7E6","#638BFF","#E2A76F","#F0C77B"],zoom=8.8,center={"lat":51.51,"lon":-0.12},
        map_style="carto-darkmatter",size_max=30,labels={"median_price_gbp":"Median price (£)"})
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0),height=480,font_color="#F1F7FF",paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig,use_container_width=True)
elif view=="London price map":
    st.subheader("Interactive London borough map")
    metric=st.radio("Colour markers by",["Median property price","Price-to-earnings ratio"],horizontal=True)
    geo=latest.groupby("borough",as_index=False).agg(median_price_gbp=("median_price_gbp","median"),
        price_to_earnings_ratio=("price_to_earnings_ratio","median"),transactions=("transactions","sum"))
    geo["lat"]=geo.borough.map(lambda x:COORDS.get(x,(None,None))[0])
    geo["lon"]=geo.borough.map(lambda x:COORDS.get(x,(None,None))[1])
    key="median_price_gbp" if metric=="Median property price" else "price_to_earnings_ratio"
    fig=px.scatter_map(geo,lat="lat",lon="lon",color=key,size="transactions",hover_name="borough",
        hover_data={"median_price_gbp":":,.0f","price_to_earnings_ratio":":.1f","transactions":True,"lat":False,"lon":False},
        color_continuous_scale=["#39C7E6","#638BFF","#E2A76F","#F0C77B"],size_max=36,
        zoom=9,center={"lat":51.51,"lon":-0.12},map_style="carto-darkmatter",
        labels={"median_price_gbp":"Median price (£)","price_to_earnings_ratio":"Price / earnings"})
    fig.update_layout(height=650,margin=dict(l=0,r=0,t=0,b=0),font_color="#F1F7FF",paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig,use_container_width=True)
    st.info("Each circle marks an approximate borough centre. Circle size represents synthetic transaction counts. This is a point map, not a borough boundary choropleth.")
    st.dataframe(geo.drop(columns=["lat","lon"]).sort_values(key,ascending=False),hide_index=True,use_container_width=True)
elif view=="Affordability explorer":
    st.subheader("Price-to-earnings intelligence")
    t=latest.groupby("borough",as_index=False).agg(price_to_earnings_ratio=("price_to_earnings_ratio","median"),
        median_price_gbp=("median_price_gbp","median")).sort_values("price_to_earnings_ratio")
    fig=px.bar(t,x="price_to_earnings_ratio",y="borough",orientation="h",color="price_to_earnings_ratio",
        color_continuous_scale=["#39C7E6","#638BFF","#E2A76F","#F0C77B"],labels={"price_to_earnings_ratio":"Price / annual earnings","borough":""})
    fig.update_layout(coloraxis_showscale=False)
    chart(fig,max(460,28*len(t)+90))
    st.subheader("Illustrative affordability calculator")
    x,y,z=st.columns(3)
    with x: salary=st.number_input("Annual household income (£)",min_value=10000,max_value=500000,value=55000,step=5000)
    with y: deposit=st.slider("Deposit (%)",5,50,20)
    with z: mortgage_multiple=st.slider("Illustrative lending multiple",2.0,6.0,4.5,0.5)
    borrowing=salary*mortgage_multiple
    budget=borrowing/(1-deposit/100)
    st.metric("Illustrative property budget",f"£{budget:,.0f}")
    st.caption("Simplified example only: no taxes, fees, credit assessment, interest or lender underwriting. Not financial advice.")
elif view=="Borough comparison":
    st.subheader("Compare boroughs")
    opts=sorted(latest.borough.unique())
    defaults=[v for v in ["Camden","Hackney","Croydon","Westminster"] if v in opts]
    selected=st.multiselect("Boroughs to compare",opts,default=defaults or opts[:4])
    sub=latest[latest.borough.isin(selected)]
    if sub.empty:st.info("Select boroughs above.")
    else:
        comp=sub.groupby(["borough","property_type"],as_index=False).median_price_gbp.median()
        fig=px.bar(comp,x="borough",y="median_price_gbp",color="property_type",barmode="group",
            color_discrete_sequence=COLORS,labels={"median_price_gbp":"Median price (£)","borough":"Borough"})
        chart(fig,440)
        st.dataframe(comp,use_container_width=True,hide_index=True)
elif view=="Data & methodology":
    st.subheader("Dataset explorer")
    st.write(f"**{len(d):,} filtered records** · **{d.year.min()}–{d.year.max()}** · **{d.borough.nunique()} boroughs**")
    x,y,z=st.columns(3)
    x.metric("Missing cells",f"{int(d.isna().sum().sum()):,}")
    y.metric("Duplicate rows",f"{int(d.duplicated().sum()):,}")
    z.metric("Property types",str(d.property_type.nunique()))
    st.dataframe(d,use_container_width=True,hide_index=True)
    st.markdown("""#### Definitions and limitations
- Each row is a **synthetic borough–year–property type aggregate**, not a transaction record.
- `median_price_gbp` and `median_annual_earnings_gbp` are fictional illustrative figures.
- `price_to_earnings_ratio` is the ratio of those two figures.
- `transactions` is a simulated count.
- `annual_change_pct` is a model trend parameter, **not** a calculated observed year-on-year change.
- Map coordinates represent approximate borough centres; they are not precise geographical boundaries.
- The data must not be cited as actual London housing evidence.""")
st.download_button("⬇ Download filtered synthetic CSV",d.to_csv(index=False).encode("utf-8"),
    file_name="london_property_pulse_filtered_demo.csv",mime="text/csv")
st.divider()
st.caption("London Property Pulse Pro · Independent demonstration · Streamlit + Plotly · Synthetic data only")
