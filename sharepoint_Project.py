import streamlit as st
import pandas as pd

def login():
    # Placeholder authentication logic
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if username == "demo" and password == "password":
        return True
    else:
        return False

def main():
    st.title("Issues Form")

    if login():
        st.success("Login successful!")

        # Show a pop-up message for choosing to log a new issue or update an existing issue
        issue_action = st.radio("Select an action:", ["Log a New Issue", "Update an Existing Issue"])

        # Placeholder DataFrame for consolidated open issues
        open_issues_data = {
            'Issue ID': [1, 2, 3, 4],
            'Issue Owner': ['John', 'Jane', 'Bob', 'Mary'],
            'Original Date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-05-01'],
            'Revised Due Date': ['2022-02-01', '2022-03-01', '2022-04-01', '2022-06-01'],
            'BU Rating': ['Limited', 'Major', 'Moderate','Critical']
        }
        open_issues_df = pd.DataFrame(open_issues_data)

        if issue_action == "Log a New Issue":
            st.write("You chose to log a new issue.")
            # Add form elements for logging a new issue
            issue_name = st.text_input("Issue Name")
            issue_description = st.text_area("Issue Description", "")
            issue_Status = st.selectbox("Issue Status",["Open","Closed","Risk Accepted","Overdue","DWB"])
            risk_type = st.selectbox("Risk Type",["Operational & Rislience Risk","Insurance risk type","Compliance Risk","Model Risk","Conduct Risk"])
            subrisk_type = st.selectbox("Subrisk Type",["Model Uncertainty Risk","Process Management Risk","Supplier Risk","Technology Risk","Transaction Processing and Management Risk","Underwriting Risk","Anti-Money Laundering","Business Continuity Risk","Change Risk","Conduct Risk","Customer Engagement Risk","Data and Records Management Risk","Fraud Risk","Information Security and Cyber Risk","Insurance Exposure Risk"])
            entity_dropdown = st.selectbox("Entity", ["FAK","ALAK","LIFESA","ALB","ALZ","NBFS","AIC", "GAM","IDIRECT","INSTANT LIFE","AL"])
            bu_rating = st.selectbox("BU Rating", ["Limited", "Major", "Moderate","Critical"])
            agl_rating = st.selectbox("AGL Rating", ["Limited", "Major", "Moderate","Critical"])
            assurance_provider_dropdown = st.selectbox("Assurance Provider", ["2LOD Risk", "External Audit","Internal Audit","GSA"])
            due_date = st.date_input("Due Date")
            financially_implicated = st.radio("Does the issue have a financial implication?", ["Yes", "No"])
        

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
            bu_rating_update = st.text_input("BU Rating Update")

            # File attachment or written evidence for the update
            attachment = st.file_uploader("Attach a File or Provide Written Evidence", type=["pdf", "docx"])

        # Add a button to submit the form
        if st.button("Submit"):
            st.success("Form submitted successfully!")

    else:
        st.error("Login failed. Please try again.")

if __name__ == "__main__":
    main()

