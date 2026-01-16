#!/usr/bin/env python3
"""
COMMAND-BASED PYTHON SQL EXECUTOR
A lightweight, terminal-based SQL execution tool built using Python.
This software allows users to connect to databases and execute SQL commands directly from the command line without any GUI.
"""

import sqlite3
import os
import sys
import time
import csv
import json
import hashlib
import getpass
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
import subprocess

class PasswordManager:
    """Handles password setup and validation for the application"""
    
    def __init__(self, config_file: str = "sql_cli_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {"password_hash": None, "setup_complete": False}
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
            return True
        except Exception:
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def setup_password(self) -> bool:
        """Setup password for first-time installation"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                 SQL CLI - FIRST TIME SETUP                   ║
║                 Professional Database Tool                   ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        if self.config.get("setup_complete"):
            print("┌─ Setup Status")
            print("│  Status: Already configured")
            print("│  Action: Password already set")
            print("└─ Setup complete")
            return True
        
        print("┌─ Security Setup")
        print("│  Action: Set administrator password")
        print("│  Purpose: Protect application access")
        print("│  Requirement: Minimum 6 characters")
        print("└─ Please configure")
        
        while True:
            try:
                password = getpass.getpass("┌─ Enter new password: ")
                if len(password) < 6:
                    print("│  Error: Password must be at least 6 characters")
                    print("└─ Please try again")
                    continue
                
                confirm_password = getpass.getpass("┌─ Confirm password: ")
                if password != confirm_password:
                    print("│  Error: Passwords do not match")
                    print("└─ Please try again")
                    continue
                
                # Hash and save password
                self.config["password_hash"] = self.hash_password(password)
                self.config["setup_complete"] = True
                
                if self.save_config():
                    print("┌─ Setup Complete")
                    print("│  Status: Password configured successfully")
                    print("│  Security: Application is now protected")
                    print("└─ Setup finished")
                    return True
                else:
                    print("┌─ Setup Error")
                    print("│  Error: Failed to save configuration")
                    print("│  Action: Please check file permissions")
                    print("└─ Setup failed")
                    return False
                    
            except KeyboardInterrupt:
                print("\n┌─ Setup Cancelled")
                print("│  Action: Setup interrupted by user")
                print("└─ Exiting")
                return False
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        if not self.config.get("password_hash"):
            return False
        return self.hash_password(password) == self.config["password_hash"]
    
    def authenticate(self) -> bool:
        """Authenticate user with password"""
        if not self.config.get("setup_complete"):
            return self.setup_password()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║                 SQL CLI - AUTHENTICATION                     ║
║                 Professional Database Tool                   ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                print(f"┌─ Authentication Required")
                print(f"│  Attempt: {attempts + 1} of {max_attempts}")
                password = getpass.getpass("│  Enter password: ")
                
                if self.verify_password(password):
                    print("┌─ Authentication Success")
                    print("│  Status: Access granted")
                    print("│  Welcome: Authorized user")
                    print("└─ Loading application")
                    return True
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"│  Error: Invalid password")
                        print(f"│  Attempts remaining: {remaining}")
                        print("└─ Please try again")
                    else:
                        print("│  Error: Too many failed attempts")
                        print("└─ Access denied")
                        
            except KeyboardInterrupt:
                print("\n┌─ Authentication Cancelled")
                print("│  Action: Cancelled by user")
                print("└─ Exiting")
                return False
        
        print("\n┌─ Security Alert")
        print("│  Status: Maximum authentication attempts reached")
        print("│  Action: Application terminated for security")
        print("└─ Exiting")
        return False
    
    def change_password(self) -> bool:
        """Change existing password"""
        if not self.config.get("setup_complete"):
            print("┌─ Password Change")
            print("│  Error: No password set yet")
            print("│  Action: Run setup first")
            print("└─ Setup required")
            return False
        
        print("┌─ Password Change")
        print("│  Action: Verify current password")
        print("└─ Authentication required")
        
        try:
            current_password = getpass.getpass("│  Enter current password: ")
            if not self.verify_password(current_password):
                print("│  Error: Current password is incorrect")
                print("└─ Change cancelled")
                return False
            
            print("│  Status: Current password verified")
            print("└─ Set new password")
            
            while True:
                new_password = getpass.getpass("│  Enter new password: ")
                if len(new_password) < 6:
                    print("│  Error: Password must be at least 6 characters")
                    continue
                
                confirm_password = getpass.getpass("│  Confirm new password: ")
                if new_password != confirm_password:
                    print("│  Error: Passwords do not match")
                    continue
                
                # Update password
                self.config["password_hash"] = self.hash_password(new_password)
                if self.save_config():
                    print("┌─ Password Changed")
                    print("│  Status: Success")
                    print("│  Security: Password updated")
                    print("└─ Change complete")
                    return True
                else:
                    print("│  Error: Failed to save new password")
                    print("└─ Change failed")
                    return False
                    
        except KeyboardInterrupt:
            print("\n┌─ Password Change Cancelled")
            print("│  Action: Cancelled by user")
            print("└─ Exiting")
            return False

class DatabaseManager:
    """Handles database connections for SQLite, MySQL, and PostgreSQL"""
    
    def __init__(self):
        self.connection = None
        self.db_type = None
        self.connection_params = {}
        self.auto_commit = True
    
    def connect_sqlite(self, database_path: str) -> bool:
        """Connect to SQLite database"""
        try:
            self.connection = sqlite3.connect(database_path)
            self.db_type = "SQLite"
            self.connection_params = {"path": database_path}
            print(f"┌─ Connection Established")
            print(f"│  Database: SQLite")
            print(f"│  Path: {database_path}")
            print(f"│  Status: Connected")
            print(f"└─ Ready for queries")
            return True
        except Exception as e:
            print(f"┌─ Connection Failed")
            print(f"│  Error: {e}")
            print(f"│  Status: Disconnected")
            print(f"└─ Please check database path and permissions")
            return False
    
    def connect_mysql(self, host: str, user: str, password: str, database: str, port: int = 3306) -> bool:
        """Connect to MySQL database"""
        try:
            import mysql.connector
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.db_type = "MySQL"
            self.connection_params = {"host": host, "user": user, "database": database, "port": port}
            print(f"┌─ Connection Established")
            print(f"│  Database: MySQL {mysql.connector.__version__}")
            print(f"│  Host: {host}:{port}")
            print(f"│  User: {user}")
            print(f"│  Schema: {database}")
            print(f"│  Status: Connected")
            print(f"└─ Ready for queries")
            return True
        except ImportError:
            print(f"┌─ Connection Failed")
            print(f"│  Error: MySQL connector not installed")
            print(f"│  Solution: pip install mysql-connector-python")
            print(f"│  Status: Disconnected")
            print(f"└─ Install required dependencies")
            return False
        except Exception as e:
            print(f"┌─ Connection Failed")
            print(f"│  Error: {e}")
            print(f"│  Status: Disconnected")
            print(f"└─ Please check connection parameters")
            return False
    
    def connect_postgresql(self, host: str, user: str, password: str, database: str, port: int = 5432) -> bool:
        """Connect to PostgreSQL database"""
        try:
            import psycopg2
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.db_type = "PostgreSQL"
            self.connection_params = {"host": host, "user": user, "database": database, "port": port}
            print(f"┌─ Connection Established")
            print(f"│  Database: PostgreSQL {psycopg2.__version__}")
            print(f"│  Host: {host}:{port}")
            print(f"│  User: {user}")
            print(f"│  Database: {database}")
            print(f"│  Status: Connected")
            print(f"└─ Ready for queries")
            return True
        except ImportError:
            print(f"┌─ Connection Failed")
            print(f"│  Error: PostgreSQL connector not installed")
            print(f"│  Solution: pip install psycopg2-binary")
            print(f"│  Status: Disconnected")
            print(f"└─ Install required dependencies")
            return False
        except Exception as e:
            print(f"┌─ Connection Failed")
            print(f"│  Error: {e}")
            print(f"│  Status: Disconnected")
            print(f"└─ Please check connection parameters")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from database"""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
                print(f"┌─ Disconnection Complete")
                print(f"│  Database: {self.db_type}")
                print(f"│  Status: Disconnected")
                print(f"└─ Session ended")
                return True
            return False
        except Exception as e:
            print(f"┌─ Disconnection Failed")
            print(f"│  Error: {e}")
            print(f"│  Status: Error")
            print(f"└─ Please try again")
            return False
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.connection is not None and self.connection is not None
    
    def get_connection_status(self) -> str:
        """Get connection status message"""
        if self.is_connected():
            return f"Connected to {self.db_type}: {self.connection_params}"
        return "Not connected to any database"

class QueryHistory:
    """Manages query history"""
    
    def __init__(self, history_file: str = "query_history.json"):
        self.history_file = history_file
        self.history: List[Dict[str, Any]] = []
        self.load_history()
    
    def load_history(self):
        """Load query history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load history: {e}")
            self.history = []
    
    def save_history(self):
        """Save query history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history[-100:], f)  # Keep last 100 queries
        except Exception as e:
            print(f"Warning: Could not save history: {e}")
    
    def add_query(self, query: str, execution_time: float, rows_affected: int = 0, error: str = None):
        """Add query to history"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query.strip(),
            "execution_time": execution_time,
            "rows_affected": rows_affected,
            "error": error
        }
        self.history.append(history_entry)
        self.save_history()
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent query history"""
        return self.history[-limit:]
    
    def clear_history(self):
        """Clear query history"""
        self.history = []
        self.save_history()

class ResultExporter:
    """Handles exporting query results"""
    
    @staticmethod
    def export_to_csv(data: List[List], headers: List[str], filename: str) -> bool:
        """Export query results to CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if headers:
                    writer.writerow(headers)
                writer.writerows(data)
            print(f"✓ Results exported to {filename}")
            return True
        except Exception as e:
            print(f"✗ CSV export failed: {e}")
            return False
    
    @staticmethod
    def export_to_txt(data: List[List], headers: List[str], filename: str) -> bool:
        """Export query results to TXT file"""
        try:
            with open(filename, 'w', encoding='utf-8') as txtfile:
                if headers:
                    txtfile.write("\t".join(headers) + "\n")
                    txtfile.write("-" * (len("\t".join(headers))) + "\n")
                
                for row in data:
                    txtfile.write("\t".join(str(cell) for cell in row) + "\n")
            
            print(f"✓ Results exported to {filename}")
            return True
        except Exception as e:
            print(f"✗ TXT export failed: {e}")
            return False

class SQLExecutor:
    """Main SQL execution engine"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.query_history = QueryHistory()
        self.result_exporter = ResultExporter()
        self.password_manager = PasswordManager()
        self.running = True
    
    def format_tabular_output(self, data: List[List], headers: List[str]) -> str:
        """Format query results in tabular format"""
        if not data:
            return "┌─ Query Result\n│  Status: No rows found\n│  Rows: 0\n└─ End of result"
        
        # Calculate column widths
        all_rows = [headers] + data if headers else data
        col_widths = []
        for i in range(len(all_rows[0])):
            max_width = max(len(str(row[i])) for row in all_rows)
            col_widths.append(max_width + 2)
        
        # Create table with borders
        result = []
        
        # Top border
        if headers:
            top_border = "┌" + "┬".join("─" * width for width in col_widths) + "┐"
            result.append(top_border)
        
        # Header row
        if headers:
            header_row = "│" + "│".join(str(headers[i]).ljust(col_widths[i]) for i in range(len(headers))) + "│"
            result.append(header_row)
            
            # Separator
            separator = "├" + "┼".join("─" * width for width in col_widths) + "┤"
            result.append(separator)
        
        # Data rows
        for row in data:
            data_row = "│" + "│".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))) + "│"
            result.append(data_row)
        
        # Bottom border
        bottom_border = "└" + "┴".join("─" * width for width in col_widths) + "┘"
        result.append(bottom_border)
        
        return "\n".join(result)
    
    def validate_sql_safety(self, query: str) -> Tuple[bool, str]:
        """Validate SQL for safety concerns"""
        query_upper = query.upper().strip()
        
        # Check for DELETE without WHERE
        if "DELETE" in query_upper and "WHERE" not in query_upper:
            print("┌─ ⚠️  SECURITY WARNING")
            print("│  Operation: DELETE without WHERE clause")
            print("│  Risk: This will delete ALL rows in the table")
            print("│  Recommendation: Add WHERE clause to limit deletion")
            print("└─ Confirm to continue")
            if not self.get_user_confirmation("Continue with DELETE ALL? (y/N): "):
                return False, "DELETE operation cancelled by user"
        
        # Check for DROP TABLE
        if "DROP TABLE" in query_upper:
            print("┌─ ⚠️  SECURITY WARNING")
            print("│  Operation: DROP TABLE")
            print("│  Risk: This will permanently delete the table and all data")
            print("│  Recommendation: Backup data before dropping tables")
            print("└─ Confirm to continue")
            if not self.get_user_confirmation("Continue with DROP TABLE? (y/N): "):
                return False, "DROP TABLE operation cancelled by user"
        
        return True, ""
    
    def get_user_confirmation(self, message: str) -> bool:
        """Get user confirmation for risky operations"""
        try:
            response = input(message).strip().lower()
            return response in ['y', 'yes']
        except KeyboardInterrupt:
            return False
    
    def execute_query(self, query: str) -> Tuple[bool, Any]:
        """Execute SQL query and return results"""
        if not self.db_manager.is_connected():
            return False, "No database connection"
        
        # Validate safety
        is_safe, safety_message = self.validate_sql_safety(query)
        if not is_safe:
            return False, safety_message
        
        start_time = time.time()
        
        try:
            cursor = self.db_manager.connection.cursor()
            
            # Determine query type
            query_upper = query.upper().strip()
            
            if query_upper.startswith(('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN')):
                # Query that returns results
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Get column names
                if self.db_manager.db_type == "SQLite":
                    headers = [description[0] for description in cursor.description] if cursor.description else []
                elif self.db_manager.db_type == "MySQL":
                    headers = [column[0] for column in cursor.description] if cursor.description else []
                elif self.db_manager.db_type == "PostgreSQL":
                    headers = [desc[0] for desc in cursor.description] if cursor.description else []
                else:
                    headers = []
                
                execution_time = time.time() - start_time
                
                # Add to history
                self.query_history.add_query(query, execution_time, len(results))
                
                # Format and display results
                if results:
                    print("\n┌─ Query Results")
                    print(f"│  Rows returned: {len(results)}")
                    print(f"│  Execution time: {execution_time:.3f} seconds")
                    print("└─ Output:")
                    print(self.format_tabular_output(results, headers))
                    print(f"\n┌─ Query Summary")
                    print(f"│  Status: Success")
                    print(f"│  Rows: {len(results)}")
                    print(f"│  Time: {execution_time:.3f}s")
                    print(f"└─ Complete")
                else:
                    print("┌─ Query Result")
                    print("│  Status: Success")
                    print("│  Rows: 0")
                    print("│  Message: No rows found")
                    print("└─ End of result")
                
                return True, results
            
            else:
                # Query that doesn't return results (INSERT, UPDATE, DELETE, DDL)
                cursor.execute(query)
                rows_affected = cursor.rowcount
                
                if self.db_manager.auto_commit:
                    self.db_manager.connection.commit()
                
                execution_time = time.time() - start_time
                
                # Add to history
                self.query_history.add_query(query, execution_time, rows_affected)
                
                print("┌─ Query Execution Complete")
                print(f"│  Status: Success")
                print(f"│  Rows affected: {rows_affected}")
                print(f"│  Execution time: {execution_time:.3f} seconds")
                print(f"│  Auto-commit: {'ON' if self.db_manager.auto_commit else 'OFF'}")
                print("└─ Operation completed")
                
                return True, rows_affected
        
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"SQL Error: {e}"
            self.query_history.add_query(query, execution_time, 0, error_msg)
            
            print("┌─ Query Execution Failed")
            print(f"│  Status: Error")
            print(f"│  Error: {e}")
            print(f"│  Time: {execution_time:.3f}s")
            print("└─ Query terminated")
            
            return False, error_msg
    
    def handle_special_commands(self, command: str) -> bool:
        """Handle special CLI commands"""
        command = command.strip().lower()
        
        if command == "help":
            self.show_help()
            return True
        
        elif command == "exit":
            self.running = False
            print("┌─ Session Ending")
            print("│  Status: Disconnecting...")
            print("│  Message: Thank you for using SQL CLI")
            print("│  Action: Closing application")
            print("└─ Goodbye!")
            return True
        
        elif command == "changepassword":
            self.password_manager.change_password()
            return True
        
        elif command == "history":
            self.show_history()
            return True
        
        elif command == "clear":
            self.clear_screen()
            return True
        
        elif command.startswith("\\dt"):
            self.show_tables()
            return True
        
        elif command.startswith("\\d "):
            table_name = command[3:].strip()
            self.describe_table(table_name)
            return True
        
        elif command.startswith("connect "):
            self.handle_connect_command(command[8:])
            return True
        
        elif command.startswith("export "):
            self.handle_export_command(command[7:])
            return True
        
        elif command == "autocommit on":
            self.db_manager.auto_commit = True
            print("┌─ Auto-commit Settings")
            print("│  Status: Enabled")
            print("│  Behavior: Changes are committed immediately")
            print("└─ Setting updated")
            return True
        
        elif command == "autocommit off":
            self.db_manager.auto_commit = False
            print("┌─ Auto-commit Settings")
            print("│  Status: Disabled")
            print("│  Behavior: Manual commit required")
            print("│  Action: Use 'commit' or 'rollback'")
            print("└─ Setting updated")
            return True
        
        elif command == "commit":
            if self.db_manager.is_connected():
                try:
                    self.db_manager.connection.commit()
                    print("┌─ Transaction Control")
                    print("│  Action: Commit")
                    print("│  Status: Success")
                    print("│  Result: Changes saved permanently")
                    print("└─ Transaction completed")
                except Exception as e:
                    print(f"┌─ Transaction Error")
                    print(f"│  Action: Commit failed")
                    print(f"│  Error: {e}")
                    print("└─ Please try again")
            else:
                print("┌─ Transaction Error")
                print("│  Status: No database connection")
                print("│  Action: Connect to database first")
                print("└─ Connection required")
            return True
        
        elif command == "rollback":
            if self.db_manager.is_connected():
                try:
                    self.db_manager.connection.rollback()
                    print("┌─ Transaction Control")
                    print("│  Action: Rollback")
                    print("│  Status: Success")
                    print("│  Result: Changes discarded")
                    print("└─ Transaction cancelled")
                except Exception as e:
                    print(f"┌─ Transaction Error")
                    print(f"│  Action: Rollback failed")
                    print(f"│  Error: {e}")
                    print("└─ Please try again")
            else:
                print("┌─ Transaction Error")
                print("│  Status: No database connection")
                print("│  Action: Connect to database first")
                print("└─ Connection required")
            return True
        
        return False
    
    def handle_connect_command(self, params: str):
        """Handle database connection commands"""
        parts = params.split()
        if not parts:
            print("Usage: connect <db_type> <parameters>")
            print("Examples:")
            print("  connect sqlite mydb.db")
            print("  connect mysql localhost user password database")
            print("  connect postgresql localhost user password database")
            return
        
        db_type = parts[0].lower()
        
        if db_type == "sqlite" and len(parts) >= 2:
            self.db_manager.connect_sqlite(parts[1])
        
        elif db_type == "mysql" and len(parts) >= 5:
            self.db_manager.connect_mysql(parts[1], parts[2], parts[3], parts[4])
        
        elif db_type == "postgresql" and len(parts) >= 5:
            self.db_manager.connect_postgresql(parts[1], parts[2], parts[3], parts[4])
        
        else:
            print("Invalid connection parameters")
    
    def handle_export_command(self, params: str):
        """Handle export commands"""
        parts = params.split()
        if len(parts) < 2:
            print("Usage: export <csv|txt> <filename>")
            return
        
        export_type = parts[0].lower()
        filename = parts[1]
        
        # This would need to store the last query results
        print("Export functionality requires previous query results")
        print("Use: export csv filename.csv  (after running a SELECT query)")
    
    def show_help(self):
        """Display help information"""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                    COMMAND REFERENCE v1.0                   ║
╚══════════════════════════════════════════════════════════════╝

┌─ SECURITY COMMANDS
│  changepassword                  - Change application password
└─ 

┌─ DATABASE CONNECTION
│  connect sqlite <file>           - Connect to SQLite database
│  connect mysql <host> <user> <pass> <db> - Connect to MySQL
│  connect postgresql <host> <user> <pass> <db> - Connect to PostgreSQL
└─ 

┌─ SQL COMMANDS
│  Any valid SQL statement ending with semicolon (;)
│  Examples: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER
└─ 

┌─ USER COMMANDS
│  help                            - Show this help
│  history                         - Show query history
│  clear                           - Clear terminal screen
│  exit                            - Exit application
└─ 

┌─ TRANSACTION CONTROL
│  commit                          - Commit current transaction
│  rollback                        - Rollback current transaction
│  autocommit on/off               - Toggle auto-commit mode
└─ 

┌─ SHORTCUT COMMANDS
│  \\dt                            - Show all tables
│  \\d <table_name>                - Describe table structure
└─ 

┌─ EXPORT COMMANDS
│  export csv <filename>           - Export last query to CSV
│  export txt <filename>           - Export last query to TXT
└─ 

┌─ EXAMPLES
│  connect sqlite test.db
│  CREATE TABLE users (id INTEGER, name TEXT);
│  INSERT INTO users VALUES (1, 'Alice');
│  SELECT * FROM users;
└─ 

╔══════════════════════════════════════════════════════════════╗
║           Professional SQL CLI - Happy Querying!            ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(help_text)
    
    def show_history(self):
        """Display query history"""
        history = self.query_history.get_history()
        if not history:
            print("┌─ Query History")
            print("│  Status: No history available")
            print("│  Message: Start executing queries to build history")
            print("└─ End of history")
            return
        
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║                    QUERY HISTORY                             ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        
        for i, entry in enumerate(history, 1):
            timestamp = entry['timestamp'][:19]  # Remove microseconds
            query = entry['query'][:50] + "..." if len(entry['query']) > 50 else entry['query']
            status = "SUCCESS" if not entry.get('error') else "ERROR"
            time_taken = f"{entry['execution_time']:.3f}s"
            rows = entry['rows_affected'] if entry['rows_affected'] > 0 else "N/A"
            
            print(f"┌─ Entry #{i}")
            print(f"│  Time: {timestamp}")
            print(f"│  Status: {status}")
            print(f"│  Duration: {time_taken}")
            print(f"│  Rows: {rows}")
            print(f"│  Query: {query}")
            print("└─")
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║           End of Query History                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
    
    def show_tables(self):
        """Show all tables in the database"""
        if not self.db_manager.is_connected():
            print("┌─ Database Connection Required")
            print("│  Status: Not connected")
            print("│  Action: Use 'connect' command first")
            print("└─ Connection needed")
            return
        
        print("┌─ Retrieving Table List")
        print("│  Database: " + self.db_manager.db_type)
        print("│  Status: Querying...")
        print("└─ Processing")
        
        if self.db_manager.db_type == "SQLite":
            self.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
        elif self.db_manager.db_type == "MySQL":
            self.execute_query("SHOW TABLES;")
        elif self.db_manager.db_type == "PostgreSQL":
            self.execute_query("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    
    def describe_table(self, table_name: str):
        """Describe table structure"""
        if not self.db_manager.is_connected():
            print("┌─ Database Connection Required")
            print("│  Status: Not connected")
            print("│  Action: Use 'connect' command first")
            print("└─ Connection needed")
            return
        
        print(f"┌─ Table Structure: {table_name}")
        print(f"│  Database: {self.db_manager.db_type}")
        print(f"│  Status: Querying...")
        print("└─ Processing")
        
        if self.db_manager.db_type == "SQLite":
            self.execute_query(f"PRAGMA table_info({table_name});")
        elif self.db_manager.db_type == "MySQL":
            self.execute_query(f"DESCRIBE {table_name};")
        elif self.db_manager.db_type == "PostgreSQL":
            self.execute_query(f"\\d {table_name};")
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run(self):
        """Main application loop"""
        # Authenticate user first
        if not self.password_manager.authenticate():
            return
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║         COMMAND-BASED PYTHON SQL EXECUTOR v1.0               ║
║         Professional Database Management Tool                ║
╚══════════════════════════════════════════════════════════════╝

Type 'help' for available commands or 'exit' to quit
        """)
        
        while self.running:
            try:
                # Show connection status in prompt
                status = "✓" if self.db_manager.is_connected() else "✗"
                prompt = f"{status}sql> "
                
                # Get user input
                user_input = input(prompt)
                
                # Handle empty input
                if not user_input.strip():
                    continue
                
                # Handle special commands
                if self.handle_special_commands(user_input):
                    continue
                
                # Handle multi-line SQL input
                if not user_input.strip().endswith(';'):
                    # Multi-line query
                    query_lines = [user_input]
                    while True:
                        try:
                            line = input("...> ")
                            if line.strip().endswith(';'):
                                query_lines.append(line)
                                break
                            query_lines.append(line)
                        except KeyboardInterrupt:
                            print("\nQuery cancelled")
                            break
                    query = '\n'.join(query_lines)
                else:
                    # Single-line query
                    query = user_input
                
                # Execute SQL query
                if query.strip().endswith(';'):
                    self.execute_query(query)
                else:
                    print("Query must end with semicolon (;)")
                
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main entry point"""
    executor = SQLExecutor()
    executor.run()

if __name__ == "__main__":
    main()
