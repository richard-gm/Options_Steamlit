import streamlit as st
import pandas as pd
import altair as alt
import plotly.figure_factory as ff


# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def get_Options_data():

    df = pd.read_csv("Data/Option.csv")
    # print(df)
    return df

try:
    df = get_Options_data()
    # Cleaning Data:
    df[df.Symbol.notnull()]
    df['Unrealized Credit Received'] = df['Unrealized Credit Received'].str.replace('$', '').astype(float)
    df['Realized Credit'] = df['Realized Credit'].str.replace('$', '').astype(float)
    # Grouping UNREALIZED COLUMN by Symbol and Adding calculations:
    df_unrealized = df.groupby('Symbol')['Unrealized Credit Received'].agg(['min', 'max', 'sum','count'])
    df_unrealized.sort_values(by='sum',ascending=False, inplace=True)
    df_unrealized.reset_index(inplace=True)
    # Display RAW data:
    df_realized = df.groupby('Symbol')['Realized Credit'].agg(['min', 'max', 'sum','count'])
    df_realized.sort_values(by='sum',ascending=False, inplace=True)

    c = alt.Chart(df_unrealized).mark_circle().encode(
        x='count', y='sum', size='count', color='Symbol', tooltip=['count', 'sum', 'Symbol'])
    st.altair_chart(c, use_container_width=True)

    # Display RAW data:
    x1 = df_unrealized.loc['sum']
    x2 = df_unrealized.loc['min']
    x3 = df_unrealized.loc['max']

    # Group data together
    hist_data = [x1, x2, x3]

    group_labels = ['Group Sum', 'Group Min', 'Group Max']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
               hist_data, group_labels, bin_size=[.1, .25, .5])

    # Plot!
    st.plotly_chart(fig, use_container_width=True)



#     ticket = st.multiselect(
#         "Choose ticket", list(df_unrealized.index), ["JMIA", "ASTR"]
#     )
    # if not ticket:
    #     st.error("Please select at least one country.")
    # else:
    #     data = df_unrealized.loc[ticket]
    #     data /= 1000000.0
    #     st.write("### Gross Agricultural Production ($B)", data.sort_index())
    #
    #     data = data.T.reset_index()
    #     data = pd.melt(data, id_vars=["index"]).rename(
    #         columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    #     )
        # chart = (
        #     alt.Chart(data)
        #         .mark_area(opacity=0.3)
        #         .encode(
        #         x="year:T",
        #         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
        #         color="Region:N",
        #     )
        # )
        # st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )