# ================================================================================
# main.py
# quieries the user for required input of a tech project's info and transforms the resultant dataframe into json input
# ================================================================================

import sqlite3
import pandas as pd
import os

DB_PATH = "portfolio_data.db"



# DATABASE

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS projects (
                   proj_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   slug TEXT UNIQUE,
                   title TEXT,
                   thumbnail_alt TEXT,
                   description TEXT,
                   thumbnail TEXT,
                   github_link TEXT,
                   demo_video TEXT,
                   problem TEXT,
                   solution TEXT,
                   lessons_learned TEXT,
                   architecture TEXT, 
                   ready_for_publish BOOLEAN
                )
            """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS technologies (
                   tech_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT UNIQUE
                )
            """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projtechs (
                   proj_id INTEGER,
                   tech_id INTEGER,
                   FOREIGN KEY (proj_id) REFERENCES projects (proj_id),
                   FOREIGN KEY (tech_id) REFERENCES technologies (tech_id)

                )
            """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
                   img_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   proj_id INTEGER,
                   filepath TEXT,
                   caption TEXT,
                   display_order INTEGER,
                   FOREIGN KEY (proj_id) REFERENCES projects (proj_id)
                )
            """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
                   doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   proj_id INTEGER,
                   title TEXT,
                   filepath TEXT,
                   FOREIGN KEY (proj_id) REFERENCES projects (proj_id)
                   )
            """)
    conn.commit()
    conn.close()

def db_to_df(table: str) -> pd.DataFrame: 
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM " + table, conn)
    conn.close()

    return df_sql

#prints the chosen db table onto the command line
def view_projects():
    data = db_to_df("projects")

    if data.empty:
        print("No projects recorded. Try using the 'Add Project' option")
    else:
        print(data)

def add_project():
    pass

def edit_project():
    pass

def delete_project():
    pass

def export_db_to_json():
    pass

# MAIN MENU

def main(): 
    while True: 
        print()
        print("=" * 50)
        print(" Portfolio Website Project Manager")
        print("=" * 50)
        print("  1. View Projects")
        print("  2. Add Project")
        print("  3. Edit Project")
        print("  4. Delete Project")
        print("  5. Export JSON")
        print("  6. Quit")
        print("-" * 50)

        choice = input("    Select an option (1-6): ").strip()

        if choice == "1":
            view_projects()
        elif choice == "2":
            add_project()
        elif choice == "3":
            edit_project()
        elif choice == "4":
            delete_project()
        elif choice == "5":
            export_db_to_json()
        elif choice == "6":
            break
        else:
            print(" invalid option chosen. Pick an option from 1-6")



if __name__ == "__main__":
    init_db()
    main()