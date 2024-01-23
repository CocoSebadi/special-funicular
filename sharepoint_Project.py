
import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Placeholder authentication logic
def login(username, password):
    return username == "demo" and password == "password"

# Placeholder function to send email
def send_email(to_email, subject, body):
    # Replace these with your email credentials and SMTP server information
    email_address = "your_email@gmail.com"
    email_password = "your_email_password"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create message
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Establish connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(message)

# Main function
def main():
    # Placeholder authentication logic
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("Login successful!")

            # Show a pop-up message for choosing to log a new issue or update an existing issue
            issue_action = st.radio("Select an action:", ["Log a New Issue", "Update an Existing Issue"])

            # Placeholder DataFrame for consolidated open issues
            open_issues_data = {
                'Issue ID': [1, 2, 3, 4],
                'Issue Owner': ['John', 'Jane', 'Bob', 'Mary'],
                'Original Date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-05-01'],
                'Revised Due Date': ['2022-02-01', '2022-03-01', '2022-04-01', '2022-06-01'],
                'BU Rating': ['Limited', 'Major', 'Moderate', 'Critical']
            }
            open_issues_df = pd.DataFrame(open_issues_data)

            if issue_action == "Log a New Issue":
                st.write("You chose to log a new issue.")
                # Add form elements for logging a new issue
                issue_name = st.text_input("Issue Name")
                issue_description = st.text_area("Issue Description", "")
                issue_Status = st.selectbox("Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue"])
                Principle_risk_type = st.selectbox("Principle_risk_type",
                                                   ["Operational & Rislience Risk", "Insurance risk type",
                                                    "Compliance Risk", "Model Risk", "Conduct Risk"])
                subrisk_type = st.selectbox("Subrisk Type",
                                            ["Model Uncertainty Risk", "Process Management Risk", "Supplier Risk",
                                             "Technology Risk", "Transaction Processing and Management Risk",
                                             "Underwriting Risk", "Anti-Money Laundering", "Business Continuity Risk",
                                             "Change Risk", "Conduct Risk", "Customer Engagement Risk",
                                             "Data and Records Management Risk", "Fraud Risk",
                                             "Information Security and Cyber Risk", "Insurance Exposure Risk"])
                entity_dropdown = st.selectbox("Entity",
                                               ["FAK", "ALAK", "LIFE SA", "ALB", "ALZ", "NBFS: SPM",
                                                "NBFS :WILLS TRUST AND ESTATES", "NBFS:AIFA", "AIC", "GAM"])
                BU_risk_rating = st.selectbox("BU risk Rating", ["Limited", "Major", "Moderate", "Critical"])
                agl_rating = st.selectbox("AGL Rating", ["Limited", "Major", "Moderate", "Critical"])
                assurance_provider_dropdown = st.selectbox("Assurance Provider",
                                                            ["2LOD Risk", "External Audit", "Internal Audit", "GSA"])
                due_date = st.date_input("Due Date")
                issue_owner_name = st.text_input("Issue Owner Name")
                issue_owner_email = st.text_input("Issue Owner Email Address")
                financially_implicated = st.radio("Does the issue have a financial implication?", ["Yes", "No"])

                # Calculate the reminder date (3 months before the due date) if due_date is not None
                if due_date is not None:
                    reminder_date = due_date - timedelta(days=3 * 30)

                    # Check if it's time to send the reminder
                    current_date = datetime.now()
                    if current_date >= reminder_date:
                        # Send the reminder email
                        subject = f"Reminder: Upcoming Issue Due Date - {issue_name}"
                        body = f"Dear {issue_owner_name},\n\nThis is a reminder that the issue '{issue_name}' is due on {due_date}. " \
                               f"I trust this email finds you well. I wanted to bring to your attention that the deadline for resolving " \
                               f"the current issue is fast approaching. As part of the resolution process, we kindly request you to " \
                               f"compile an Incident Closure Plan (ICP) using the specified ICP format."
                        send_email(issue_owner_email, subject, body)

                        st.write(f"Reminder email sent to {issue_owner_email} on {reminder_date}")

                # Add a button to submit the form
                if st.button("Submit"):
                    st.success("Form submitted successfully!")

            elif issue_action == "Update an Existing Issue":
                st.write("You chose to update an existing issue.")

                # Show consolidated open issues in a table
                st.subheader("Consolidated Open Issues:")
                st.table(open_issues_df)

                # Allow the user to select the issue they want to update
                selected_issue_id = st.selectbox("Select the Issue to Update", open_issues_df['Issue ID'])

                # Additional form elements for updating an existing issue
                issue_owner = st.text_input("Issue Owner")
                original_date = st.date_input("Original Date")
                revised_due_date = st.date_input("Revised Due Date")

                # File attachment or written evidence for the update
                attachment = st.file_uploader("Attach a File or Provide Written Evidence", type=["pdf", "docx"])

                # Add a button to submit the form
                if st.button("Submit"):
                    st.success("Form submitted successfully!")


if __name__ == "__main__":
    main()
