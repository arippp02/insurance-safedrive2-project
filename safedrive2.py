import mysql.connector
import logging
from tabulate import tabulate
from datetime import datetime, timedelta

# Create a connection to the MySQL database
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="safedrive2"  # Updated database name here
        )
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Database connection error: {err}")
        raise

# Display the main menu
def main_menu():
    while True:
        print("\n--- SafeDrive Menu ---")
        print("+-------+-------------------------+")
        print("|   No. | Module                  |")
        print("+=======+=========================+")
        print("|     1 | Policyholder Management |")
        print("|     2 | Policy Management       |")
        print("|     3 | Vehicle Management      |")
        print("|     4 | Application Management  |")
        print("|     5 | Claim Management        |")
        print("|     6 | Reports & Analytics     |")
        print("|     0 | Exit                    |")
        print("+-------+-------------------------+")
        choice = input("Enter your choice: ")

        if choice == "1":
            policyholder_management()
        elif choice == "2":
            policy_management()
        elif choice == "3":
            vehicle_management()
        elif choice == "4":
            application_management()
        elif choice == "5":
            claim_management()
        elif choice == "6":
            reports_and_analytics()
        elif choice == "0":
            break
        else:
            print("Invalid choice! Please try again.")

# Placeholder for Policyholder Management
def policyholder_management():
    while True:
        print("\n--- Policyholder Management ---")
        print("+-------+-------------------------+")
        print("|   No. | Action                  |")
        print("+=======+=========================+")
        print("|     1 | Add New Policyholder    |")
        print("|     2 | View Policyholders      |")
        print("|     3 | Update Policyholder     |")
        print("|     4 | Delete Policyholder     |")
        print("|     0 | Return to Main Menu     |")
        print("+-------+-------------------------+")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_policyholder()
        elif choice == "2":
            view_policyholders()
        elif choice == "3":
            update_policyholder()
        elif choice == "4":
            delete_policyholder()
        elif choice == "0":
            return
        else:
            print("Invalid choice! Please try again.")

def add_policyholder():
    print("\n--- Add New Policyholder ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Fetch available Application IDs from the database
        cursor.execute("SELECT Application_ID, Purpose, ApprovalStatus FROM application")
        applications = cursor.fetchall()

        if not applications:
            print("No applications found. Please add applications before proceeding.")
            return

        # Display available Application IDs
        print("\nAvailable Applications:")
        print("+----------------+----------------------------------+-------------------+")
        print("| Application ID | Purpose                          | Approval Status    |")
        print("+----------------+----------------------------------+-------------------+")
        for app in applications:
            print(f"| {app[0]:<14} | {app[1]:<32} | {app[2]:<17} |")
        print("+----------------+----------------------------------+-------------------+")

        # Step 3: Prompt user for policyholder details
        name = input("Enter Policyholder Name: ").strip()
        application_id = input("Enter Application ID (linked to this policyholder): ").strip()
        contact_details = input("Enter Contact Details (e.g., phone/email): ").strip()
        dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
        license_number = input("Enter Driving License Number: ").strip()

        # Validate inputs (basic validation; extend as needed)
        if not name or not application_id or not contact_details or not dob or not license_number:
            print("All fields are required. Please try again.")
            return

        # Step 4: Check if the application ID exists
        cursor.execute("SELECT ApprovalStatus FROM application WHERE Application_ID = %s", (application_id,))
        app_status = cursor.fetchone()

        if not app_status:
            print(f"Error: Application ID {application_id} does not exist.")
            return

        # Removed the check for "Approved" status, now we allow all statuses
        print(f"Note: Application ID {application_id} has the status: {app_status[0]}")

        # Step 5: Insert into the policyholder table
        query = """
        INSERT INTO policyholder 
        (Policyholder_Name, Application_ID, ContactDetails, DateOfBirth, DrivingLicenseNumber)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, application_id, contact_details, dob, license_number))
        conn.commit()

        # Get the auto-generated ID
        new_policyholder_id = cursor.lastrowid
        print(f"\nPolicyholder added successfully!")
        print(f"Assigned Policyholder ID: {new_policyholder_id}")

        # Display the newly added policyholder details
        print("\nNew Policyholder Details:")
        print("+-----------------+------------------------+")
        print("| Field           | Value                  |")
        print("+-----------------+------------------------+")
        print(f"| Policyholder ID | {new_policyholder_id:<22} |")
        print(f"| Name           | {name:<22} |")
        print(f"| Application ID | {application_id:<22} |")
        print(f"| Contact        | {contact_details:<22} |")
        print(f"| Date of Birth  | {dob:<22} |")
        print(f"| License Number | {license_number:<22} |")
        print("+-----------------+------------------------+")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def view_policyholders():
    print("\n--- View Policyholders ---")

    try:
        conn = create_connection()
        cursor = conn.cursor()
        # Query to fetch relevant policyholder data
        query = """
        SELECT 
            Policyholder_ID, 
            Policyholder_Name, 
            Application_ID, 
            ContactDetails, 
            DateOfBirth, 
            DrivingLicenseNumber 
        FROM policyholder;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Check if there are any records
        if not results:
            print("No policyholders found.")
            return

        # Display results in a table format with fixed-width columns
        print("+----------------+------------------------+----------------+------------------------+----------------+-------------------------+")
        print("| Policyholder ID | Policyholder Name      | Application ID | Contact Details        | Date of Birth  | Driving License No      |")
        print("+----------------+------------------------+----------------+------------------------+----------------+-------------------------+")
        
        # Use fixed-width formatting for better alignment
        for row in results:
            # Format the date properly (ensure it fits the fixed-width column)
            dob = row[4].strftime('%Y-%m-%d') if row[4] else "N/A"
            print(f"| {row[0]:<16} | {row[1]:<22} | {row[2]:<14} | {row[3]:<22} | {dob:<14} | {row[5]:<23} |")
        
        print("+----------------+------------------------+----------------+------------------------+----------------+-------------------------+")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

def delete_policyholder():
    print("\n--- Delete Policyholder ---")
    
    try:
        # Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Fetch and display all available Policyholder IDs
        cursor.execute("SELECT Policyholder_ID, Policyholder_Name FROM policyholder")
        policyholders = cursor.fetchall()

        if not policyholders:
            print("No policyholders found!")
            return
        
        # Display available policyholders
        print("\nAvailable Policyholders:")
        print("+------------------+-------------------------+")
        print("| Policyholder ID  | Policyholder Name       |")
        print("+------------------+-------------------------+")
        for record in policyholders:
            print(f"| {record[0]:<16} | {record[1]:<23} |")
        print("+------------------+-------------------------+")
        
        # Ask for Policyholder ID to delete
        policyholder_id = int(input("\nEnter Policyholder ID to delete: "))
        
        # Check if the policyholder exists and get full details
        cursor.execute("SELECT * FROM policyholder WHERE Policyholder_ID = %s", (policyholder_id,))
        existing_record = cursor.fetchone()

        if not existing_record:
            print("Policyholder not found!")
            return
        
        # Format Date of Birth for display
        date_of_birth = existing_record[4]
        if isinstance(date_of_birth, datetime):
            formatted_dob = date_of_birth.strftime('%Y-%m-%d')
        else:
            formatted_dob = str(date_of_birth)
        
        # Show policyholder details before deletion
        print("\nPolicyholder details to be deleted:")
        print("+------------------+-------------------------+")
        print("| Field            | Value                   |")
        print("+------------------+-------------------------+")
        print(f"| Policyholder ID  | {existing_record[0]:<23} |")
        print(f"| Name             | {existing_record[1]:<23} |")
        print(f"| Application ID   | {existing_record[2]:<23} |")
        print(f"| Contact Details  | {existing_record[3]:<23} |")
        print(f"| Date of Birth    | {formatted_dob:<23} |")
        print(f"| License No       | {existing_record[5]:<23} |")
        print("+------------------+-------------------------+")
        
        # Check for related vehicles
        cursor.execute("SELECT COUNT(*) FROM vehicle WHERE Policyholder_ID = %s", (policyholder_id,))
        vehicle_count = cursor.fetchone()[0]
        
        if vehicle_count > 0:
            print(f"\nWarning: This policyholder has {vehicle_count} vehicle(s) registered.")
            print("Deleting this policyholder will also delete all associated vehicle records.")
        
        # Confirm deletion
        confirm = input("\nAre you sure you want to delete this policyholder? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("\nDeletion cancelled.")
            return
        
        # Delete the policyholder record (cascade will handle related records if defined)
        delete_query = "DELETE FROM policyholder WHERE Policyholder_ID = %s"
        cursor.execute(delete_query, (policyholder_id,))
        conn.commit()

        print(f"\nPolicyholder ID {policyholder_id} deleted successfully!")
        if vehicle_count > 0:
            print(f"Associated vehicle records have also been deleted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_policyholder():
    print("\n--- Delete Policyholder ---")
    
    try:
        # Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Fetch and display all available Policyholder IDs
        cursor.execute("SELECT Policyholder_ID, Policyholder_Name FROM policyholder")
        policyholders = cursor.fetchall()

        if not policyholders:
            print("No policyholders found!")
            return
        
        # Display available policyholders
        print("\nAvailable Policyholders:")
        print("+------------------+-------------------------+")
        print("| Policyholder ID  | Policyholder Name       |")
        print("+------------------+-------------------------+")
        for record in policyholders:
            print(f"| {record[0]:<16} | {record[1]:<23} |")
        print("+------------------+-------------------------+")
        
        # Ask for Policyholder ID to delete
        policyholder_id = int(input("\nEnter Policyholder ID to delete: "))
        
        # Check if the policyholder exists and get full details
        cursor.execute("SELECT * FROM policyholder WHERE Policyholder_ID = %s", (policyholder_id,))
        existing_record = cursor.fetchone()

        if not existing_record:
            print("Policyholder not found!")
            return
        
        # Format Date of Birth for display
        date_of_birth = existing_record[4]
        if isinstance(date_of_birth, datetime):
            formatted_dob = date_of_birth.strftime('%Y-%m-%d')
        else:
            formatted_dob = str(date_of_birth)
        
        # Show policyholder details before deletion
        print("\nPolicyholder details to be deleted:")
        print("+------------------+-------------------------+")
        print("| Field            | Value                   |")
        print("+------------------+-------------------------+")
        print(f"| Policyholder ID  | {existing_record[0]:<23} |")
        print(f"| Name             | {existing_record[1]:<23} |")
        print(f"| Application ID   | {existing_record[2]:<23} |")
        print(f"| Contact Details  | {existing_record[3]:<23} |")
        print(f"| Date of Birth    | {formatted_dob:<23} |")
        print(f"| License No       | {existing_record[5]:<23} |")
        print("+------------------+-------------------------+")
        
        # Check for related vehicles
        cursor.execute("SELECT COUNT(*) FROM vehicle WHERE Policyholder_ID = %s", (policyholder_id,))
        vehicle_count = cursor.fetchone()[0]
        
        if vehicle_count > 0:
            print(f"\nWarning: This policyholder has {vehicle_count} vehicle(s) registered.")
            print("Deleting this policyholder will also delete all associated vehicle records.")
        
        # Confirm deletion
        confirm = input("\nAre you sure you want to delete this policyholder? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("\nDeletion cancelled.")
            return
        
        # Delete the policyholder record (cascade will handle related records)
        delete_query = "DELETE FROM policyholder WHERE Policyholder_ID = %s"
        cursor.execute(delete_query, (policyholder_id,))
        conn.commit()

        print(f"\nPolicyholder ID {policyholder_id} deleted successfully!")
        if vehicle_count > 0:
            print(f"Associated vehicle records have also been deleted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Policy Management menu
def policy_management():
    while True:
        print("\n--- Policy Management ---")
        print("+-------+-----------------------+")
        print("|   No. | Action                |")
        print("+=======+=======================+")
        print("|     1 | Add New Policy        |")
        print("|     2 | View Policies         |")
        print("|     3 | Update Policy         |")
        print("|     4 | Delete Policy         |")
        print("|     0 | Return to Main Menu   |")
        print("+-------+-----------------------+")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_policy()
        elif choice == "2":
            view_policies()
        elif choice == "3":
            update_policy()
        elif choice == "4":
            delete_policy()
        elif choice == "0":
            return
        else:
            print("Invalid choice! Please try again.")

# Add New Policy
def add_policy():
    print("\n--- Add New Policy ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Fetch available policy types
        cursor.execute("SELECT PolicyType_ID, PolicyType_Name FROM policytype")
        policy_types = cursor.fetchall()

        if not policy_types:
            print("No policy types found. Please add policy types before proceeding.")
            return

        # Display available policy types
        print("\nAvailable Policy Types:")
        for pt in policy_types:
            print(f"ID: {pt[0]}, Name: {pt[1]}")

        # Step 3: Prompt user for policy details
        policy_type_id = input("Enter the Policy Type ID: ").strip()
        start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
        end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
        premium_amount = input("Enter Premium Amount: ").strip()

        # Validate inputs
        if not policy_type_id or not start_date or not end_date or not premium_amount:
            print("All fields are required. Please try again.")
            return

        # Step 4: Insert the new policy into the policy table
        query = """
            INSERT INTO policy (PolicyType, StartDate, EndDate, PremiumAmount)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (policy_type_id, start_date, end_date, premium_amount))
        conn.commit()

        # Get the last inserted Policy_ID
        policy_id = cursor.lastrowid

        # Step 5: Add policy-specific details based on the selected policy type
        if policy_type_id == "2":
            # Third-party Policy
            liability_coverage = input("Enter Liability Coverage Amount: ").strip()
            injury_coverage = input("Enter Injury Coverage Amount: ").strip()

            if not liability_coverage or not injury_coverage:
                print("All fields for Third-party Policy are required. Please try again.")
                return

            thirdparty_query = """
                INSERT INTO thirdparty_policy (Policy_ID, LiabilityCoverage, InjuryCoverage)
                VALUES (%s, %s, %s);
            """
            cursor.execute(thirdparty_query, (policy_id, liability_coverage, injury_coverage))

            # Display covered items for Third-party Policy
            print(f"\nCoverage Amounts:\n - Liability Coverage: {liability_coverage}\n - Injury Coverage: {injury_coverage}")

        elif policy_type_id == "1":
            # Comprehensive Policy
            accident_coverage = input("Enter Accident Coverage Amount: ").strip()
            theft_coverage = input("Enter Theft Coverage Amount: ").strip()
            glass_coverage = input("Enter Glass Coverage Amount: ").strip()

            if not accident_coverage or not theft_coverage or not glass_coverage:
                print("All fields for Comprehensive Policy are required. Please try again.")
                return

            comprehensive_query = """
                INSERT INTO comprehensive_policy (Policy_ID, AccidentCoverage, TheftCoverage, GlassCoverage)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(comprehensive_query, (policy_id, accident_coverage, theft_coverage, glass_coverage))

            # Display covered items for Comprehensive Policy
            print(f"\nCoverage Amounts:\n - Accident Coverage: {accident_coverage}\n - Theft Coverage: {theft_coverage}\n - Glass Coverage: {glass_coverage}")

        else:
            print("Invalid Policy Type ID. No additional policy details were added.")
            return

        # Commit the changes
        conn.commit()
        print("Policy added successfully, including additional details!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# View Policies
def view_policies():
    print("\n--- View Policies ---")
    
    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Fetch detailed coverage amounts for all policies
        query = """
        SELECT p.Policy_ID, pt.PolicyType_Name, 
               DATE_FORMAT(p.StartDate, '%Y-%m-%d') AS StartDate,
               DATE_FORMAT(p.EndDate, '%Y-%m-%d') AS EndDate,
               p.PremiumAmount, p.CoverageAmount,
               c.Coverage_Type, c.Coverage_Amount
        FROM policy p
        JOIN policytype pt ON p.PolicyType = pt.PolicyType_ID
        LEFT JOIN policy_coverage c ON p.Policy_ID = c.Policy_ID
        """
        cursor.execute(query)
        policies = cursor.fetchall()

        if not policies:
            print("No policies found.")
            return

        # Step 3: Organize data to calculate totals and display detailed coverage
        total_coverage = {}  # Stores total amounts per coverage type
        policy_details = {}  # Stores detailed coverage info per policy

        for row in policies:
            policy_id = row[0]
            if policy_id not in policy_details:
                # Initialize new policy entry
                policy_details[policy_id] = {
                    "PolicyType": row[1],
                    "StartDate": row[2],
                    "EndDate": row[3],
                    "PremiumAmount": row[4],
                    "CoverageAmount": row[5],
                    "DetailedCoverage": []
                }

            # Add coverage details for this policy
            if row[6]:  # If coverage type is not NULL
                coverage_type = row[6]
                coverage_amount = row[7]
                policy_details[policy_id]["DetailedCoverage"].append(f"{coverage_type}: {coverage_amount:.2f}")

                # Update total coverage amounts
                total_coverage[coverage_type] = total_coverage.get(coverage_type, 0) + coverage_amount

        # Step 4: Display policies in a properly formatted table
        print("+-------------+---------------------+--------------+--------------+------------------+-------------------+-----------------------------------+")
        print("|   Policy ID | Policy Type         | Start Date   | End Date     |   Premium Amount |   Coverage Amount | Detailed Coverage                 |")
        print("+=============+=====================+==============+==============+==================+===================+===================================+")
        for policy_id, details in policy_details.items():
            premium_amount = f"{details['PremiumAmount']:.2f}" if details['PremiumAmount'] is not None else "0.00"
            coverage_amount = f"{details['CoverageAmount']:.2f}" if details['CoverageAmount'] is not None else "0.00"
            detailed_coverage = "; ".join(details["DetailedCoverage"]) if details["DetailedCoverage"] else "None"
            print(f"| {policy_id:<11} | {details['PolicyType']:<19} | {details['StartDate']:<12} | {details['EndDate']:<12} | {premium_amount:>16} | {coverage_amount:>17} | {detailed_coverage:<35} |")
        print("+-------------+---------------------+--------------+--------------+------------------+-------------------+-----------------------------------+")

        # Step 5: Display total coverage amounts
        print("\nTotal Coverage Amounts:")
        for coverage_type, total_amount in total_coverage.items():
            print(f"- {coverage_type} Coverage: {total_amount:.2f}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

#Update Policy
def update_policy():
    print("\n--- Update Policy ---")
    
    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Fetch and display available policies
        cursor.execute("""
        SELECT p.Policy_ID, pt.PolicyType_Name, DATE_FORMAT(p.StartDate, '%Y-%m-%d') AS StartDate,
               DATE_FORMAT(p.EndDate, '%Y-%m-%d') AS EndDate, p.PremiumAmount, p.CoverageAmount
        FROM policy p
        JOIN policytype pt ON p.PolicyType = pt.PolicyType_ID
        """)
        policies = cursor.fetchall()

        if not policies:
            print("No policies found. Please add policies before proceeding.")
            return

        print("\nAvailable Policies:")
        print("+-------------+---------------------+--------------+--------------+------------------+-------------------+")
        print("|   Policy ID | Policy Type         | Start Date   | End Date     |   Premium Amount |   Coverage Amount |")
        print("+=============+=====================+==============+==============+==================+===================+")
        for policy in policies:
            print(f"| {policy[0]:<11} | {policy[1]:<19} | {policy[2]:<12} | {policy[3]:<12} | {policy[4]:<16,.2f} | {policy[5]:<17,.2f} |")
        print("+-------------+---------------------+--------------+--------------+------------------+-------------------+")

        # Step 3: Prompt the user for the Policy ID to update
        policy_id = input("\nEnter the Policy ID to update: ").strip()
        
        # Verify if the entered Policy ID exists
        cursor.execute("SELECT Policy_ID FROM policy WHERE Policy_ID = %s", (policy_id,))
        if cursor.fetchone() is None:
            print(f"Policy ID {policy_id} does not exist. Please try again.")
            return

        # Step 4: Update basic policy details
        policy_type = input("Enter the new Policy Type ID: ").strip()
        start_date = input("Enter the new Start Date (YYYY-MM-DD): ").strip()
        end_date = input("Enter the new End Date (YYYY-MM-DD): ").strip()
        premium_amount = float(input("Enter the new Premium Amount: ").strip())
        coverage_amount = float(input("Enter the new Coverage Amount: ").strip())

        # Update the policy table
        cursor.execute("""
        UPDATE policy
        SET PolicyType = %s, StartDate = %s, EndDate = %s, PremiumAmount = %s, CoverageAmount = %s
        WHERE Policy_ID = %s
        """, (policy_type, start_date, end_date, premium_amount, coverage_amount, policy_id))

        # Step 5: Update detailed coverage (delete existing details and insert new ones)
        cursor.execute("DELETE FROM policy_coverage WHERE Policy_ID = %s", (policy_id,))
        
        while True:
            coverage_type = input("Enter a Coverage Type (or 'done' to finish): ").strip()
            if coverage_type.lower() == 'done':
                break
            coverage_amt = float(input(f"Enter the Coverage Amount for {coverage_type}: ").strip())
            cursor.execute("INSERT INTO policy_coverage (Policy_ID, Coverage_Type, Coverage_Amount) VALUES (%s, %s, %s)", 
                           (policy_id, coverage_type, coverage_amt))

        # Commit the transaction
        conn.commit()
        print(f"Policy ID {policy_id} updated successfully!")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

#Delete Policy
def delete_policy():
    print("\n--- Delete Policy ---")
    
    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Fetch and display available policies with all dependencies
        query = """
        SELECT 
            p.Policy_ID, 
            pt.PolicyType_Name, 
            DATE_FORMAT(p.StartDate, '%Y-%m-%d') AS StartDate,
            DATE_FORMAT(p.EndDate, '%Y-%m-%d') AS EndDate,
            p.PremiumAmount, 
            p.CoverageAmount,
            COUNT(DISTINCT pv.Vehicle_ID) as vehicle_count,
            COUNT(DISTINCT c.Claim_ID) as claim_count,
            COUNT(DISTINCT cp.Policy_ID) as comp_policy_count
        FROM policy p
        JOIN policytype pt ON p.PolicyType = pt.PolicyType_ID
        LEFT JOIN policy_vehicle pv ON p.Policy_ID = pv.Policy_ID
        LEFT JOIN claim c ON p.Policy_ID = c.Policy_ID
        LEFT JOIN comprehensive_policy cp ON p.Policy_ID = cp.Policy_ID
        GROUP BY p.Policy_ID, pt.PolicyType_Name, p.StartDate, p.EndDate, p.PremiumAmount, p.CoverageAmount
        """
        cursor.execute(query)
        policies = cursor.fetchall()

        if not policies:
            print("No policies found. Nothing to delete.")
            return

        # Display available policies with all dependency counts
        print("\nAvailable Policies:")
        print("+-------------+---------------------+--------------+--------------+------------------+-------------------+-----------------+---------------+--------------------+")
        print("|   Policy ID | Policy Type         | Start Date   | End Date     |   Premium Amount |   Coverage Amount | Linked Vehicles | Linked Claims | Comprehensive Link |")
        print("+=============+=====================+==============+==============+==================+===================+=================+===============+====================+")
        for policy in policies:
            premium_amount = f"{policy[4]:,.2f}" if policy[4] is not None else "0.00"
            coverage_amount = f"{policy[5]:,.2f}" if policy[5] is not None else "0.00"
            print(f"| {policy[0]:<11} | {policy[1]:<19} | {policy[2]:<12} | {policy[3]:<12} | "
                  f"{premium_amount:>16} | {coverage_amount:>17} | {policy[6]:>15} | {policy[7]:>13} | {policy[8]:>18} |")
        print("+-------------+---------------------+--------------+--------------+------------------+-------------------+-----------------+---------------+--------------------+")
        
        # Step 3: Get user input for Policy ID to delete
        policy_id = input("Enter the Policy ID to delete: ").strip()
        if not policy_id.isdigit():
            print("Invalid Policy ID. Please enter a valid number.")
            return

        # Step 4: Check for all dependencies
        cursor.execute("SELECT COUNT(*) FROM policy_vehicle WHERE Policy_ID = %s", (policy_id,))
        vehicle_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM claim WHERE Policy_ID = %s", (policy_id,))
        claim_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM comprehensive_policy WHERE Policy_ID = %s", (policy_id,))
        comp_policy_count = cursor.fetchone()[0]

        # Step 5: Handle dependencies
        if vehicle_count > 0 or claim_count > 0 or comp_policy_count > 0:
            print(f"\nPolicy ID {policy_id} has the following dependencies:")
            if vehicle_count > 0:
                print(f"- {vehicle_count} linked vehicle(s)")
            if claim_count > 0:
                print(f"- {claim_count} claim(s)")
            if comp_policy_count > 0:
                print(f"- Comprehensive policy record")
            
            cascade_delete = input("\nWould you like to delete all related records? (y/n): ").strip().lower()
            if cascade_delete != 'y':
                print("Deletion cancelled.")
                return
            
            # Final confirmation for cascade delete
            print("\nWARNING: This will delete:")
            print(f"- The policy record")
            if vehicle_count > 0:
                print(f"- {vehicle_count} vehicle association(s)")
            if claim_count > 0:
                print(f"- {claim_count} claim record(s)")
            if comp_policy_count > 0:
                print(f"- The comprehensive policy record")
            
            final_confirm = input("\nAre you absolutely sure you want to proceed? (y/n): ").strip().lower()
            if final_confirm != 'y':
                print("Deletion cancelled.")
                return

            try:
                # Start transaction
                cursor.execute("START TRANSACTION")
                
                # Delete related records in correct order
                if claim_count > 0:
                    cursor.execute("DELETE FROM claim WHERE Policy_ID = %s", (policy_id,))
                if vehicle_count > 0:
                    cursor.execute("DELETE FROM policy_vehicle WHERE Policy_ID = %s", (policy_id,))
                if comp_policy_count > 0:
                    cursor.execute("DELETE FROM comprehensive_policy WHERE Policy_ID = %s", (policy_id,))
                
                # Delete the policy
                cursor.execute("DELETE FROM policy WHERE Policy_ID = %s", (policy_id,))
                
                # Commit transaction
                conn.commit()
                print(f"\nSuccessfully deleted Policy ID {policy_id} and all related records!")
                
            except mysql.connector.Error as err:
                conn.rollback()
                print(f"Error during deletion: {err}")
                print("All changes have been rolled back.")
                return
                
        else:
            # Simple delete without dependencies
            confirmation = input(f"Are you sure you want to delete Policy ID {policy_id}? (y/n): ").strip().lower()
            if confirmation != 'y':
                print("Deletion cancelled.")
                return

            cursor.execute("DELETE FROM policy WHERE Policy_ID = %s", (policy_id,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"Policy ID {policy_id} deleted successfully!")
            else:
                print(f"Policy ID {policy_id} not found. No changes made.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Vehicle Management menu
def vehicle_management():
    while True:
        print("\n--- Vehicle Management ---")
        print("+-------+-----------------------+")
        print("|   No. | Action                |")
        print("+=======+=======================+")
        print("|     1 | Add New Vehicle       |")
        print("|     2 | View Vehicles         |")
        print("|     3 | Update Vehicle        |")
        print("|     4 | Delete Vehicle        |")
        print("|     0 | Return to Main Menu   |")
        print("+-------+-----------------------+")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_vehicle()
        elif choice == "2":
            view_vehicles()
        elif choice == "3":
            update_vehicle()
        elif choice == "4":
            delete_vehicle()
        elif choice == "0":
            return
        else:
            print("Invalid choice! Please try again.")

# Placeholder functions for Vehicle Management
def add_vehicle():
    print("\n--- Add New Vehicle ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Display available Policyholder IDs
        print("\nAvailable Policyholders:")
        cursor.execute("SELECT Policyholder_ID, Policyholder_Name FROM policyholder")
        policyholders = cursor.fetchall()

        if not policyholders:
            print("No policyholders available!")
            return

        print("+------------------+-----------------------------+")
        print("| Policyholder ID  | Policyholder Name           |")
        print("+------------------+-----------------------------+")
        for ph in policyholders:
            print(f"| {ph[0]:<16} | {ph[1]:<27} |")
        print("+------------------+-----------------------------+")

        # Step 3: Get policyholder details and vehicle information
        policyholder_id = int(input("Enter Policyholder ID: "))
        vehicle_type = input("Enter Vehicle Type (Personal/Commercial): ").strip()
        make_model = input("Enter Make and Model of the Vehicle: ")
        year_of_manufacture = int(input("Enter Year of Manufacture: "))

        # Step 4: Display available Policies with details
        print("\nAvailable Policies:")
        cursor.execute("""
            SELECT p.Policy_ID, pt.PolicyType_Name, DATE_FORMAT(p.StartDate, '%Y-%m-%d') AS StartDate,
                   DATE_FORMAT(p.EndDate, '%Y-%m-%d') AS EndDate, p.PremiumAmount, p.CoverageAmount
            FROM policy p
            JOIN policytype pt ON p.PolicyType = pt.PolicyType_ID
        """)
        policies = cursor.fetchall()

        if not policies:
            print("No policies available!")
            link_policy = 'n'  # Skip linking policy if none available
        else:
            print("+------------+---------------------+--------------+--------------+------------------+-------------------+")
            print("| Policy ID | Policy Type         | Start Date   | End Date     | Premium Amount   | Coverage Amount   |")
            print("+------------+---------------------+--------------+--------------+------------------+-------------------+")
            for policy in policies:
                print(f"| {policy[0]:<10} | {policy[1]:<19} | {policy[2]:<12} | {policy[3]:<12} | {policy[4]:<16,.2f} | {policy[5]:<17,.2f} |")
            print("+------------+---------------------+--------------+--------------+------------------+-------------------+")

            link_policy = input("Do you want to link this vehicle to a policy? (y/n): ").strip().lower()

        # Step 5: Insert the vehicle into the `vehicle` table
        cursor.execute("""
            INSERT INTO vehicle (Policyholder_ID, VehicleType, MakeModel, YearOfManufacture)
            VALUES (%s, %s, %s, %s)
        """, (policyholder_id, vehicle_type, make_model, year_of_manufacture))

        # Commit the insertion to get the last inserted Vehicle ID
        conn.commit()
        vehicle_id = cursor.lastrowid

        # Step 6: Insert additional details based on vehicle type
        if vehicle_type.lower() == 'personal':
            owner_name = input("Enter Owner's Name: ")
            cursor.execute("""
                INSERT INTO personal_vehicle (Vehicle_ID, OwnerName)
                VALUES (%s, %s)
            """, (vehicle_id, owner_name))
        elif vehicle_type.lower() == 'commercial':
            business_name = input("Enter Business Name: ")
            cursor.execute("""
                INSERT INTO commercial_vehicle (Vehicle_ID, BusinessName)
                VALUES (%s, %s)
            """, (vehicle_id, business_name))
        else:
            print("Invalid vehicle type!")
            return

        # Step 7: Link the vehicle to a policy if user chooses 'y'
        if link_policy == 'y':
            policy_id = int(input("Enter Policy ID to link the vehicle: "))
            cursor.execute("""
                INSERT INTO policy_vehicle (Policy_ID, Vehicle_ID)
                VALUES (%s, %s)
            """, (policy_id, vehicle_id))

        # Step 8: Commit all changes
        conn.commit()

        print("\nVehicle added successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

def view_vehicles():
    print("\n--- View All Vehicles ---")

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Step 1: Fetch all vehicles
        cursor.execute("""
            SELECT v.Vehicle_ID, v.Policyholder_ID, v.VehicleType, v.MakeModel, v.YearOfManufacture,
                   CASE 
                       WHEN v.VehicleType = 'personal' THEN pv.OwnerName
                       WHEN v.VehicleType = 'commercial' THEN cv.BusinessName
                       ELSE 'N/A'
                   END AS OwnerBusinessName
            FROM vehicle v
            LEFT JOIN personal_vehicle pv ON v.Vehicle_ID = pv.Vehicle_ID
            LEFT JOIN commercial_vehicle cv ON v.Vehicle_ID = cv.Vehicle_ID
        """)
        vehicles = cursor.fetchall()

        if not vehicles:
            print("No vehicles found!")
            return

        # Step 2: Display the vehicle details
        print("+------------+------------------+-------------------+-------------------------+---------------------+-------------------------+")
        print("| Vehicle ID | Policyholder ID  | Vehicle Type      | Make & Model            | Year of Manufacture | Owner/Business Name     |")
        print("+------------+------------------+-------------------+-------------------------+---------------------+-------------------------+")

        for vehicle in vehicles:
            # Replace None with an empty string or 'N/A'
            vehicle_id = vehicle[0] if vehicle[0] is not None else 'N/A'
            policyholder_id = vehicle[1] if vehicle[1] is not None else 'N/A'
            vehicle_type = vehicle[2] if vehicle[2] is not None else 'N/A'
            make_model = vehicle[3] if vehicle[3] is not None else 'N/A'
            year_of_manufacture = vehicle[4] if vehicle[4] is not None else 'N/A'
            owner_business_name = vehicle[5] if vehicle[5] is not None else 'N/A'

            # Display vehicle details
            print(f"| {vehicle_id:<10} | {policyholder_id:<16} | {vehicle_type:<17} | {make_model:<23} | {year_of_manufacture:<16} | {owner_business_name:<23} |")

        print("+------------+------------------+-------------------+-------------------------+------------------+-------------------------+")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

def update_vehicle():
    print("\n--- Update Vehicle ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Display available vehicle IDs
        cursor.execute("SELECT Vehicle_ID, MakeModel, VehicleType FROM vehicle")  # Including VehicleType here
        vehicles = cursor.fetchall()

        if not vehicles:
            print("No vehicles found!")
            return

        print("\nAvailable vehicles:")
        print("+------------+-------------------------+")
        print("| Vehicle ID | Make & Model            |")
        print("+------------+-------------------------+")
        for vehicle in vehicles:
            print(f"| {vehicle[0]:<10} | {vehicle[1]:<23} |")
        print("+------------+-------------------------+")

        # Step 3: Ask the user to choose a vehicle to update
        vehicle_id = input("\nEnter the Vehicle ID to update: ")

        # Step 4: Validate if the Vehicle ID exists
        cursor.execute("SELECT * FROM vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
        vehicle = cursor.fetchone()

        if not vehicle:
            print("Vehicle not found!")
            return

        print(f"Vehicle data: {vehicle}")  # Debugging print to check the full vehicle data

        # Step 5: Ask the user what details to update
        print("\nSelect the details to update:")
        print("1. Vehicle Type")
        print("2. Make & Model")
        print("3. Year of Manufacture")
        print("4. Owner Name / Business Name")
        print("0. Cancel")

        choice = input("Enter your choice: ")

        if choice == "1":
            vehicle_type = input("Enter new Vehicle Type (personal/commercial): ").strip().lower()
            if vehicle_type not in ['personal', 'commercial']:
                print("Invalid Vehicle Type! Please enter 'personal' or 'commercial'.")
                return
            cursor.execute("UPDATE vehicle SET VehicleType = %s WHERE Vehicle_ID = %s", (vehicle_type, vehicle_id))

            # Update Owner/Business based on Vehicle Type
            if vehicle_type == "personal":
                owner_name = input("Enter new Owner Name: ").strip()
                cursor.execute("UPDATE personal_vehicle SET OwnerName = %s WHERE Vehicle_ID = %s", (owner_name, vehicle_id))
            elif vehicle_type == "commercial":
                business_name = input("Enter new Business Name: ").strip()
                cursor.execute("UPDATE commercial_vehicle SET BusinessName = %s WHERE Vehicle_ID = %s", (business_name, vehicle_id))

        elif choice == "2":
            make_model = input("Enter new Make & Model: ").strip()
            cursor.execute("UPDATE vehicle SET MakeModel = %s WHERE Vehicle_ID = %s", (make_model, vehicle_id))

        elif choice == "3":
            year_of_manufacture = input("Enter new Year of Manufacture: ").strip()
            cursor.execute("UPDATE vehicle SET YearOfManufacture = %s WHERE Vehicle_ID = %s", (year_of_manufacture, vehicle_id))

        elif choice == "4":
            # Check vehicle type and ensure name can be updated
            vehicle_type = vehicle[2].strip().lower()  # Accessing vehicle type correctly
            print(f"Detected Vehicle Type: {vehicle_type}")  # Debugging print to check vehicle type

            if vehicle_type == "personal":  # If vehicle is personal, update owner
                owner_name = input("Enter new Owner Name: ").strip()
                print(f"Updating Owner Name to: {owner_name}")  # Debugging print to check input
                cursor.execute("UPDATE personal_vehicle SET OwnerName = %s WHERE Vehicle_ID = %s", (owner_name, vehicle_id))
            elif vehicle_type == "commercial":  # If vehicle is commercial, update business
                business_name = input("Enter new Business Name: ").strip()
                print(f"Updating Business Name to: {business_name}")  # Debugging print to check input
                cursor.execute("UPDATE commercial_vehicle SET BusinessName = %s WHERE Vehicle_ID = %s", (business_name, vehicle_id))
            else:
                print("Vehicle type is not recognized. Unable to update name.")
                return

        elif choice == "0":
            print("Update canceled.")
            return

        else:
            print("Invalid choice! Please select a valid option.")
            return

        # Commit the changes
        conn.commit()
        print("Vehicle updated successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

def delete_vehicle():
    print("\n--- Delete Vehicle ---")
    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Display available vehicle IDs
        cursor.execute("SELECT Vehicle_ID, MakeModel FROM vehicle")
        vehicles = cursor.fetchall()
        if not vehicles:
            print("No vehicles found!")
            return
            
        print("\nAvailable vehicles:")
        print("+------------+-------------------------+")
        print("| Vehicle ID | Make & Model            |")
        print("+------------+-------------------------+")
        for vehicle in vehicles:
            print(f"| {vehicle[0]:<10} | {vehicle[1]:<23} |")
        print("+------------+-------------------------+")

        # Step 3: Ask the user to choose a vehicle to delete
        vehicle_id = input("\nEnter the Vehicle ID to delete: ")

        # Step 4: Validate if the Vehicle ID exists
        cursor.execute("SELECT * FROM vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
        vehicle = cursor.fetchone()
        if not vehicle:
            print("Vehicle not found!")
            return

        # Step 5: Confirm deletion
        confirmation = input(f"Are you sure you want to delete vehicle with ID {vehicle_id}? (yes/no): ").lower()
        if confirmation != 'yes':
            print("Vehicle deletion canceled.")
            return

        # Step 6: Delete in the correct order to handle foreign key constraints
        # First, delete from policy_vehicle (if exists)
        cursor.execute("DELETE FROM policy_vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
        
        # Then delete from personal_vehicle (if exists)
        cursor.execute("DELETE FROM personal_vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
        
        # Then delete from commercial_vehicle (if exists)
        cursor.execute("DELETE FROM commercial_vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
        
        # Finally delete from the vehicle table
        cursor.execute("DELETE FROM vehicle WHERE Vehicle_ID = %s", (vehicle_id,))

        # Commit the changes
        conn.commit()
        print(f"Vehicle with ID {vehicle_id} deleted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # Rollback changes if any error occurs
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Application Management menu
def application_management():
    while True:
        print("\n--- Application Management ---")
        print("+-------+---------------------------+")
        print("|   No. | Action                    |")
        print("+=======+===========================+")
        print("|     1 | Add New Application       |")
        print("|     2 | View Applications         |")
        print("|     3 | Update Application Status |")
        print("|     0 | Return to Main Menu       |")
        print("+-------+---------------------------+")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_new_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            update_application_status()
        elif choice == "0":
            return
        else:
            print("Invalid choice! Please try again.")

# Add New Application placeholder function
def add_new_application():
    print("\n--- Add New Application ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Fetch available officer IDs from the database
        cursor.execute("SELECT Officer_ID, FullName FROM insurance_officer")  # Correct table name
        officers = cursor.fetchall()

        if not officers:
            print("No officers found. Please add officers before proceeding.")
            return

        # Display available officers
        print("\nAvailable Officers:")
        print("+----------------+--------------------------+")
        print("| Officer ID     | Officer Name             |")
        print("+----------------+--------------------------+")
        for officer in officers:
            print(f"| {officer[0]:<15} | {officer[1]:<24} |")
        print("+----------------+--------------------------+")

        officer_id = input("Enter Officer ID from the list above: ")

        # Step 3: Prompt user for the details of the new application
        review_date = input("Enter Review Date (YYYY-MM-DD): ")
        purpose = input("Enter Purpose: ")
        approval_status = input("Enter Approval Status (Approved, Pending, Rejected): ")
        application_date = input("Enter Application Date (YYYY-MM-DD): ")
        
        # Fetch available policy types from the database
        cursor.execute("SELECT PolicyType_ID, PolicyType_Name FROM policytype")
        policy_types = cursor.fetchall()

        if not policy_types:
            print("No policy types found. Please add policy types before proceeding.")
            return

        print("\nAvailable Policy Types:")
        print("+----------------+--------------------------+")
        print("| Policy Type ID | Policy Type Name         |")
        print("+----------------+--------------------------+")
        for pt in policy_types:
            print(f"| {pt[0]:<15} | {pt[1]:<24} |")
        print("+----------------+--------------------------+")

        policy_type_id = input("Enter Policy Type ID from the list above: ")

        # Step 4: Insert the new application into the application table (no need to specify Application_ID)
        cursor.execute("""
            INSERT INTO application (Officer_ID, ReviewDate, Purpose, ApprovalStatus, ApplicationDate, PolicyType_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (officer_id, review_date, purpose, approval_status, application_date, policy_type_id))

        # Commit the changes
        conn.commit()

        print("New application added successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# View Applications placeholder function
def view_applications():
    print("\n--- View Applications ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Query to fetch all applications from the database
        cursor.execute("""
            SELECT a.Application_ID, a.Officer_ID, a.ReviewDate, a.Purpose, a.ApprovalStatus, 
                   a.ApplicationDate, p.PolicyType_Name 
            FROM application a
            JOIN policytype p ON a.PolicyType_ID = p.PolicyType_ID
        """)

        applications = cursor.fetchall()

        if not applications:
            print("No applications found.")
            return

        # Step 3: Display the fetched data in a table format
        print("\nApplications List:")
        print("+----------------+-----------------+------------+-------------------------+------------------+------------------+-------------------------+")
        print("| Application ID | Officer ID      | Review Date| Purpose                 | Approval Status  | Application Date | Policy Type Name         |")
        print("+----------------+-----------------+------------+-------------------------+------------------+------------------+-------------------------+")

        for app in applications:
            # Format the dates properly and handle NULL values
            review_date = app[2].strftime('%Y-%m-%d') if app[2] else 'N/A'
            application_date = app[5].strftime('%Y-%m-%d') if app[5] else 'N/A'
            approval_status = app[4] if app[4] else 'N/A'

            # Display the application details
            print(f"| {app[0]:<15} | {app[1]:<15} | {review_date:<10} | {app[3]:<23} | {approval_status:<16} | {application_date:<16} | {app[6]:<23} |")
        
        print("+----------------+-----------------+------------+-------------------------+------------------+------------------+-------------------------+")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# Update Application Status placeholder function
def update_application_status():
    print("\n--- Update Application Status ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Fetch available applications to show to the user
        cursor.execute("SELECT Application_ID, ApprovalStatus FROM application")
        applications = cursor.fetchall()

        if not applications:
            print("No applications found.")
            return

        # Step 3: Display available applications with their current status
        print("\nAvailable Applications:")
        print("+----------------+------------------+")
        print("| Application ID | Approval Status  |")
        print("+----------------+------------------+")
        
        for app in applications:
            print(f"| {app[0]:<15} | {app[1]:<16} |")
        
        print("+----------------+------------------+")

        # Step 4: Ask the user to select an Application ID to update
        application_id = input("\nEnter the Application ID to update: ")

        # Step 5: Check if the selected Application ID exists in the database
        cursor.execute("SELECT * FROM application WHERE Application_ID = %s", (application_id,))
        application = cursor.fetchone()

        if not application:
            print("Application ID not found.")
            return

        # Step 6: Ask the user for the new approval status
        new_status = input("Enter the new approval status (e.g., 'Approved', 'Pending', 'Rejected'): ")

        # Step 7: Update the ApprovalStatus in the database
        cursor.execute("UPDATE application SET ApprovalStatus = %s WHERE Application_ID = %s", (new_status, application_id))
        conn.commit()

        print(f"Application ID {application_id} status updated to '{new_status}'.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# Claim Management menu
def claim_management():
    while True:
        print("\n--- Claim Management ---")
        print("+-------+-----------------------+")
        print("|   No. | Action                |")
        print("+=======+=======================+")
        print("|     1 | Add New Claim         |")
        print("|     2 | View Claims           |")
        print("|     3 | Update Claim          |")
        print("|     4 | Delete Claim          |")
        print("|     0 | Return to Main Menu   |")
        print("+-------+-----------------------+")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_claim()
        elif choice == "2":
            view_claims()
        elif choice == "3":
            update_claim()
        elif choice == "4":
            delete_claim()
        elif choice == "0":
            return
        else:
            print("Invalid choice! Please try again.")

# Placeholder functions for Claim Management
def add_claim():
    print("\n--- Add New Claim ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Display available Policy IDs
        cursor.execute("SELECT Policy_ID FROM policy")
        policies = cursor.fetchall()

        if not policies:
            print("No policies found in the system.")
            return

        print("\nAvailable Policy IDs:")
        for policy in policies:
            print(f"Policy ID: {policy[0]}")

        # Step 3: Get the Policy ID for which the claim is being made
        policy_id = input("\nEnter the Policy ID for the claim: ")

        # Step 4: Check if the Policy ID exists in the 'policy' table
        cursor.execute("SELECT Policy_ID FROM policy WHERE Policy_ID = %s", (policy_id,))
        policy = cursor.fetchone()

        if not policy:
            print("Policy ID not found.")
            return

        # Step 5: Get the other claim details from the user
        date_of_claim = input("Enter the Date of Claim (YYYY-MM-DD): ")
        claim_amount = float(input("Enter the Claim Amount: "))
        claim_status = input("Enter the Claim Status (e.g., 'Pending', 'Approved', 'Rejected'): ")

        # Step 6: Insert the new claim into the 'claim' table
        cursor.execute("""
            INSERT INTO claim (Policy_ID, DateOfClaim, ClaimAmount, ClaimStatus)
            VALUES (%s, %s, %s, %s)
        """, (policy_id, date_of_claim, claim_amount, claim_status))

        # Step 7: Commit the transaction to the database
        conn.commit()

        print(f"Claim for Policy ID {policy_id} successfully added.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

def view_claims():
    print("\n--- View Claims ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Query the claims table
        cursor.execute("SELECT Claim_ID, Policy_ID, DateOfClaim, ClaimAmount, ClaimStatus FROM claim")
        claims = cursor.fetchall()

        if not claims:
            print("No claims found.")
            return

        # Step 3: Display the claims in a table-like format
        print("\n+------------+-----------+----------------+--------------+--------------+")
        print("| Claim ID   | Policy ID | Date of Claim  | Claim Amount | Claim Status |")
        print("+------------+-----------+----------------+--------------+--------------+")

        for claim in claims:
            # Format DateOfClaim properly
            date_of_claim = claim[2].strftime('%Y-%m-%d') if claim[2] else 'N/A'
            # Format ClaimAmount with 2 decimal places
            claim_amount = f"{claim[3]:.2f}" if claim[3] else 'N/A'
            # Ensure ClaimStatus is not None
            claim_status = claim[4] if claim[4] else 'N/A'

            # Print the row with properly aligned columns
            print(f"| {claim[0]:<10} | {claim[1]:<9} | {date_of_claim:<14} | {claim_amount:<12} | {claim_status:<12} |")

        print("+------------+-----------+----------------+--------------+--------------+")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

def update_claim():
    print("\n--- Update Claim ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Show available claims
        cursor.execute("SELECT Claim_ID, Policy_ID, DateOfClaim, ClaimAmount, ClaimStatus FROM claim")
        claims = cursor.fetchall()

        if not claims:
            print("No claims found.")
            return

        # Display the claims for selection
        print("\nAvailable Claims:")
        print("+------------+-----------+------------+------------+-------------+")
        print("| Claim ID   | Policy ID | Date of Claim | Claim Amount | Claim Status |")
        print("+------------+-----------+------------+------------+-------------+")

        for claim in claims:
            print(f"| {claim[0]:<10} | {claim[1]:<9} | {claim[2]} | {claim[3]:<12} | {claim[4]:<12} |")

        print("+------------+-----------+------------+------------+-------------+")

        # Step 3: Get Claim ID from the user
        claim_id = int(input("\nEnter the Claim ID to update: "))

        # Check if the claim exists
        cursor.execute("SELECT * FROM claim WHERE Claim_ID = %s", (claim_id,))
        claim = cursor.fetchone()

        if not claim:
            print("Claim not found!")
            return

        # Step 4: Ask user which field they want to update
        print("\nWhich field would you like to update?")
        print("1. Claim Amount")
        print("2. Claim Status")
        choice = int(input("Enter your choice (1 or 2): "))

        if choice == 1:
            new_amount = float(input("Enter the new claim amount: "))
            cursor.execute("UPDATE claim SET ClaimAmount = %s WHERE Claim_ID = %s", (new_amount, claim_id))
            print(f"Claim Amount updated to {new_amount:.2f}")
        elif choice == 2:
            new_status = input("Enter the new claim status: ")
            cursor.execute("UPDATE claim SET ClaimStatus = %s WHERE Claim_ID = %s", (new_status, claim_id))
            print(f"Claim Status updated to {new_status}")
        else:
            print("Invalid choice.")

        # Commit the changes
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

def delete_claim():
    print("\n--- Delete Claim ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Show available claims
        cursor.execute("SELECT Claim_ID, Policy_ID, DateOfClaim, ClaimAmount, ClaimStatus FROM claim")
        claims = cursor.fetchall()

        if not claims:
            print("No claims found.")
            return

        # Display the claims for selection
        print("\nAvailable Claims:")
        print("+------------+-----------+------------+------------+-------------+")
        print("| Claim ID   | Policy ID | Date of Claim | Claim Amount | Claim Status |")
        print("+------------+-----------+------------+------------+-------------+")

        for claim in claims:
            print(f"| {claim[0]:<10} | {claim[1]:<9} | {claim[2]} | {claim[3]:<12} | {claim[4]:<12} |")

        print("+------------+-----------+------------+------------+-------------+")

        # Step 3: Get Claim ID from the user
        claim_id = int(input("\nEnter the Claim ID to delete: "))

        # Check if the claim exists
        cursor.execute("SELECT * FROM claim WHERE Claim_ID = %s", (claim_id,))
        claim = cursor.fetchone()

        if not claim:
            print("Claim not found!")
            return

        # Step 4: Confirm deletion
        confirmation = input(f"Are you sure you want to delete Claim ID {claim_id} (y/n)? ").lower()

        if confirmation == 'y':
            cursor.execute("DELETE FROM claim WHERE Claim_ID = %s", (claim_id,))
            conn.commit()
            print(f"Claim ID {claim_id} has been deleted.")
        else:
            print("Deletion canceled.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# Reports and Analytics menu
def reports_and_analytics():
    while True:
        print("\n--- Reports & Analytics ---")
        print("+-------+----------------------------------+")
        print("|   No. | Action                           |")
        print("+=======+==================================+")
        print("|     1 | View Monthly Policy Sales        |")
        print("|     2 | View Top 5 Vehicle Types Insured |")
        print("|     3 | View Premium Trends              |")
        print("|     0 | Return to Main Menu              |")
        print("+-------+----------------------------------+")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_monthly_policy_sales()
        elif choice == "2":
            view_top_5_vehicle_types()
        elif choice == "3":
            view_premium_trends()
        elif choice == "0":
            return
        else:
            print("Invalid choice! Please try again.")

# View Monthly Policy Sales placeholder function
def view_monthly_policy_sales():
    print("\n--- View Monthly Policy Sales ---")
    
    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Query to get the total sales per month
        query = """
            SELECT 
                DATE_FORMAT(StartDate, '%Y-%m') AS Month, 
                SUM(PremiumAmount) AS TotalSales
            FROM policy
            GROUP BY Month
            ORDER BY Month DESC
        """
        cursor.execute(query)
        sales_data = cursor.fetchall()

        # Step 3: Check if we have any sales data
        if not sales_data:
            print("No policy sales data available.")
            return

        # Step 4: Display the results
        print("\nMonthly Policy Sales:")
        print("+------------+--------------+")
        print("| Month      | Total Sales  |")
        print("+------------+--------------+")
        for data in sales_data:
            # Display with proper formatting for TotalSales (comma separation and 2 decimals)
            print(f"| {data[0]:<10} | {data[1]:>12,.2f} |")
        print("+------------+--------------+")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# View Top 5 Vehicle Types Insured placeholder function
def view_top_5_vehicle_types():
    print("\n--- View Top 5 Vehicle Types Insured ---")
    
    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Query to get the top 5 most insured vehicle types
        query = """
            SELECT v.VehicleType, COUNT(*) AS VehicleCount
            FROM vehicle v
            JOIN policy_vehicle pv ON v.Vehicle_ID = pv.Vehicle_ID
            GROUP BY v.VehicleType
            ORDER BY VehicleCount DESC
            LIMIT 5
        """
        cursor.execute(query)
        vehicle_data = cursor.fetchall()

        # Step 3: Check if we have any vehicle data
        if not vehicle_data:
            print("No vehicle data available.")
            return

        # Step 4: Display the results
        print("\nTop 5 Vehicle Types Insured:")
        print("+-----------------------+---------------------------+")
        print("| Vehicle Type          | Number of Insured Vehicles |")
        print("+-----------------------+---------------------------+")
        for data in vehicle_data:
            print(f"| {data[0]:<22} | {data[1]:>25} |")
        print("+-----------------------+---------------------------+")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# View Premium Trends placeholder function
def view_premium_trends():
    print("\n--- View Premium Trends ---")

    try:
        # Step 1: Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Step 2: Query to get premium trends over time (e.g., monthly)
        query = """
            SELECT DATE_FORMAT(StartDate, '%Y-%m') AS Month, 
                   SUM(PremiumAmount) AS TotalPremium
            FROM policy
            GROUP BY Month
            ORDER BY Month DESC
        """
        cursor.execute(query)
        premium_data = cursor.fetchall()

        # Step 3: Check if we have any premium data
        if not premium_data:
            print("No premium data available.")
            return

        # Step 4: Display the results
        print("\nPremium Trends (Monthly):")
        print("+------------+--------------------+")
        print("| Month      | Total Premium ($)  |")
        print("+------------+--------------------+")
        for data in premium_data:
            # Display with proper formatting for TotalPremium (comma separation and 2 decimals)
            print(f"| {data[0]:<10} | {data[1]:>18,.2f} |")
        print("+------------+--------------------+")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# Main execution
if __name__ == "__main__":
    main_menu()
