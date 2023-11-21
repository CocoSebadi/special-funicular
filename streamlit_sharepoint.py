import streamlit as st
import random
import string
import pandas as pd
import matplotlib.pyplot as plt
import time
import logging
from backend import PostgreSQLDatabase


def generate_password():
    # Define the pool of characters for the password
    password_characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a password with a length of 12 characters
    password = ''.join(random.choice(password_characters) for i in range(12))

    return password

def is_valid_username(username):
    # Check if the username starts with 'ab' and has additional alphanumeric characters
    return username.startswith('ab') and username[2:].isalnum()

# Streamlit UI components
st.title("Login Page")

# Input fields for username and password
username_input = st.text_input("Enter Username:")
password_input = st.text_input("Enter Password:", type="password")

# Button to submit the login form
if st.button("Login"):
    # Check if the username is valid
    if is_valid_username(username_input):
        st.success(f"Welcome, {username_input}!")

        # Generate and display a random password
        generated_password = generate_password()
        st.info(f"Your generated password: {generated_password}")

    else:
        st.error("Invalid username. Please enter a valid username starting with 'ab'.")

# Function to handle the main page after login
def main_page(db):
    st.title("Main Page")
    
    # Show a pop-up message for choosing to log a new issue or update an existing issue
    issue_action = st.selectbox("Select an action:", ["Log a New Issue", "Update an Existing Issue"])

    # Ensure that only authenticated users can access the system
    if authenticated_user:
        st.header("Issue Details")

            # Input fields for issue details
        issue_name = st.text_input("Issue Name")
        issue_description = st.text_area("Issue Description")
    
        issue_Status = st.selectbox("Issue Status",["Open","Closed","Risk Accepted","Overdue","DWB"])

        risk_type = st.selectbox("Risk Type", ["Low", "Medium", "High"])
    
        subrisk_type = st.selectbox("Subrisk Type",["Model Uncertainty Risk","Process Management Risk","Supplier Risk","Technology Risk","Transaction Processing and Management Risk","Underwriting Risk","Anti-Money Laundering","Business Continuity Risk","Change Risk","Conduct Risk","Customer Engagement Risk","Data and Records Management Risk","Fraud Risk","Information Security and Cyber Risk","Insurance Exposure Risk"])

        entity_dropdown = st.selectbox("Entity", ["FAK","ALAK","LIFESA","ALB","ALZ","NBFS","AIC", "GAM","IDIRECT","INSTANT LIFE","AL"])

        bu_rating = st.selectbox("BU Rating", ["Limited", "Major", "Moderate","Critical"])
    
        agl_rating = st.selectbox("AGL Rating", ["Limited", "Major", "Moderate","Critical"])

        assurance_provider_dropdown = st.selectbox("Assurance Provider", ["2LOD Risk", "External Audit","Internal Audit","GSA"])

        due_date = st.date_input("Due Date")
            
        financially_implicated = st.radio("Does the issue have a financial implication?", ["Yes", "No"])

        risk_event_type = st.text_input("Type of Risk Event")

        # Additional options for updating an existing issue
        if issue_action == "Update an Existing Issue":
            additional_evidence = st.checkbox("Require Additional Evidence")
            if additional_evidence:
                st.text("Please provide additional evidence for the update.")

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
            
        # Power BI Embedding
        st.subheader("Power BI Report Embedding")

        # Replace "your_powerbi_report_url" and "your_powerbi_embed_token" with your actual values
        powerbi_url = "your_powerbi_report_url"
        powerbi_embed_token = "your_powerbi_embed_token"

        iframe_code = f'<iframe width="800" height="600" src="{powerbi_url}&$token={powerbi_embed_token}" frameborder="0" allowFullScreen="true"></iframe>'
        st.markdown(iframe_code, unsafe_allow_html=True)

        # Button to submit the form with a unique key
        submit_button_key = "submit_button_" + str(hash(time.time()))  # Using a timestamp for uniqueness
        if st.button("Submit Form", key=submit_button_key):
            # Logic to handle form submission and data storage
            issue_data = {
                "name": issue_name,
                "description": issue_description,
                "risk_type": risk_type,
                "entities": entity_dropdown,
                "bu_rating": bu_rating,
                "agl_rating": agl_rating,
                "assurance_provider": assurance_provider_dropdown,
                "due_date": due_date,
                "financially_implicated": financially_implicated,
                "risk_event_type": risk_event_type,
                "additional_evidence": additional_evidence if issue_action == "Update an Existing Issue" else None,
                "file_contents": uploaded_file.read() if uploaded_file is not None else None,
                "issue_Status": st.selectbox("Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue", "DWB"]),
                "subrisk_type": st.selectbox("Subrisk Type", ["Model Uncertainty Risk", "Process Management Risk",
                                                            "Supplier Risk", "Technology Risk",
                                                            "Transaction Processing and Management Risk",
                                                            "Underwriting Risk", "Anti-Money Laundering",
                                                            "Business Continuity Risk", "Change Risk",
                                                            "Conduct Risk", "Customer Engagement Risk",
                                                            "Data and Records Management Risk", "Fraud Risk",
                                                            "Information Security and Cyber Risk", "Insurance Exposure Risk"])
            }

            # Validate data
            if validate_issue_data(issue_data):
                # Log the issue data
                log_issue_data(issue_data)

                # If creating a new issue
                if issue_action == "Log a New Issue":
                    db.create_issue(issue_data)
                    st.success("New issue logged successfully!")

                # If updating an existing issue
                elif issue_action == "Update an Existing Issue":
                    # Assume issue_id is the ID of the issue being updated
                    issue_id = st.number_input("Enter the ID of the issue to update:", value=1, min_value=1)
                    db.update_issue(issue_id, issue_data)
                    st.success(f"Issue with ID {issue_id} updated successfully!")
            else:
                st.warning("Issue data validation failed. Please check the entered data.")
        
        # Display recent issues
        display_recent_issues(db)
        
    else:
        st.warning("You are not authenticated. Please login.")    

    # Create an instance of the PostgreSQLDatabase class
    db = PostgreSQLDatabase(dbname='your_dbname', user='your_user', password='your_password', host='your_host', port='your_port')

    # Streamlit UI components for the entire application
    st.title("Issue Tracking System")

# Placeholder for user authentication (replace with your authentication logic)
# For demonstration purposes, a dummy authentication is used
authenticated_user = st.sidebar.text_input("Enter username for authentication:")
login_button = st.sidebar.button("Login", key="login_button_unique_key")

# Check if the user is authenticated and the login button is clicked
if authenticated_user and login_button:
    # Redirect to the main page by setting a query parameter in the URL
    st.experimental_set_query_params(authenticated=True)
    # Reload the app to apply the changes
    st.experimental_rerun()

# Check if the 'authenticated' query parameter is present in the URL
if "authenticated" in st.experimental_get_query_params():
    # If the user is authenticated, show the main page
    main_page(db)

# Backend instructions (replace with your actual backend logic)
st.sidebar.header("Backend Instructions")
st.sidebar.markdown

# Close the database connection when done
db.close_connection()
