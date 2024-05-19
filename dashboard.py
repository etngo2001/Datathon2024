import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def main():
	st.set_page_config(page_title="Applez & Pheesh", page_icon=":cookie:",layout="wide")

	st.title(":chart_with_upwards_trend: Drug Overdose Deathrate Trends :chart_with_downwards_trend:")
	st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

	df = pd.read_csv("cleaned_drug_overdose_deathrate_data.csv", encoding = "ISO-8859-1")

	col1, col2 = st.columns((2))

	with col1:
		start = st.selectbox("From:", df["YEAR"].unique(), 0)

	with col2:
		end_options = list(df["YEAR"].unique())
		end_options = end_options[end_options.index(start):]
		end = st.selectbox("To:", end_options, len(end_options) - 1)

	df = df[(df["YEAR"] >= start) & (df["YEAR"] <= end)].copy()


	st.sidebar.header("Choose your filter: ")

	dynamic_filters = DynamicFilters(df, filters=["DRUG", "SEX", "AGE", "HISPANIC ORIGIN", "RACE"])
	with st.sidebar:
		dynamic_filters.display_filters()

	st.subheader('Time Series Analysis')

	linechart = pd.DataFrame(dynamic_filters.filter_df()).reset_index()
	fig = px.line(linechart, x = "YEAR", y="ESTIMATE", labels = {"ESTIMATE": "Estimate of Deaths (per 100,000 population)"}, height=500, width = 1000, template="gridon")
	st.plotly_chart(fig,use_container_width=True)

	with st.expander("View Data of Time Series:"):
		st.write(linechart.T.style.background_gradient(cmap="Blues"))
		csv = linechart.to_csv(index=False).encode("utf-8")
		st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')
	with st.expander("View Data of Time Series"):
			dynamic_filters.display_df()

# Download orginal DataSet
	csv = df.to_csv(index = False).encode('utf-8')
	st.download_button('Download Full Dataset', data = csv, file_name = "Data.csv",mime = "text/csv")

main()