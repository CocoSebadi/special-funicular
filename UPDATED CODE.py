import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Define a function to calculate reminder date
def calculate_reminder_date(due_date):
    return due_date - timedelta(days=3 * 30)

# Define a function to validate employee number
def validate_employee_number(employee_number):
    valid_employee_numbers = ["emp123", "emp456", "emp789"]
    return employee_number in valid_employee_numbers

# Define a function to send reminder emails
def send_email(recipient_email, subject, message):
    # Code for sending emails
    pass


#Custom Streamlit theme
def set_custom_theme():
    st.markdown(
        """
        <style>
            body {
                background-color: red; /* Change theme background color to red */
                display: flex;
                flex-direction: column;
                align-items: center; /* Align items (including the logo) horizontally in the center */
            }
            .css-1poyekb {
                background-color: red; /* Change theme color to red */
                color: #f0f2f6;
            }
            .element-container img {
                max-width: 10%; /* Resize logo image to appear smaller */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit app layout with custom theme
set_custom_theme()
st.title("Issue Tracker App")
st.image("ABSA logo.jpg", use_column_width=True)  # Add company logo
# Login Section
employee_number = st.text_input("Employee Number", max_chars=7)

if st.button("Login"):
    if len(employee_number) == 7 and validate_employee_number(employee_number):
        st.success("Login successful!")
    else:
        st.error("Invalid employee number. Please try again.")
        st.stop()

# Issue Action Section
issue_action = st.radio("Select an action:", ["Log a New Issue", "Update an Existing Issue"])

if issue_action == "Log a New Issue":
    st.write("You chose to log a new issue.")
    
    # Add form elements for logging a new issue
    issue_name = st.text_input("Issue Name")
    issue_description = st.text_area("Issue Description", "")
    issue_status = st.selectbox("Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue"])
    risk_type = st.selectbox("Risk Type", ["Operational & Resilience Risk", "Insurance risk type", "Compliance Risk", "Model Risk", "Conduct Risk"])
    subrisk_type = st.selectbox("Subrisk Type", ["Model Uncertainty Risk", "Process Management Risk", "Supplier Risk", "Technology Risk", "Transaction Processing and Management Risk", "Underwriting Risk", "Anti-Money Laundering", "Business Continuity Risk", "Change Risk", "Conduct Risk", "Customer Engagement Risk", "Data and Records Management Risk", "Fraud Risk", "Information Security and Cyber Risk", "Insurance Exposure Risk"])
    entity_dropdown = st.selectbox("Entity", ["FAK", "ALAK", "LIFE SA", "ALB", "ALZ", "NBFS: SPM", "NBFS: WILLS TRUST AND ESTATES", "NBFS: AIFA", "AIC", "GAM"])
    bu_rating = st.selectbox("BU Rating", ["Limited", "Major", "Moderate", "Critical"])
    agl_rating = st.selectbox("AGL Rating", ["Limited", "Major", "Moderate", "Critical"])
    assurance_provider_dropdown = st.selectbox("Assurance Provider", ["2LOD Risk", "External Audit", "Internal Audit", "GSA"])
    due_date = st.date_input("Due Date")
    financially_implicated_help = "Select 'Yes' if the issue has a financial implication, otherwise select 'No'."
    financially_implicated = st.radio("Does the issue have a financial implication?", ["Yes", "No"])
    view_option = st.radio("View Financial Statements:", ["Balance Sheet", "Income Statement"])
     # Add checkboxes for indicating the issue level
    issue_level = st.radio("Is the issue at the Group Level or PSC Level?", ["Group Level", "AFS Level"])
    issue_owner_name = st.text_input("Issue Owner Name")
    issue_owner_email = st.text_input("Issue Owner Email Address")
     # Convert the input due_date to datetime object
    due_date = datetime.combine(due_date, datetime.min.time())

        # Calculate the reminder date (3 months before the due date)
    reminder_date = calculate_reminder_date(due_date)

        # Check if it's time to send the reminder
    current_date = datetime.now()
    if current_date >= reminder_date:
            # Assuming you have some email sending functionality here
             send_email(issue_owner_email, "Reminder: Upcoming Issue Due Date", f"Dear {issue_owner_name},\n\nThis is a reminder that the issue '{issue_name}' is due on {due_date}.I trust this email finds you well. I wanted to bring to your attention that the deadline for resolving the current issue is fast approaching. As part of the resolution process, we kindly request you to compile an Incident Closure Plan (ICP) using the specified ICP format.")

    # Submit button for logging new issue
    if st.button("Submit New Issue"):
        st.success("New issue submitted successfully!")

elif issue_action == "Update an Existing Issue":
    st.write("You chose to update an existing issue.")
    
    # File uploader for existing issues tracker
    uploaded_file = st.file_uploader("Upload an existing issues tracker file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Specify encoding parameter to handle non-UTF-8 characters
        existing_issues_df = pd.read_csv(uploaded_file, encoding='latin1')
        st.write("Existing Issues Tracker Loaded:")
        st.write(existing_issues_df)

        # Selectbox to choose issue to update
        selected_issue_id = st.selectbox("Select the Issue to Update", existing_issues_df['Issue ID'])

        # Form elements for updating an existing issue
        issue_owner = st.text_input("Issue Owner")
        original_date = st.date_input("Original Date")
        revised_due_date = st.date_input("Revised Due Date")
        attachment = st.file_uploader("Attach a File or Provide Written Evidence", type=["pdf", "docx"])

        # Submit button for updating existing issue
        if st.button("Submit Update"):
            st.success("Issue updated successfully!")
    else:
        st.warning("Please upload an existing issues tracker file.")

# Display error if login fails
else:
    st.error("Login failed. Please try again.")

    
