import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# JSON file path
JSON_FILE = "expenses.json"

# ---------- Load & Save with JSON ----------
def load_expenses_json():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            st.session_state.expenses = pd.DataFrame(data)
    else:
        st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def save_expenses_json():
    data = st.session_state.expenses.to_dict(orient="records")
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)
    st.success("Expenses saved to JSON!")

# ---------- Visualize Expenses ----------
def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=st.session_state.expenses, x='Category', y='Amount', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No expenses to visualize!")

# ---------- Initialize State ----------
if 'expenses' not in st.session_state:
    load_expenses_json()

if "budget" not in st.session_state:
    st.session_state.budget = 0

# ---------- Title ----------
st.title('Expense Tracker')

# ---------- Sidebar: Budget ----------
st.sidebar.header("Set Budget")
st.session_state.budget = st.sidebar.number_input("Enter your budget", min_value=0, value=st.session_state.budget)

# ---------- Sidebar: Add Expense ----------
with st.sidebar:
    st.header('Add Expense')
    date = st.date_input('Date')
    category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'])
    amount = st.number_input('Amount', min_value=0.0, format="%.2f")
    description = st.text_input('Description')
    if st.button('Add'):
        new_expense = pd.DataFrame([[str(date), category, amount, description]], 
                                   columns=st.session_state.expenses.columns)
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
        st.success('Expense added!')

# ---------- Save Button ----------
if st.button("Save Expenses to JSON"):
    save_expenses_json()

# ---------- Summary ----------
total_spent = st.session_state.expenses["Amount"].sum() if not st.session_state.expenses.empty else 0
budget_remaining = st.session_state.budget - total_spent

st.header("Budget Summary")
st.metric("Total Spent", f"₹{total_spent}")
st.metric("Budget Remaining", f"₹{budget_remaining}")

# ---------- Expense Table ----------
st.header("All Expenses")
st.dataframe(st.session_state.expenses)

# ---------- Visualization ----------
st.header('Visualization')
if st.button('Visualize Expenses'):
    visualize_expenses()
