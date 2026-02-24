# SafeDrive2 — Vehicle Insurance Management System

SafeDrive2 is a TMF2034 Database project, CONSIST command-line based vehicle insurance management system developed using Python and MySQL. The system enables insurance officers to manage policyholders, vehicles, policies, and claims, while also generating analytical reports. It simulates real-world insurance workflows and demonstrates strong integration between application logic and relational databases.

This project highlights backend development, database design, and structured CRUD operations in a production-style environment.

---

## Overview

The system provides a structured interface for managing insurance operations, including policyholder registration, vehicle records, policy creation, claims processing, and reporting. It ensures data consistency through relational database constraints and supports efficient data retrieval using SQL queries.

---

## Core Features

### Policyholder Management

* Add new policyholders
* View existing policyholder records
* Update policyholder information
* Delete policyholder entries

### Vehicle Management

* Register vehicles under policyholders
* View vehicle details
* Maintain relational links between policyholders and vehicles

### Policy Management

* Create and manage insurance policies
* Track coverage details and premium values
* Maintain relationships between vehicles and policies

### Claims Management

* Submit insurance claims
* View and update claim records
* Track claim history and status

### Reporting and Analytics

* View monthly policy sales
* Identify most commonly insured vehicle types
* Analyse insurance trends using SQL queries

---

## Technologies Used

* Python — application logic and CLI interface
* MySQL — relational database management
* mysql-connector-python — database connectivity
* SQL — schema design and data operations

---

## Database Design

The system uses a relational database structure consisting of multiple interconnected entities, including:

* Policyholder
* Vehicle
* Policy
* Claim
* Insurance Officer
* Payment
* Policy Type

The database enforces integrity using:

* Primary keys
* Foreign keys
* Cascading updates and deletes

This ensures consistency and prevents orphaned records.


---

## Author

Muhammad Arif bin Saji
Software Engineering Student
Universiti Malaysia Sarawak (UNIMAS)
