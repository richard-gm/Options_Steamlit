import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import matplotlib.pyplot as plt

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")


@st.cache(allow_output_mutation=True)
def get_Options_data():

    df = pd.read_csv("Data/Option.csv")
    # print(df)
    return df

try:
        st.title('Options breakdown')
        df = get_Options_data()
        # Cleaning Data:
        df[df.Symbol.notnull()]
        df['Unrealized Credit Received'] = df['Unrealized Credit Received'].str.replace('$', '').astype(float)
        df['Realized Credit'] = df['Realized Credit'].str.replace('$', '').astype(float)
        # Grouping UNREALIZED COLUMN by Symbol and Adding calculations:
        df_unrealized = df.groupby('Symbol')['Unrealized Credit Received'].agg(['min', 'max', 'sum', 'count'])
        df_unrealized.sort_values(by='sum', ascending=False, inplace=True)
        df_unrealized.reset_index(inplace=True)
        # Display RAW data:

        c = alt.Chart(df_unrealized).mark_circle().encode(
            x='count', y='sum', size='count', color='Symbol', tooltip=['count', 'sum', 'Symbol'])
        st.altair_chart(c, use_container_width=True)
        df2_unrealized = df_unrealized.dropna()
        # Display RAW data:
        values = st.slider(
                 'Select a range of values',
                         0.0, 100.0, (25.0, 75.0))
        st.write('Values:', values)

except URLError as e:
    st.error(
            """
            **This demo requires internet access.**    
            Connection error: %s
        """
        % e.reason
    )


#
#
#     csv = convert_df(my_large_df)
