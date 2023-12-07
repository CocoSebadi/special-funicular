import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor

class PostgreSQLDatabase:
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
            print("Connected to the database!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print("Connection closed.")

    def initialize_database(self):
        # Add your database initialization code here if needed
        pass

    def create_issue(self, issue_data):
        try:
            insert_query = sql.SQL("""
                INSERT INTO issues (name, description, issue_status, risk_type, subrisk_type, entities, 
                                    bu_rating, agl_rating, assurance_provider, due_date, financially_implicated, 
                                    risk_event_type, additional_evidence, file_contents)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """)
            
            self.cursor.execute(insert_query, (
                issue_data["name"], issue_data["description"], issue_data["issue_status"],
                issue_data["risk_type"], issue_data["subrisk_type"], issue_data["entities"],
                issue_data["bu_rating"], issue_data["agl_rating"], issue_data["assurance_provider"],
                issue_data["due_date"], issue_data["financially_implicated"], issue_data["risk_event_type"],
                issue_data["additional_evidence"], issue_data["file_contents"]
            ))
            
            issue_id = self.cursor.fetchone()[0]
            self.conn.commit()

            print(f"Issue created with ID: {issue_id}")
            return issue_id
        except Exception as e:
            print(f"Error creating issue: {e}")

# You can add more methods based on your application's needs
