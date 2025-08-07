#!/usr/bin/env python3
"""
Script to reset admin password in the database
"""

import os
import mysql.connector
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

def reset_admin_password():
    """Reset the admin password to a new value"""
    
    # Get new password from user
    new_password = input("Enter new admin password: ")
    confirm_password = input("Confirm new password: ")
    
    if new_password != confirm_password:
        print("❌ Passwords don't match!")
        return
    
    if len(new_password) < 6:
        print("❌ Password should be at least 6 characters long!")
        return
    
    # Generate hash
    password_hash = generate_password_hash(new_password)
    print(f"Generated hash: {password_hash}")
    
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        cursor = connection.cursor()
        
        # Update admin password
        update_query = "UPDATE user SET password_hash = %s WHERE username = 'admin'"
        cursor.execute(update_query, (password_hash,))
        
        if cursor.rowcount > 0:
            connection.commit()
            print(f"✅ Admin password updated successfully!")
            print(f"New password: {new_password}")
        else:
            print("❌ No admin user found to update")
            
            # Ask if user wants to create admin user
            create_admin = input("Do you want to create an admin user? (y/n): ")
            if create_admin.lower() == 'y':
                insert_query = """
                INSERT INTO user (username, email, password_hash) 
                VALUES ('admin', 'admin@hoahuongduong.edu.vn', %s)
                """
                cursor.execute(insert_query, (password_hash,))
                connection.commit()
                print(f"✅ Admin user created successfully!")
                print(f"Username: admin")
                print(f"Password: {new_password}")
        
    except mysql.connector.Error as error:
        print(f"❌ Database error: {error}")
    except Exception as error:
        print(f"❌ Error: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def show_current_admin_info():
    """Show current admin user information"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, email, password_hash FROM user WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result:
            print("Current admin user info:")
            print(f"ID: {result[0]}")
            print(f"Username: {result[1]}")
            print(f"Email: {result[2]}")
            print(f"Password Hash: {result[3]}")
        else:
            print("❌ No admin user found in database")
            
    except mysql.connector.Error as error:
        print(f"❌ Database error: {error}")
    except Exception as error:
        print(f"❌ Error: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    print("Admin Password Management Tool")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Show current admin info")
        print("2. Reset admin password")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            show_current_admin_info()
        elif choice == '2':
            reset_admin_password()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
