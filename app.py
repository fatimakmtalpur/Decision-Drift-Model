import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Discipline Model", layout="wide")

st.title("Decision Drift Model Dashboard")

# ---- LOAD EXISTING FILES (NO RE-SIMULATION) ----
df = pd.read_csv("C:/Users/MEMONS/Desktop/Financial_model/discipline_history.csv")
pred = pd.read_csv("C:/Users/MEMONS/Desktop/Financial_model/predicted_discipline.csv")
st.write(pred['predicted_discipline'].describe())
raw = pd.read_csv("C:/Users/MEMONS/Desktop/Financial_model/budget_data.csv")
raw['date'] = pd.to_datetime(raw['date'])

# Convert date
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')
df = df.groupby('date', as_index=False).mean(numeric_only=True)

# FIX: create missing columns
df['ideal'] = 100
df['deviation'] = df['ideal'] - df['discipline']

#actual data
st.subheader("Actual Spending Data")
st.write(raw.head())
daily = raw.groupby('date')['amount'].sum().reset_index()

fig0, ax0 = plt.subplots(figsize=(8,3))
ax0.plot(daily['date'], daily['amount'], color='green')
ax0.set_title("Daily Spending")
ax0.tick_params(axis='x', rotation=45)

st.pyplot(fig0, use_container_width=True)
# ---- GRAPH 1: DISCIPLINE VS TARGET ----
st.subheader("Discipline vs Target")

fig1, ax1 = plt.subplots(figsize=(8,3))
ax1.plot(df['date'], df['discipline'], label="Actual Discipline")
ax1.plot(df['date'], df['ideal'], linestyle='--', label="Target Discipline")
ax1.set_title("Actual vs Target Discipline")
ax1.legend()
ax1.tick_params(axis='x', rotation=45)

st.pyplot(fig1, use_container_width=True)

# ---- GRAPH 2: DEVIATION ----
st.subheader("Deviation from Target")

fig2, ax2 = plt.subplots(figsize=(8,3))
ax2.plot(df['date'], df['deviation'], color='red')
ax2.set_title("Deviation from Ideal Discipline")
ax2.tick_params(axis='x', rotation=45)

st.pyplot(fig2, use_container_width=True)

# ---- GRAPH 3: PREDICTION ----
st.subheader("Predicted Discipline")

fig3, ax3 = plt.subplots(figsize=(8,3))

# Ensure clean base date
last_date = df['date'].max()

# Ensure future_day is clean integer
pred['future_day'] = pred['future_day'].astype(int)

# Build proper datetime axis for prediction
pred['date'] = pd.to_datetime(last_date) + pd.to_timedelta(pred['future_day'], unit='D')

# Plot prediction
ax3.plot(pred['date'], pred['predicted_discipline'])
ax3.set_title("Future Discipline Prediction")
ax3.tick_params(axis='x', rotation=45)

st.pyplot(fig3, use_container_width=True)
# ---- METRICS ----
st.subheader("Key Metrics")

current = df['discipline'].iloc[-1]
avg = df['discipline'].mean()
dev = df['deviation'].mean()

if current >= 70:
    status = "On Track"
elif current >= 50:
    status = "Drifting"
else:
    status = "Off Track"

col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Discipline", round(current, 2))
col2.metric("Average Discipline", round(avg, 2))
col3.metric("Avg Deviation", round(dev, 2))
col4.metric("Status", status)

#for easy accessing
#C:/Users/MEMONS/Desktop/Financial_model/
#python -m streamlit run app.py