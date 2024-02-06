import streamlit as st
import sqlite3
from hashlib import sha256
import pandas as pd
#from auth import sign
import random 
import psycopg2

##PosGreSQL
params = {
    "host": "localhost",
    "user": "postgres",
    "port": 5432,
    "password": "Mkw@naz1" 
}
connection = psycopg2.connect(**params, dbname= "ICP_db")
    

CURSOR=connection.cursor()

# # Function to create a SQLite database connection
# def create_connection():
#     conn = sqlite3.connect("issues20240202.db")
#     return conn


# function to view current issues
def view_all_issues():
    CURSOR.execute('SELECT * FROM  issues')
    data = CURSOR.fetchall()
    return data


# function to view current issues status
def view_all_issues_status():
    CURSOR.execute('SELECT issue_status FROM  issues')
    data = CURSOR.fetchall()
    return data

df_status=pd.DataFrame(view_all_issues_status(),columns=['Issue_Status'])
# Function to create a table for  new user
# Function to create a table for  new user
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# Function to sign up a new user
def signup(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = password
    cursor.execute("INSERT INTO  users  (username, password) VALUES (?,?)", (username, hashed_password))

    conn.commit()
    conn.close()

#
# Function to log in a user
def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = password
    cursor.execute("SELECT * FROM  users  WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()

    conn.close()
    return user






# # Function to create the issues table
# def create_table():
#     conn = create_connection()
#     cursor = conn.cursor()

#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS issues (
#             id Serial PRIMARY KEY,
#             issue_code VARCHAR(255) UNIQUE,
#             issue_name VARCHAR(255),
#             description TEXT,
#             issue_status VARCHAR(50),
#             risk_type VARCHAR(50),
#             subrisk_type VARCHAR(50),
#             entities VARCHAR(255),
#             bu_rating VARCHAR(50),
#             agl_rating VARCHAR(50),
#             assurance_provider VARCHAR(255),
#             due_date DATE,
#             financially_implicated BOOLEAN,
#             risk_event_type VARCHAR(255),
#             additional_evidence TEXT,
#             file_contents VARCHAR(255),
#             issuer_name VARCHAR(255),
#             issuer_surname VARCHAR(255),
#             issuer_email VARCHAR(255),
#             usernam Varchar(255)      
#         )
#     ''')

#     conn.commit()
#     conn.close()
# Functions to fetch issue code and generate new code from the database start here
def generate_unique_code():
    while True:
        # Generate a random four-digit code
        code = str(random.randint(1000, 9999))

        # Check if the code is unique in the database
        if not is_code_exists(code):
            return code
 
def is_code_exists(code):
    #Check if the code exists in the 'issues' table
    CURSOR.execute("SELECT COUNT(*) FROM issues WHERE issue_code = ?", (code,))
    count = CURSOR.fetchone()[0]
    return count > 0
    

#Function end here :)
    
# Streamlit UI
def main():
    

    st.title("Issue Tracker App")

    # Sidebar
    page = st.sidebar.radio("Navigation", ["Login", "View Current Issues", "Log Issue", "Update Issue"])
    if page=='View Current Issues':
       

        df=pd.DataFrame(view_all_issues(),columns=["ID",'issue_code','name',' description','issue_status','risk_type','subrisk_type','entities','bu_rating','agl_rating','assurance_provider','due_date','financially_implicated','risk_event_type',' additional_evidence',' file_contents','issuer_name','issuer_surname','issuer_email','username'])
        dffiltered=st.text_input("...")
        df_fil=df[df['issue_code']==dffiltered]
        src_btn=st.button("Search")
        if src_btn==True:
            st.table(df_fil)
        else:
            st.table(df.tail(5))
        #st.write(view_all_issues())
    # if page == "Signup":
    #     st.header("Signup")
    #     username = st.text_input("Username")
    #     password = st.text_input("Password", type="password")
    #     if st.button("Signup"):
    #         signup(username, password)
    #         st.success("Signup successful! Now you can log in.")

    if page == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.username = username  # Store username in session state
                st.success(f"Welcome, {user[1]}!")
            else:
                st.error("Invalid username or password.")

    elif page == "Log Issue":
        st.header("Log Issue")
        if st.session_state.get('username'):
            issue_code = st.text_input("Issue Code (4 characters)")
            issue_name = st.text_input("Name")
            description = st.text_area("Description")
            issue_status =st.selectbox("Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue"])
            risk_type = st.selectbox("Risk Type", ["Operational & Resilience Risk", "Insurance risk type", "Compliance Risk", "Model Risk", "Conduct Risk"])
            subrisk_type = st.selectbox("Subrisk Type", ["Model Uncertainty Risk", "Process Management Risk", "Supplier Risk", "Technology Risk", "Transaction Processing and Management Risk", "Underwriting Risk", "Anti-Money Laundering", "Business Continuity Risk", "Change Risk", "Conduct Risk", "Customer Engagement Risk", "Data and Records Management Risk", "Fraud Risk", "Information Security and Cyber Risk", "Insurance Exposure Risk"])
            bu_rating = st.selectbox("BU Rating", ["Limited", "Major", "Moderate", "Critical"])
            agl_rating = st.selectbox("AGL Rating", ["Limited", "Major", "Moderate", "Critical"])
            assurance_provider_dropdown = st.selectbox("Assurance Provider", ["2LOD Risk", "External Audit", "Internal Audit", "GSA"])
            due_date = st.date_input("Due Date")
            financially_implicated = st.radio("Does the issue have a financial implication?", ["Yes", "No"])

            # Check the user's choice
            if financially_implicated == "Yes":
                # Prompt the user to upload a financial statement
                uploaded_file = st.file_uploader("Upload your financial statement (PDF or Excel)", type=["pdf", "xlsx"])
                if uploaded_file:
                    # Process the uploaded file (you can add your logic here)
                    st.success("File uploaded successfully!")
                else:
                    st.warning("Please upload a valid financial statement.")
            else:
                st.info("No financial implications. Proceed with other actions.")
            issuer_name = st.text_input("Issuer Name")
            issuer_surname = st.text_input("Issuer surname")
            issuer_email = st.text_input("Issuer Email Address")
            # e... Add other input fields for the remaining columns
            # File attachment option for various types
            uploaded_file = st.file_uploader("Attach a File (if applicable)", type=["pdf", "jpg", "png", "txt", "csv", "xlsx"])
    
            # Check if a file is uploaded
            if uploaded_file is not None:
                file_type = uploaded_file.name.split(".")[-1].lower()
    
                # Your logic for handling CSV data goes here
                if file_type == "csv":
                    # Handle CSV file
                    df = pd.read_csv(uploaded_file)
                    st.write("CSV file content:")
                    st.dataframe(df)
    
                # Your logic for handling Excel data goes here
                elif file_type in ["xlsx", "xls"]:
                    # Handle Excel file
                    df = pd.read_excel(uploaded_file)
                    st.write("Excel file content:")
                    st.dataframe(df)
    
                else:
                    # Handle other file types
                    file_contents = uploaded_file.read()
                    st.text(f"Content of the uploaded file ({file_type}):")
                    st.text(file_contents.decode("utf-8"))

            if st.button("Log Issue"):
                            if issue_status != "Open":
                                st.warning("The issue status must be 'Open' to log a new issue. Please correct the issue status.")
            else:
                log_issue(issue_code, issue_name, description,issue_status,risk_type,subrisk_type, bu_rating ,agl_rating,assurance_provider_dropdown, due_date,financially_implicated,issuer_name,issuer_surname,issuer_email,st.session_state.username)
                st.success("Issue logged successfully!")
        else:
            st.warning("Please login to log an issue.")

    elif page == "Update Issue":
        st.header("Update Issue")
        st.subheader("Main Table")
        # df=pd.DataFrame(view_all_issues(),columns=['issue_code','issue_name',' description','issue_status','risk_type','subrisk_type','entities','bu_rating','agl_rating','assurance_provider','due_date','financially_implicated','risk_event_type',' additional_evidence',' file_contents','issuer_name','issuer_surname','issuer_email','username'])
        # dffiltered=st.text_input("...")
        # df_fil=df[df['issue_code']==dffiltered]
        # src_btn=st.button("Search")
        # if src_btn==True:
        #     st.data_editor(df_fil)
        # else:
        #     #st.table(df.tail(5))
        #     st.data_editor(df)
        df=pd.DataFrame(view_all_issues(),columns=["ID",'issue_code','name',' description','issue_status','risk_type','subrisk_type','entities','bu_rating','agl_rating','assurance_provider','due_date','financially_implicated','risk_event_type',' additional_evidence',' file_contents','issuer_name','issuer_surname','issuer_email','username'])
        dffiltered=st.text_input("...")
        df_fil=df[df['issue_code']==dffiltered]
        src_btn=st.button("Search")
        if src_btn==True:
            st.data_editor(df_fil)
        else:
            st.data_editor(df.tail(5))

        if st.checkbox("Updated Description"):
            if st.session_state.get('username'):
                issue_id = st.text_input("Enter Issue ID")
                new_issue = st.text_area("Describe the updated issue",key=30)
                if st.button("Update Issue"):
                    update_issue(issue_id, new_issue)
                    st.success("Issue updated successfully!")

            if st.checkbox("Updated Issue Status"):
                if st.session_state.get('username'):
                    issue_id = st.text_input("Enter Issue ID",key='id')
                    new_issue =st.selectbox("Status",options=["Open", "Closed", "Risk Accepted", "Overdue"]) #st.text_area("Describe the updated issue",key=20)
                    if st.button("Update Issue Status"):
                        update_issue_status(issue_id, new_issue)
                        st.success("Issue updated successfully!")
            else:
                st.warning("Please login to update an issue.")

# Function to log an issue
def log_issue(issue_code, issue_name, description, issue_status,risk_type,subrisk_type, bu_rating,agl_rating,assurance_provider,due_date,financially_implicated,issuer_name,issuer_surname, issuer_email,username):

    CURSOR.execute('''
        INSERT INTO issues (
            issue_code,name, description,issue_status,risk_type,subrisk_type,bu_rating,agl_rating ,assurance_provider, due_date,financially_implicated,issuer_name,issuer_surname, issuer_email,username
        ) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ''', (issue_code, issue_name, description, issue_status,risk_type,subrisk_type, bu_rating,agl_rating,assurance_provider, due_date,financially_implicated,issuer_name,issuer_surname, issuer_email,username))

    connection.commit()
    connection.close()

# def log_issue(issue_code, name, description, issue_status,risk_type ,subrisk_type,entities,bu_rating,agl_rating, risk_event_type, assurance_provider,due_date,financially_implicated,issuer_surname,issuer_email,username):
#     conn = create_connection()
#     cursor = conn.cursor()

#     cursor.execute('''
#         INSERT INTO issues (
#            issue_code, name, description, issue_status,risk_type ,subrisk_type,entities,bu_rating,agl_rating, risk_event_type, username,assurance_provider,due_date,financially_implicated,issuer_surname,issuer_email
#         ) VALUES (?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?)
#     ''', (issue_code, name, description, issue_status,risk_type ,subrisk_type,entities,bu_rating,agl_rating, risk_event_type, assurance_provider,due_date,financially_implicated,issuer_surname,issuer_email,username))

#     conn.commit()
#     conn.close()

# Function to update an issue Discription
def update_issue(issue_id, new_issue):

    CURSOR.execute("UPDATE issues SET description=%s WHERE id=%s, (new_issue, issue_id)")

    connection.commit()
    connection.close()

# Function to update an issue Status
def update_issue_status(issue_id, new_issue):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE issues SET issue_status=? WHERE id=?", (new_issue, issue_id))

    conn.commit()
    conn.close()
# ... (Other functions remain unchanged)

if __name__ == '__main__':
    main()
