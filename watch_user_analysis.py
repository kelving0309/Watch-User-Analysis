import pandas as pd
import plotly.express as px
import streamlit as st
import os
import toml
import numpy as np
import warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Watch User Analysis", page_icon=":bar_chart:", layout="wide")
st.title("Watch User Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)



df = pd.read_csv("All watch users.csv")

# clean and prepare data
df = df.drop(columns=['ID','Serial', 'Name'])
df['dateTimeCreated'] = pd.to_datetime(df['dateTimeCreated'])
df['date'] = df['dateTimeCreated'].dt.date
df['date_month'] = df['dateTimeCreated'].dt.to_period('M')

df = df.dropna(subset=['date', 'date_month'])
pivot_df = df.pivot_table(index='date_month', columns='Model', aggfunc='size', fill_value=0)
#filtered_device_count = pivot_df.drop(pivot_df.index[0])





# WATCH USER REGISTRATION OVER MONTHS

pivot_df.index = pivot_df.index.astype(str)
# Drop the first row
filtered_device_count = pivot_df.iloc[1:]

columns_to_plot = ['rev2', 'rev3', 'revx5']

# Create a line plot using Plotly Express
fig = px.line(filtered_device_count, x=filtered_device_count.index, y=columns_to_plot,
              labels={'value': 'No. of Devices Registered', 'index': 'Month'},
              title='Monthly Count of Devices Registered')

# Customize layout
fig.update_layout(
    xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
    legend_title='Device Type',  # Set legend title
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),  # Adjust legend position
    xaxis=dict(title='Month', showgrid=False),  # Hide gridlines on x-axis
    yaxis=dict(title='No. of Devices Registered', showgrid=False),  # Show gridlines on y-axis
    plot_bgcolor='white',  # Set plot background color
    autosize = False,
    margin=dict(t=100, l=100, r=100, b=100)  # Adjust margin
)

# Show the plot in Streamlit
st.markdown(
    "<div style='display: flex; justify-content: center;'>"
    "<div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')



# WATCH USERS UPGRADED FROM PREVIOUS MODEL

upgrade_df = {
    'Product': ['v2', 'v3', 'x5'],
    'Total_Users': [38602, 64948, 13847],  # Replace None with the total number of x5 users
    'Upgraded_From_Previous': [None, 9618, 6808]  # Replace None with the number of v2 users
}

upgrade_df = pd.DataFrame(upgrade_df)

# Create a bar chart for total users
fig1 = go.Figure()

# Add bars for total users
fig1.add_trace(go.Bar(
    x=upgrade_df['Product'],
    y=upgrade_df['Total_Users'],
    name='Total Users',
    marker=dict(color='rgba(100, 149, 237, 1)'),
    width=0.4  # Set the width of the bars to 0.4

))

# Add faded overlay bars for upgraded users
fig1.add_trace(go.Bar(
    x=upgrade_df['Product'],
    y=upgrade_df['Upgraded_From_Previous'],
    name='Upgraded Users',
    marker=dict(color='rgba(255, 99, 71, 0.3)'),
    width=0.4,  # Set the width of the bars to 0.4
    offset=-0.1  # Move the overlay bar slightly to the left
))

# Update layout
fig1.update_layout(
    title='Number of Users and which Upgraded from Previous Model',
    xaxis_title='Device',
    yaxis_title='Number of Users',
    legend=dict(x=0.7, y=1.0,  # Set the x and y position of the legend box
                bgcolor='rgba(255, 255, 255, 0)',  # Set the background color of the legend box to transparent
                bordercolor='rgba(255, 255, 255, 0)'  # Set the border color of the legend box to transparent
               ),
    xaxis=dict(showgrid=False),  # Hide grid lines on x-axis
    yaxis=dict(showgrid=False),  # Hide grid lines on y-axis
    width = 500,
    height= 400
)




# NUMBER OF USERS UPLOADED A ROUND

# read in rounds df
df_rounds = pd.read_csv("All rounds.csv")

data = {
    'Device': ['v2', 'v3', 'x5'],
    'Total_Users': [38602, 64948, 13847],
    'Users_With_Round': [26179, 50022, 10856]
}

# Calculate the percentage of users with a round
data['Percentage_With_Round'] = [round(uw / tu * 100, 2) for uw, tu in zip(data['Users_With_Round'], data['Total_Users'])]

# Create figure
fig2 = go.Figure()

# Add bars for total users
fig2.add_trace(go.Bar(
    x=data['Device'],
    y=data['Total_Users'],
    name='Total Users',
    marker=dict(color='rgba(100, 149, 237, 1)'),
    width=0.4  # Set the width of the bars to 0.4
))

# Add faded overlay bars for users with rounds
fig2.add_trace(go.Bar(
    x=data['Device'],
    y=data['Users_With_Round'],
    name='Users with Round',
    marker=dict(color='rgba(255, 99, 71, 0.3)'),
    width=0.4,  # Set the width of the bars to 0.4
    offset=-0.1  # Move the overlay bar slightly to the left
))

# Update layout
fig2.update_layout(
    title='Number of Users and Users who Uploaded a Round',
    xaxis_title='Device',
    yaxis_title='Number of Users',
    legend=dict(x=0.7, y=1.0,  # Set the x and y position of the legend box
                bgcolor='rgba(255, 255, 255, 0)',  # Set the background color of the legend box to transparent
                bordercolor='rgba(255, 255, 255, 0)'  # Set the border color of the legend box to transparent
               ),
    xaxis=dict(showgrid=False),  # Hide grid lines on x-axis
    yaxis=dict(showgrid=False),  # Hide grid lines on y-axis
    width = 500,
    height= 400
)


left, right = st.columns(2)
with left:
    st.plotly_chart(fig1)
with right:
    st.plotly_chart(fig2)

st.markdown('---')





# HOW MANY USERS SWITCHED BACK TO V3

total_users = 6808
users_count = 605

# Calculate the percentage of users
percentage = (users_count / total_users) * 100

# Create a gauge chart
metric_fig = go.Figure(data=[go.Pie(labels=['Users using V3 after X5', 'User who bought V3 and X5'],
                             values=[users_count, total_users - users_count],
                             hole=0.5)])

# Add title
metric_fig.update_layout(title_text='Users who uploaded a round with V3 after using X5')

st.markdown(
    "<div style='display: flex; justify-content: center;'>"
    "<div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)
st.plotly_chart(metric_fig, use_container_width=True)

st.markdown('---')


# DROP OFF RATE PER DEVICE

df_drop_off_per_device = df_rounds.groupby(['UserID', 'ProductType']).agg(
    number_of_rounds=('UserID', 'size'),  # Count the total number of rounds
    number_of_signed_off_rounds=('SignedOff', lambda x: (x == 1).sum())  # Count the signed-off rounds
).reset_index()

users_count_per_device = df_drop_off_per_device.groupby(['number_of_rounds', 'ProductType'])['UserID'].nunique().reset_index().rename(columns={'UserID': 'number_of_users'})
users_count_per_device['ProductType'] = users_count_per_device['ProductType'].replace({
    1: 'V1',
    2: 'V2',
    3: 'V3',
    4: 'H4',
    8: 'X5',
    12: 'V5'
})

# Line plot
fig = px.line(users_count_per_device, x='number_of_rounds', y='number_of_users', color='ProductType', 
              labels={'number_of_rounds': 'Number of Rounds Uploaded', 'number_of_users': 'Number of Users'},
              title='Number of Users vs Number of Rounds Uploaded')

fig.update_xaxes(range=[0, 200])

# Show plot

st.markdown(
    "<div style='display: flex; justify-content: center;'>"
    "<div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')


# CREATE BOX PLOTS FOR NUMBER OF ROUNDS FOR EACH DEVICE

# get dropoff data for each device
v2_dropoff = df_drop_off_per_device[df_drop_off_per_device['ProductType'] == 2]
v2_dropoff = v2_dropoff.drop(columns=['ProductType'])

v3_dropoff = df_drop_off_per_device[df_drop_off_per_device['ProductType'] == 3]
v3_dropoff = v3_dropoff.drop(columns=['ProductType'])


x5_dropoff = df_drop_off_per_device[df_drop_off_per_device['ProductType'] == 8]
x5_dropoff = x5_dropoff.drop(columns=['ProductType'])

col1, col2, col3 = st.columns(3)
with col1:
    fig = px.box(v2_dropoff, y=v2_dropoff['number_of_rounds'], points='all')
    fig.update_layout(title = 'V2', yaxis_title = 'Number of Rounds Uploaded per User', height=600,width = 300, yaxis = dict(showgrid=False, range =[0,500]), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)
with col2:
    fig = px.box(v3_dropoff, y=v3_dropoff['number_of_rounds'], points='all')
    fig.update_layout(title = 'V3', yaxis_title = 'Number of Rounds Uploaded per User', height=600, width = 300, yaxis = dict(showgrid=False, range =[0,500]), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)
with col3:
    fig = px.box(x5_dropoff, y=x5_dropoff['number_of_rounds'], points='all')
    fig.update_layout(title= 'X5', yaxis_title = 'Number of Rounds Uploaded per User', height=600, width = 300, yaxis = dict(showgrid=False, range =[0,500]), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)











