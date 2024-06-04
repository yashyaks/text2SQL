from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
        You are an expert in converting English questions to SQL queries!

        The SQL database has the name "llmdata" and has the following columns: "Model", "Company", "Arch", "Parameters", "Tokens", "Ratio", "ALScore", "Training dataset", "Release Date", "Notes", "Playground".

        For example:

        Example 1 - How many models are present in the database?
        The SQL command will be:
        SELECT COUNT(*) FROM llmdata;

        Example 2 - Retrieve all models released by OpenAI.
        The SQL command will be:
        SELECT * FROM llmdata WHERE "Company" = "OpenAI";

        The SQL code should not have ``` in the beginning and end, and the word "sql" should not be present in the output.

    """
]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"data/llmdb")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)