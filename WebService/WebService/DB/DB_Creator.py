#################
#### imports ####
#################
import sqlite3
from sqlite3 import Error
 
 
def main():
    database = "c:/data/datenbank.sqlite"
 
	#Table: patient_informations
    sql_create_patient_informations_table = """ CREATE TABLE patient_informations (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT
                                        NOT NULL
                                        UNIQUE,
    patient_id                  INTEGER REFERENCES patients (id) ON DELETE NO ACTION
                                                                 ON UPDATE CASCADE,
    clump_thickness             INT,
    uniformity_cell_size        INT,
    uniformity_cell_shape       INT,
    marginal_adhesion           INT,
    single_epithelial_cell_size INT,
    bare_nuclei                 INT,
    bland_chromatin             INT,
    normal_nucleoli             INT,
    mitoses                     INT,
    result                      INT
); """
 
    #Table: patients
    sql_create_patients_table = """CREATE TABLE patients (
    id         INTEGER      PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
    first_name VARCHAR (50),
    last_name  VARCHAR (50),
    birth_date DATE,
    address    VARCHAR (75),
    city       VARCHAR (50),
    email      VARCHAR (75) UNIQUE
                            NOT NULL,
    phone      VARCHAR (25) 
); );"""
 

#Table: users
    sql_create_users_table = """CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, first_name VARCHAR (50), last_name VARCHAR (50), email VARCHAR (50) UNIQUE NOT NULL, password VARCHAR (100) NOT NULL, token VARCHAR (100));"""
 

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create patient_informations table
        create_table(conn, sql_create_patient_informations_table)
        # create patients table
        create_table(conn, sql_create_patients_table)
	    # create users table
        create_table(conn, sql_create_users_table)
    else:
        print("Error! cannot create the database connection.")