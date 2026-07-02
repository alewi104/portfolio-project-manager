# ================================================================================
# main.py
# quieries the user for required input of a tech project's info and transforms the resultant dataframe into json input
# ================================================================================

import sqlite3
import pandas as pd
import os

DB_PATH = "portfolio_data.db"

# TODO: Add error handling to functions that interact with the database
# TODO: After the error handling is complete make those functions return a boolean
# TODO: Add input validation for yes/no and integer inputs. Can try for all str inputs
# TODO: Add appropriate comments for the file and methods
# TODO: conn.close() should be in 'finally' section of error handling try block

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
                   summary TEXT,
                   display_order INTEGER,
                   FOREIGN KEY (proj_id) REFERENCES projects (proj_id)
                   )
            """)
    conn.commit()
    conn.close()

# HELPERS

def db_to_df(table: str): 
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM " + table, conn)
    conn.close()

    if df_sql.empty:
        return print("The " + table + " table is empty")
    else:
        return df_sql

def export_db_to_json():
    pass

def check_item_exists(id: int, table:str) -> bool: # add error handling for database errors
    conn = get_connection()

    if table == "projects":
        item_id = "proj_id"
    elif table == "technologies":
        item_id = "tech_id"
    elif table == "images":
        item_id = "img_id"
    elif table == "documents":
        item_id = "doc_id"
    else:
        print("Table name does not exist")
        return
    df_sql = pd.read_sql("SELECT * FROM " + table + " WHERE " + item_id + "= " + id, conn)
    
    conn.close()

    return not df_sql.empty

def move_image(proj_id: int, img_id:int, new_position:int):
    conn = get_connection()
    cursor = conn.cursor() 
    cursor.execute(
        "SELECT img_id FROM images WHERE proj_id = ? ORDER BY display_order",
        (proj_id,)
    )
    order = [row[0] for row in cursor.fetchall()]

    order.remove(img_id)
    order.insert(new_position, img_id)

    cursor.executemany(
        "UPDATE images SET display_order = ? WHERE img_id = ?",
        [(i, iid) for i, iid in enumerate(order)]
    )

# ADD HELPERS

def add_project(slug: str, title: str, thumbnail_alt: str, description: str, thumbnail: str, github_link: str, demo_video: str, problem: str, solution: str, lessons_learned: str, architecture: str, ready_for_publish: str):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO projects (slug, title, thumbnail_alt, description, thumbnail, github_link, demo_video, problem, solution, lessons_learned, architecture, ready_for_publish) VALUES(?,?,?,?,?,?,?,?,?,?,?,?);" 
    cursor.execute(query, (slug, title, thumbnail_alt, description, thumbnail, github_link, demo_video, problem, solution, lessons_learned, architecture, ready_for_publish))
            
    conn.commit()
    conn.close()

def add_technology(name: str): #adds should probably return a succsessful/failed boolean state
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO technologies (name) VALUES(?);"
    cursor.execute(query, (name,))

    conn.commit()
    conn.close()

def add_projtech_relationship(proj_id: int, tech_id:int):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO projtechs (proj_id, tech_id) VALUES(?, ?);"
    cursor.execute(query, (proj_id, tech_id))

    conn.commit()
    conn.close()


def add_image(proj_id:int, filepath:str, caption:str):
    conn = get_connection()
    cursor = conn.cursor()

    count_query = "SELECT COUNT(*) FROM images WHERE proj_id = ?"
    cursor.execute(count_query, (proj_id,))
    count = cursor.fetchone()[0]

    query = "INSERT INTO images (proj_id, filepath, caption, display_order) VALUES(?,?,?,?);"
    cursor.execute(query, (proj_id, filepath, caption, count))

    conn.commit()
    conn.close()

    return cursor.lastrowid

def add_document(proj_id:int, title: str, filepath:str, summary:str, display_order:int):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO images (proj_id, title, filepath, summary, display_order) VALUES(?,?,?,?,?);"
    cursor.execute(query, (proj_id, title, filepath, summary, display_order))

    conn.commit()
    conn.close()

# EDIT HELPERS

def edit_project():
    pass

def edit_technology():
    pass

def edit_projtech_relationship():
    pass

def edit_image():
    pass

def edit_document():
    pass

# DELETE HELPER

def delete_item_by_id(id: int, table: str):
    conn = get_connection()
    cursor = conn.cursor()

    if table == "projects":
        item_id_type = "proj_id"
    elif table == "technologies":
        item_id_type = "tech_id"
    elif table == "images":
        item_id_type = "img_id"
    elif table == "documents":
        item_id_type = "doc_id"
    else:
        print("Table name does not exist")
        return

    query = "DELETE FROM " + table + " WHERE " + item_id_type + " = ?"

    cursor.execute(query, id)

    conn.commit()
    print(f"Rows deleted: {cursor.rowcount}")
    conn.close()


# prints the chosen db table onto the command line
def view_table(table: str):
    data = db_to_df(table)
    print()
    if data == None:
        return 
    else:
        print(data)
        
    
def view_all_tables():
    view_table("projects")
    view_table("technologies")
    view_table("projtechs")
    view_table("images")
    view_table("documents")

def view_image_display_order_by_project(proj_id: int) -> pd.DataFrame:
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM images WHERE proj_id = " + proj_id + " ORDER BY display_order", conn)
    conn.close()

    if df_sql.empty:
        print("The images table is empty")

    return df_sql


# PROMPTS

# PROJECT PROMPTS

def add_project_prompt():
    while True:
        print()
        print("-" * 50)
        print("PROJECT ENTRY")
        print("-" * 50)

        title = input("     1. Enter title: ").strip()
        slug = input("     2. Enter slug: ").strip()
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


        print()
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
            continue
        else:
            continue
        
        add_images = input("     Would you like to add images to this project? (yes/no): ").strip()
        if add_images == "yes":
            add_image_prompt()
        elif add_images == "no":
            continue
    
        add_documents = input("     Would you like to add documents to this project? (yes/no): ").strip()
        if add_document == "yes":
            add_document_prompt()
        


    

def edit_project_prompt():
    pass

def delete_project_prompt():
    while True:
        view_table("projects")

        choice = input("    Select the project id you'd like to delete: ").strip()

        if choice == "exit":
            break

        project_exists = check_item_exists(choice, "projects")

        if project_exists == False:
            print()
            print("Please select an existing project")
            print()
            continue # may need to change back to break
        else:
            confirm = input("   Are you sure you would like to delete project with id: " + choice + "? (yes/no) ").strip()

            if confirm == "yes":
                delete_item_by_id(choice, "projects")
                continue
            else:
                continue

# TECHNOLOGY PROMPTS

def add_tech_prompt():
    while True:
        tech = input("      What technology would you like to add? Type 'exit' to leave ").strip()
        if tech == "exit":
            break
                
        confirm = input("       Are you sure you would like to add " + tech + "? (yes/no) ").strip()
            
        if confirm == "yes":
                    add_technology(tech)
        elif confirm == "no":
            continue
        else:
            break # need handling to input either yes or no only

def delete_tech_prompt():
    while True: 
        view_table("technologies")

        tech_id = input("      What technology would you like to remove by id? Type 'exit' to leave ").strip()
        if tech_id == "exit":
            break
        
        confirm = input("   Are you sure you would like to delete " + tech_id + "? (yes/no) ").strip()

        if confirm == "yes":
            delete_item_by_id(tech_id, "technologies")
        elif confirm == "no":
            continue
        else:
            break # need handling to input either yes or no only

# IMAGE PROMPTS

def add_image_prompt():
    while True:
        print()
        print("-" * 50)
        print("IMAGE ENTRY")
        print("-" * 50)

        print(db_to_df("projects"))
        proj_id = input("      Which project would you like to add images to? ").strip()
        if proj_id == "exit":
            break
        
        while True:
            filepath = input("      Where is the image located (filepath)? ").strip()
            caption = input("      Provide a descriptive caption for the image: ").strip()      
            confirm = input("       Are you sure you would like to add this image? (yes/no/exit) ").strip()
                
            if confirm == "yes":
                display_order = add_image(proj_id, filepath, caption)
                print(view_image_display_order_by_project(proj_id))
                print("image display order is #" + display_order + "in gallery ")
                print()
            elif confirm == "no":
                continue
            elif confirm =="exit":
                break # need handling to input either yes or no only

        
def export_prompt():
    pass

# MENUS

def edit_project_menu():
    while True:
        view_table("projects")
        proj_id = input("      Which project would you like to edit? ").strip()
        if proj_id == "exit":
            break
        
        project_exists = check_item_exists(proj_id, "projects")
        if project_exists == True:
            continue
        else:
            print("Please pick a project that exists")
            break

        print()
        print("-" * 50)
        print("Edit Project Menu")
        print("-" * 50)
        print("  1. Edit Project Info")
        print("  2. Edit Project Images")
        print("  3. Edit Project Documents")
        print("  4. Back")
        print("-" * 50)

        choice = input("      What would you like to edit? Select an option (1-4): ").strip()

        if choice == "1":
            edit_project_prompt()
        elif choice == "2":
            edit_image_prompt()
        elif choice == "3":
            edit_document_prompt()
        elif choice == "4":
            break
        else:
            print(" invalid option chosen. Pick an option from 1-4")
        


def view_tech_menu():
    while True:
        print()
        print("=" * 50)
        print(" Technologies Menu")
        print("=" * 50)
        print("  1. View Technologies")
        print("  2. Add Technology")
        print("  3. Delete Technology")
        print("  4. Back")
        print("-" * 50)

        choice = input("    Select an option (1-4): ").strip()

        if choice == "1":
            print()
            view_table("technologies")
        elif choice == "2":
            add_tech_prompt()
        elif choice == "3":
            delete_tech_prompt()
        elif choice == "4":
            break
        else:
            print(" invalid option chosen. Pick an option from 1-4")

# MAIN MENU

def main(): 
    while True: 
        print()
        print("=" * 50)
        print(" Portfolio Website Project Manager")
        print("=" * 50)
        print("  1. View Projects")
        print("  2. View All Tables")
        print("  3. Add Project")
        print("  4. Edit Project")
        print("  5. Delete Project")
        print("  6. Export JSON")
        print("  7. Technologies Menu")
        print("  8. Quit")
        print("-" * 50)

        choice = input("    Select an option (1-8): ").strip()

        if choice == "1":
            view_table("projects")
        elif choice == "2":
            view_all_tables()
        elif choice == "3":
            add_project_prompt()
        elif choice == "4":
            edit_project_menu()
        elif choice == "5":
            delete_project_prompt()
        elif choice == "6":
            export_db_to_json()
        elif choice == "7":
            view_tech_menu()
        elif choice == "8":
            break
        else:
            print(" invalid option chosen. Pick an option from 1-8")



if __name__ == "__main__":
    init_db()
    main()