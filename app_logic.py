import streamlit as st
import pandas as pd
from PostgreSQLDatabase import PostgreSQLDatabase
from config import Config

# Access configurations
database_config = Config.DB_CONFIG
powerbi_config = Config.POWERBI_CONFIG
streamlit_config = Config.STREAMLIT_CONFIG
api_key = Config.API_KEY
secret_key = Config.SECRET_KEY

class AppLogic:
    def __init__(self, db):
        self.db = db

    def initialize_database(self):
        # You can include any initialization logic here
        # For example, creating tables, setting up indices, etc.
        # For now, we'll just create tables if they don't exist
        self.create_tables()

    def create_tables(self):
        # Add logic to create tables if they don't exist
        # This could involve executing SQL statements or using an ORM
        # Replace the following lines with your actual table creation logic

        # Example: Creating 'issues' table
        create_issues_table_query = """
        CREATE TABLE IF NOT EXISTS issues (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            issue_status VARCHAR(50),
            risk_type VARCHAR(50),
            subrisk_type VARCHAR(50),
            entities VARCHAR(255),
            bu_rating VARCHAR(50),
            agl_rating VARCHAR(50),
            assurance_provider VARCHAR(255),
            due_date DATE,
            financially_implicated BOOLEAN,
            risk_event_type VARCHAR(255),
            additional_evidence TEXT,
            file_contents BYTEA
            -- Add other issue-related fields as needed
        );
        """

        # Execute the query to create 'issues' table
        self.db.execute_query(create_issues_table_query)

    def validate_issue_data(self, issue_data):
    # Implement validation logic for issue data
    # Return True if data is valid, else False
        valid = True  # Placeholder for validation logic

    # Check if the 'name' field is not empty
        if not issue_data.get("name"):
            st.warning("Issue name cannot be empty.")
            valid = False

    # Check if the 'due_date' is a valid date (you can customize this based on your requirements)
        try:
            datetime.strptime(issue_data.get("due_date"), "%Y-%m-%d")
        except ValueError:
            st.warning("Invalid due date format. Please use YYYY-MM-DD.")
            valid = False

    # Add more validation checks as needed

        return valid


    def log_new_issue(self, issue_data):
        # Logic to log a new issue in the database
        if self.validate_issue_data(issue_data):
            self.db.create_issue(issue_data)
            st.success("New issue logged successfully!")
        else:
            st.warning("Issue data validation failed. Please check the entered data.")

    def update_existing_issue(self, issue_id, issue_data):
        # Logic to update an existing issue in the database
        if self.validate_issue_data(issue_data):
            self.db.update_issue(issue_id, issue_data)
            st.success(f"Issue with ID {issue_id} updated successfully!")
        else:
            st.warning("Issue data validation failed. Please check the entered data.")

    def display_recent_issues(self):
        # Logic to display recent issues in the UI
        # For now, we'll use a placeholder query to get recent issues
        recent_issues_query = "SELECT * FROM issues ORDER BY id DESC LIMIT 10;"
        
        # Execute the query to get recent issues
        recent_issues = self.db.execute_query(recent_issues_query)

        # Display recent issues using Streamlit components
        st.header("Recent Issues")
        if recent_issues:
            # Display recent issues in a DataFrame
            st.dataframe(recent_issues)
        else:
            st.info("No recent issues found.")

    def close_connection(self):
        # Close the database connection
        self.db.close_connection()
