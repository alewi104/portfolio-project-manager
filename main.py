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

def check_project_exists(id: int):
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM projects WHERE proj_id = " + id, conn)
    
    conn.close()

    return not df_sql.empty

def add_project(slug: str, title: str, thumbnail_alt: str, description: str, thumbnail: str, github_link: str, demo_video: str, problem: str, solution: str, lessons_learned: str, architecture: str, ready_for_publish: str):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO projects (slug, title, thumbnail_alt, description, thumbnail, github_link, demo_video, problem, solution, lessons_learned, architecture, ready_for_publish) VALUES(?,?,?,?,?,?,?,?,?,?,?,?);" 
    cursor.execute(query, (slug, title, thumbnail_alt, description, thumbnail, github_link, demo_video, problem, solution, lessons_learned, architecture, ready_for_publish))
            
    conn.commit()
    conn.close()

def delete_project(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM projects WHERE proj_id = ?"
    proj_id = id
    cursor.execute(query, proj_id)

    conn.commit()
    print(f"Rows deleted: {cursor.rowcount}")
    conn.close()



#prints the chosen db table onto the command line
def view_projects():
    while True:
        data = db_to_df("projects")

        if data.empty:
            print("No projects recorded. Try using the 'Add Project' option")
        else:
            print()
            print(data)
        
        break

def add_project_menu():
    while True:
        print()
        print("-" * 50)
        print("PROJECT ENTRY")
        print("-" * 50)

        title = input("     1. Enter title: ").strip()
        slug = input("      2. Enter slug: ").strip()
        description = input("     3. Enter a short description: ").strip()
        problem = input("     4. Enter problem description: ").strip()
        solution = input("     5. Enter solutions: ").strip()
        lessons_learned = input("     6. Enter the lessons learned: ").strip()
        architecture = input("     7. Enter architecture: ").strip()
        thumbnail = input("     8. Enter thumbnail url: ").strip()
        thumbnail_alt = input("     9. Enter thumbnail alt description: ").strip()
        github_link = input("     10. Enter github repo url: ").strip()
        demo_video = input("     11. Enter a demo video url: ").strip()
        ready_for_publish = input("     12. Is this project ready to publish? (True/False): ").strip()


        done = input("     done? (y/n): ").strip()

        # if ready_for_publish == "yes":
        #     ready_for_publish = True
        # elif ready_for_publish == "no":
        #     ready_for_publish = False
        # else:
        #     print("a yes or no only")
        #     continue
        
        if done == "y":
            add_project(slug, title, thumbnail_alt, description, thumbnail, github_link, demo_video, problem, solution, lessons_learned, architecture, ready_for_publish)
            break


def edit_project():
    pass

def delete_project_menu():
    while True:
        view_projects()

        choice = input("    Select the project id you'd like to delete: ").strip()

        if choice == "exit":
            break

        project_exists = check_project_exists(choice)

        if project_exists == False:
            print()
            print("Please select an existing project")
            print()
            break
        else:
            confirm = input("   Are you sure you would like to delete project with id: " + choice + "? (yes/no) ").strip()

            if confirm == "yes":
                delete_project(choice)
                break
            else:
                break



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
            add_project_menu()
        elif choice == "3":
            edit_project()
        elif choice == "4":
            delete_project_menu()
        elif choice == "5":
            export_db_to_json()
        elif choice == "6":
            break
        else:
            print(" invalid option chosen. Pick an option from 1-6")



if __name__ == "__main__":
    init_db()
    main()