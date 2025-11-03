import streamlit as st
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title=" Olympic Data Dashboard", layout="wide")
st.title(" Olympic Dataset Analysis Dashboard")

# --- File Upload ---
uploaded_file = st.file_uploader(" Upload Olympic dataset (CSV file)", type=["csv"])

if uploaded_file is not None:
    # --- Load Dataset ---
    df = pd.read_csv(uploaded_file, sep="\t", header=None)
    df.columns = ["Name", "Age", "Country", "Year", "Date", "Sport", "Gold", "Silver", "Bronze", "Total"]

    # Convert numeric columns
    medal_cols = ["Gold", "Silver", "Bronze", "Total"]
    for col in medal_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Select Question ---
    st.subheader(" Choose a Question to Display")

    cols = st.columns(9)
    selected_option = None

    for i in range(9):
        with cols[i]:
            if st.button(f"{i+1}️⃣"):
                selected_option = i + 1

    # --- Q1: Dataset Preview ---
    if selected_option == 1:
        st.subheader(" Q1: Dataset Preview")
        st.write(df.head())
        st.write("**Columns:**", df.columns.tolist())

    # --- Q2: Medal Type Distribution ---
    elif selected_option == 2:
        st.subheader(" Q2: Medal Type Distribution")
        medal_totals = df[["Gold", "Silver", "Bronze"]].sum().reset_index()
        medal_totals.columns = ["Medal Type", "Total Count"]
        st.dataframe(medal_totals)

    # --- Q3: Country-wise Total Medals ---
    elif selected_option == 3:
        st.subheader(" Q3: Country-wise Total Medals")
        country_table = df.groupby("Country")["Total"].sum().reset_index().sort_values(by="Total", ascending=False)
        st.dataframe(country_table)

    # --- Q4: Gender-wise Medal Count ---
    elif selected_option == 4:
        st.subheader(" Q4: Gender-wise Medal Count")
        possible_gender_cols = ['Gender', 'Sex', 'gender', 'sex']
        gender_col = next((col for col in possible_gender_cols if col in df.columns), None)
        if gender_col:
            gender_table = df.groupby(gender_col)[["Gold", "Silver", "Bronze", "Total"]].sum().reset_index()
            st.dataframe(gender_table)
        else:
            st.warning(" No gender column found in this dataset.")

    # --- Q5: Year-wise Medal Trend ---
    elif selected_option == 5:
        st.subheader(" Q5: Year-wise Medal Trend")
        if "Year" in df.columns:
            year_table = df.groupby("Year")[["Gold", "Silver", "Bronze", "Total"]].sum().reset_index().sort_values(by="Year")
            st.dataframe(year_table)
        else:
            st.warning(" 'Year' column not found in dataset.")

    # --- Q6: Age-wise Medal Distribution ---
    elif selected_option == 6:
        st.subheader(" Q6: Age-wise Medal Distribution")
        if "Age" in df.columns:
            age_table = df.groupby("Age")[["Gold", "Silver", "Bronze", "Total"]].sum().reset_index().sort_values(by="Age")
            st.dataframe(age_table)
        else:
            st.warning(" 'Age' column not found in dataset.")

    # --- Q7: Sport-wise Medal Distribution ---
    elif selected_option == 7:
        st.subheader(" Q7: Sport-wise Medal Distribution")
        sport_table = df.groupby("Sport")[["Gold", "Silver", "Bronze", "Total"]].sum().reset_index().sort_values(by="Total", ascending=False)
        st.dataframe(sport_table)

    # --- Q8: Country-wise Gold Medal Distribution ---
    elif selected_option == 8:
        st.subheader(" Q8: Country-wise Gold Medal Distribution")
        gold_table = df.groupby("Country")["Gold"].sum().reset_index().sort_values(by="Gold", ascending=False)
        st.dataframe(gold_table)

    # --- Q9: Top 10 Athletes with Most Medals ---
    elif selected_option == 9:
        st.subheader(" Q9: Top 10 Athletes with Most Medals")
        top10 = df.groupby("Name")["Total"].sum().nlargest(10).reset_index()
        st.dataframe(top10)

    # --- Default Message ---
    else:
        st.info(" Click a number (1️ to 9️) above to view the specific analysis.")

else:
    st.info(" Please upload your Olympic dataset to begin.")
