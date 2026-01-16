# COMMAND-BASED PYTHON SQL EXECUTOR

A lightweight, terminal-based SQL execution tool built using Python.  
This software allows users to connect to databases and execute SQL commands directly from the command line without any GUI.

---

## ✨ FEATURES

### 1. Database Management
- Supports multiple databases:
  - SQLite
  - MySQL
  - PostgreSQL
- Secure database connection handling
- Connect and disconnect functionality
- Clear connection status messages

---

### 2. SQL Command Interface
- Interactive command prompt (`sql>`)
- Supports single-line SQL commands
- Supports multi-line SQL queries
- SQL execution triggered using semicolon (`;`)

---

### 3. SQL Query Execution
- Supports all major SQL commands:

#### DDL Commands
- CREATE
- DROP
- ALTER

#### DML Commands
- SELECT
- INSERT
- UPDATE
- DELETE

#### Transaction Commands
- COMMIT
- ROLLBACK

---

### 4. Result Handling
- SELECT query results displayed in tabular format
- Shows number of rows affected for INSERT, UPDATE, DELETE
- Displays query execution time

---

### 5. Error Handling & Validation
- SQL syntax error handling
- Database connection error handling
- Invalid command detection with meaningful messages

---

### 6. Query History Management
- Automatically saves executed SQL queries
- View query history using command
- Ability to re-execute previous queries

---

### 7. Security & Safety Features
- Warning for DELETE commands without WHERE clause
- Confirmation required before DROP TABLE
- User confirmation prompts for risky operations

---

### 8. Export & Logging
- Export query results to CSV format
- Export query results to TXT format
- Maintains query and error logs

---

### 9. User Commands
- `help`    → Displays available commands
- `exit`    → Closes the application
- `history` → Shows executed query history
- `clear`   → Clears the terminal screen

---

### 10. Optional Advanced Features
- Switch database at runtime
- Command shortcuts:
  - `\dt` → Show all tables
  - `\d table_name` → Describe table structure
- Auto-commit ON/OFF mode

---

## 🛠 Technologies Used
- Python 3
- SQLite / MySQL / PostgreSQL
- Standard Python Libraries

---

## 🎯 Project Use Case
- College / University DBMS project
- Learning SQL and database interaction
- Command-line database administration tool

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.6 or higher
- Optional database connectors (for MySQL/PostgreSQL)

### Install Optional Dependencies
```bash
# For MySQL support
pip install mysql-connector-python

# For PostgreSQL support
pip install psycopg2-binary
```

### Running the Application
```bash
cd sql_cli
python main.py
```

---

## 🚀 Usage Guide

### 1. Start the Application
```bash
python main.py
```

### 2. Connect to a Database

#### SQLite (Built-in)
```sql
connect sqlite mydatabase.db
```

#### MySQL
```sql
connect mysql localhost username password database_name
```

#### PostgreSQL
```sql
connect postgresql localhost username password database_name
```

### 3. Execute SQL Commands

#### Create a Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER
);
```

#### Insert Data
```sql
INSERT INTO users (name, email, age) 
VALUES ('Alice', 'alice@example.com', 25);
```

#### Query Data
```sql
SELECT * FROM users;
SELECT name, age FROM users WHERE age > 20;
```

#### Update Data
```sql
UPDATE users SET age = 26 WHERE name = 'Alice';
```

#### Delete Data
```sql
DELETE FROM users WHERE id = 1;
```

### 4. Multi-line Queries
```sql
sql> SELECT name, email,
...> FROM users
...> WHERE age > 20
...> ORDER BY name;
```

### 5. Transaction Management
```sql
autocommit off          -- Disable auto-commit
INSERT INTO users ...   -- Make changes
COMMIT                  -- Commit changes
-- or
ROLLBACK                -- Rollback changes
```

---

## 📋 Available Commands

### Database Connection
- `connect sqlite <file>` - Connect to SQLite database
- `connect mysql <host> <user> <pass> <db>` - Connect to MySQL
- `connect postgresql <host> <user> <pass> <db>` - Connect to PostgreSQL

### User Commands
- `help` - Show help information
- `history` - Show query history
- `clear` - Clear terminal screen
- `exit` - Exit application

### Security Commands
- `changepassword` - Change application password

### Transaction Commands
- `commit` - Commit current transaction
- `rollback` - Rollback current transaction
- `autocommit on/off` - Toggle auto-commit mode

### Shortcut Commands
- `\dt` - Show all tables in current database
- `\d table_name` - Describe table structure

### Export Commands
- `export csv filename.csv` - Export last query results to CSV
- `export txt filename.txt` - Export last query results to TXT

---

## 🔒 SECURITY FEATURES

### Password Protection
The application now includes robust password protection for enhanced security:

#### First-Time Setup
- **Automatic Setup**: On first run, the application prompts for password setup
- **Minimum Requirements**: Password must be at least 6 characters long
- **Secure Storage**: Passwords are hashed using SHA-256 encryption
- **Configuration File**: `sql_cli_config.json` stores encrypted credentials

#### Authentication Process
- **Startup Protection**: Application requires password authentication on every launch
- **Multiple Attempts**: Users get 3 attempts to enter the correct password
- **Security Lockout**: Application terminates after 3 failed attempts
- **Session Security**: Password required for each new session

#### Password Management
- **Change Password**: Use `changepassword` command to update password
- **Current Verification**: Must enter current password to set new one
- **Password Confirmation**: New password must be confirmed twice
- **Secure Updates**: Password changes are immediately encrypted and saved

### DELETE Protection
The application warns before executing DELETE statements without WHERE clause:
```
WARNING: You are about to DELETE all rows. Continue? (y/N):
```

### DROP TABLE Protection
Confirmation required before dropping tables:
```
WARNING: You are about to DROP a table. Continue? (y/N):
```

### Query History
All executed queries are automatically logged in `query_history.json` for audit purposes.

---

## 📊 Example Session

```bash
$ python main.py

╔══════════════════════════════════════════════════════════════╗
║                 SQL CLI - FIRST TIME SETUP                   ║
║                 Professional Database Tool                   ║
╚══════════════════════════════════════════════════════════════╝

┌─ Security Setup
│  Action: Set administrator password
│  Purpose: Protect application access
│  Requirement: Minimum 6 characters
└─ Please configure

┌─ Enter new password: ******
┌─ Confirm password: ******
┌─ Setup Complete
│  Status: Password configured successfully
│  Security: Application is now protected
└─ Setup finished

╔══════════════════════════════════════════════════════════════╗
║                 SQL CLI - AUTHENTICATION                     ║
║                 Professional Database Tool                   ║
╚══════════════════════════════════════════════════════════════╝

┌─ Authentication Required
│  Attempt: 1 of 3
│  Enter password: ******
┌─ Authentication Success
│  Status: Access granted
│  Welcome: Authorized user
└─ Loading application

╔══════════════════════════════════════════════════════════════╗
║         COMMAND-BASED PYTHON SQL EXECUTOR v1.0               ║
║         Professional Database Management Tool                ║
╚══════════════════════════════════════════════════════════════╝

Type 'help' for available commands or 'exit' to quit

✓sql> connect sqlite test.db
┌─ Connection Established
│  Database: SQLite
│  Path: test.db
│  Status: Connected
└─ Ready for queries

✓sql> CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
┌─ Query Execution Complete
│  Status: Success
│  Rows affected: 0
│  Execution time: 0.001 seconds
│  Auto-commit: ON
└─ Operation completed

✓sql> INSERT INTO users VALUES (1, 'Alice');
┌─ Query Execution Complete
│  Status: Success
│  Rows affected: 1
│  Execution time: 0.001 seconds
│  Auto-commit: ON
└─ Operation completed

✓sql> SELECT * FROM users;

┌─ Query Results
│  Rows returned: 1
│  Execution time: 0.000 seconds
└─ Output:
┌──────┬───────┐
│ id   │ name  │
├──────┼───────┤
│ 1    │ Alice │
└──────┴───────┘

┌─ Query Summary
│  Status: Success
│  Rows: 1
│  Time: 0.000s
└─ Complete

✓sql> changepassword
┌─ Password Change
│  Action: Verify current password
└─ Authentication required

│  Enter current password: ******
│  Status: Current password verified
└─ Set new password

│  Enter new password: ******
│  Confirm new password: ******
┌─ Password Changed
│  Status: Success
│  Security: Password updated
└─ Change complete

✓sql> exit
┌─ Session Ending
│  Status: Disconnecting...
│  Message: Thank you for using SQL CLI
│  Action: Closing application
└─ Goodbye!
```

---

## 📁 Project Structure

```
sql_cli/
├── main.py                    # Main application file
├── README.md                  # This documentation
├── sql_cli_config.json        # Password configuration (auto-generated)
├── query_history.json         # Query history storage (auto-generated)
├── 1_Database_Management/     # Database connection modules
├── 2_SQL_Command_Interface/   # Command interface modules
├── 3_SQL_Query_Execution/     # Query execution modules
├── 4_Result_Handling/         # Result display modules
├── 5_Error_Handling_Validation/ # Error handling modules
├── 6_Query_History_Management/ # History management modules
├── 7_Security_Safety/         # Security features modules
├── 8_Export_Logging/          # Export and logging modules
├── 9_User_Commands/           # User command modules
└── 10_Optional_Advanced_Features/ # Advanced features modules
```

---

## 🐛 Troubleshooting

### Common Issues

1. **MySQL/PostgreSQL Connection Errors**
   - Ensure database connectors are installed
   - Verify database is running and accessible
   - Check connection parameters

2. **Permission Errors**
   - Ensure write permissions for current directory
   - Check database file permissions

3. **SQL Syntax Errors**
   - Ensure queries end with semicolon (;)
   - Check SQL syntax for your specific database

### Error Messages
- `✗ SQLite connection failed: ...` - Database file not found or permission issue
- `✗ MySQL connector not installed` - Install mysql-connector-python
- `✗ PostgreSQL connector not installed` - Install psycopg2-binary
- `SQL Error: ...` - SQL syntax or execution error

---

## 🤝 Contributing

This project is designed for educational purposes and DBMS learning. Feel free to:
- Report bugs and issues
- Suggest new features
- Improve documentation
- Add database support

---

## 📝 License

This project is open-source and available for educational and non-commercial use.

---

## 🎓 Educational Use

Perfect for:
- College DBMS projects
- SQL learning and practice
- Database administration tasks
- Command-line interface development

**Happy SQL querying! 🚀**
<br><br>
<img src-"<img width="1366" height="640" alt="image" src="https://github.com/user-attachments/assets/3596b4cd-fdef-41be-b49a-dd115f593113" />
"

