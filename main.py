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
# TODO: maybe utilize a project object to store a projects attributes in memory
# TODO: fix in gallery enumeration. Displays item's entire table index instead of per project 

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
                   FOREIGN KEY (proj_id) REFERENCES projects (proj_id) ON DELETE CASCADE,
                   FOREIGN KEY (tech_id) REFERENCES technologies (tech_id) ON DELETE CASCADE

                )
            """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
                   img_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   proj_id INTEGER,
                   filepath TEXT,
                   caption TEXT,
                   display_order INTEGER,
                   FOREIGN KEY (proj_id) REFERENCES projects (proj_id) ON DELETE CASCADE
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
                   FOREIGN KEY (proj_id) REFERENCES projects (proj_id) ON DELETE CASCADE
                   )
            """)
    conn.commit()
    conn.close()

# HELPERS

def db_to_df(table: str) -> pd.DataFrame: 
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM " + table, conn)
    conn.close()

    if df_sql.empty:
        print("The " + table + " table is empty")
    
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
        return False
    df_sql = pd.read_sql("SELECT * FROM " + table + " WHERE " + item_id + "= " + id, conn)
    
    conn.close()

    return not df_sql.empty

def move_image_or_document(proj_id: int, item_id:int, item_type: str, new_position:int):
    conn = get_connection()
    cursor = conn.cursor()

    if item_type == "image":
        item_id_type = "img_id"
        table = "images"
    elif item_type == "document":
        item_id_type = "doc_id"
        table = "documents"
    else:
        print("Item type not found")


    query = "SELECT " + item_id_type + " FROM " + table + " WHERE proj_id = ? ORDER BY display_order"
    cursor.execute(query, (proj_id,))

    order = [row[0] for row in cursor.fetchall()]

    print(item_id, type(item_id))
    print(order)
    print([type(x) for x in order])
    
    if item_id not in order:
        raise ValueError(
            f"{item_type} {item_id} not found in project {proj_id}. "
            f"Items found: {order}"
    )

    order.remove(item_id)
    order.insert(new_position, item_id)

    cursor.executemany(
        "UPDATE images SET display_order = ? WHERE img_id = ?",
        [(i, iid) for i, iid in enumerate(order)]
    )

    conn.commit()
    conn.close()

# ADD HELPERS

def add_project(slug: str, title: str, thumbnail_alt: str, description: str, thumbnail: str, github_link: str, demo_video: str, problem: str, solution: str, lessons_learned: str, architecture: str, ready_for_publish: bool):
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

    return count

def add_document(proj_id:int, title: str, filepath:str, summary:str):
    conn = get_connection()
    cursor = conn.cursor()

    count_query = "SELECT COUNT(*) FROM documents WHERE proj_id = ?"
    cursor.execute(count_query, (proj_id,))
    count = cursor.fetchone()[0]

    query = "INSERT INTO documents (proj_id, title, filepath, summary, display_order) VALUES(?,?,?,?,?);"
    cursor.execute(query, (proj_id, title, filepath, summary, count))

    conn.commit()
    conn.close()

    return count

# EDIT HELPERS

# def edit_project_info_query(attribute: str, proj_id: int) -> str:
#     query = "UPDATE projects SET title = ? WHERE proj_id = ?"

def edit_project(proj_id: int, slug: str, title: str, thumbnail_alt: str, description: str, thumbnail: str, github_link: str, demo_video: str, problem: str, solution: str, lessons_learned: str, architecture: str, ready_for_publish: bool):
    conn = get_connection()
    cursor = conn.cursor()
    
    if title is not None:
        cursor.execute("UPDATE projects SET title = ? WHERE proj_id = ?", (title, proj_id))
    if slug is not None:
        cursor.execute("UPDATE projects SET slug = ? WHERE proj_id = ?", (slug, proj_id))
    if description is not None:
        cursor.execute("UPDATE projects SET description = ? WHERE proj_id = ?", (description, proj_id))
    if problem is not None:
        cursor.execute("UPDATE projects SET problem = ? WHERE proj_id = ?", (problem, proj_id))
    if solution is not None:
        cursor.execute("UPDATE projects SET solution = ? WHERE proj_id = ?", (solution, proj_id))
    if lessons_learned is not None:
        cursor.execute("UPDATE projects SET lessons_learned = ? WHERE proj_id = ?", (lessons_learned, proj_id))
    if architecture is not None:
        cursor.execute("UPDATE projects SET architecture = ? WHERE proj_id = ?", (architecture, proj_id))
    if thumbnail is not None:
        cursor.execute("UPDATE projects SET thumbnail = ? WHERE proj_id = ?", (thumbnail, proj_id))
    if thumbnail_alt is not None:
        cursor.execute("UPDATE projects SET thumbnail_alt = ? WHERE proj_id = ?", (thumbnail_alt, proj_id))
    if github_link is not None:
        cursor.execute("UPDATE projects SET github_link = ? WHERE proj_id = ?", (github_link, proj_id))
    if demo_video is not None:
        cursor.execute("UPDATE projects SET demo_video = ? WHERE proj_id = ?", (demo_video, proj_id))
    if ready_for_publish is not None:
        cursor.execute("UPDATE projects SET ready_for_publish = ? WHERE proj_id = ?", (ready_for_publish, proj_id))
    
    conn.commit()
    conn.close()


def edit_technology(tech_id: int, name: str):
    conn = get_connection()
    cursor = conn.cursor()
    # may have to add foreign key pragma

    if name is not None:
        cursor.execute("UPDATE technologies SET name = ? WHERE tech_id  = ", (name, tech_id))
    
    conn.commit()
    conn.close()
    

# Come back to reporpose this 
def edit_projtech_relationship(proj_id: int, tech_id:int):
    conn = get_connection()
    cursor = conn.cursor()

    if tech_id is not None:
        cursor.execute("UPDATE projtechs SET tech_id = ? WHERE proj_id = ?", (tech_id, proj_id))

    conn.commit()
    conn.close()

def edit_image(img_id:int, filepath:str, caption:str):
    conn = get_connection()
    cursor = conn.cursor()

    if filepath is not None:
        cursor.execute("UPDATE images SET filepath = ? WHERE img_id = ?", (filepath, img_id))
    if caption is not None: 
        cursor.execute("UPDATE images SET caption = ? WHERE img_id = ?", (caption, img_id))

    conn.commit()
    conn.close()

def edit_document(doc_id:int, title: str, filepath:str, summary:str):
    conn = get_connection()
    cursor = conn.cursor()

    if filepath is not None:
        cursor.execute("UPDATE documents SET filepath = ? WHERE doc_id = ?", (filepath, doc_id))
    if title is not None: 
        cursor.execute("UPDATE documents SET title = ? WHERE doc_id = ?", (title, doc_id))
    if summary is not None: 
        cursor.execute("UPDATE documents SET summary = ? WHERE doc_id = ?", (summary, doc_id))

    conn.commit()
    conn.close()

# DELETE HELPER

def delete_item_by_id(id: int, table: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

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
def view_table(table: str) -> bool:
    data = db_to_df(table)
    print()
    if data.empty:
        return False
    else:
        print(data)
        return True
        
    
def view_all_tables():
    view_table("projects")
    view_table("technologies")
    view_table("projtechs")
    view_table("images")
    view_table("documents")

def view_item_display_order_by_project(proj_id: int, table: str) -> bool:
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM " + table + " WHERE proj_id = " + proj_id + " ORDER BY display_order", conn)
    conn.close()

    if df_sql.empty:
        print("The " + table + " table is empty for project id: " + proj_id )
        return False
    else:
        print(df_sql)
        return True

def view_item(proj_id: int, table: str) -> bool:
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM " + table + " WHERE proj_id = " + proj_id , conn)
    conn.close()

    if df_sql.empty:
        print("The item can not be found")
        return False
    else:
        print(df_sql)
        return True


# PROMPTS

# PROJECT PROMPTS

def add_project_prompt():
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
        add_images = input("     Would you like to add images to this project? (yes/no): ").strip()
        if add_images == "yes":
            add_image_prompt()
        #elif add_images == "no":
            

        add_documents = input("     Would you like to add documents to this project? (yes/no): ").strip()
        if add_documents == "yes":
            add_document_prompt()
        #elif add_documents == "no":

        add_technologies = input("     Would you like to add technologies to this project? (yes/no): ").strip()
        if add_technologies == "yes":
            add_projtech_relationship_prompt()
        #elif add_technologies == "no":
        #    return print("Project created")
    elif done == "n":
        return print("PROJECT ABORTED")
    
    return print("PROJECT CREATED")
    

def edit_project_prompt(proj_id: int):
    print()
    print("-" * 50)
    print("PROJECT EDIT ENTRY")
    print("-" * 50)

    if view_item(proj_id, "projects") == False:
        return print("PROJECT EDIT ABORTED")
    print("Leave blank if you wish to keep an option as is")

    title = input("     1. Enter new title: ").strip()
    slug = input("     2. Enter new slug: ").strip()
    description = input("     3. Enter a new short description: ").strip()
    problem = input("     4. Enter new problem description: ").strip()
    solution = input("     5. Enter new solutions: ").strip()
    lessons_learned = input("     6. Enter the new lessons learned: ").strip()
    architecture = input("     7. Enter new architecture: ").strip()
    thumbnail = input("     8. Enter a new thumbnail url: ").strip()
    thumbnail_alt = input("     9. Enter a new thumbnail alt description: ").strip()
    github_link = input("     10. Enter a new github repo url: ").strip()
    demo_video = input("     11. Enter a new demo video url: ").strip()
    ready_for_publish = input("     12. Is this project ready to publish? (True/False): ").strip()


    print()
    done = input("     done? (y/n): ").strip()

    if title == "":
        title = None
    if slug == "":
        slug = None
    if description == "":
        description = None
    if problem == "":
        problem = None
    if solution == "":
        solution = None
    if lessons_learned == "":
        lessons_learned = None
    if architecture == "":
        architecture = None
    if thumbnail == "":
        thumbnail = None
    if thumbnail_alt == "":
        thumbnail_alt = None
    if github_link == "":
        github_link = None
    if demo_video == "":
        demo_video = None
    if ready_for_publish == "":
        ready_for_publish = None
    

    if done == "y":
        edit_project(proj_id, slug, title, thumbnail_alt, description, thumbnail, github_link, demo_video, problem, solution, lessons_learned, architecture, ready_for_publish)
    elif done == "n":
        return print("PROJECT EDIT ABORTED")
    
    return print("PROJECT EDIT SAVED")

        

def delete_project_prompt():
    while True:
        if view_table("projects") == False:
            print("There are no projects to delete. Try creating one first")
            break

        proj_id = input("    Select the project id you'd like to delete: ").strip()

        if proj_id == "exit":
            break

        project_exists = check_item_exists(proj_id, "projects")

        if project_exists == False:
            print()
            print("Please select an existing project")
            print()
            continue # may need to change back to break
        else:
            confirm = input("   Are you sure you would like to delete project with id: " + proj_id + "? (yes/no) ").strip()

            if confirm == "yes":
                delete_item_by_id(proj_id, "projects")
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

def add_image_prompt(proj_id=None):
    while True:
        print()
        print("-" * 50)
        print("IMAGE ENTRY")
        print("-" * 50)

        if proj_id is None:
            view_table("projects")
            proj_id = input("      Which project would you like to add images to? ").strip()
            if proj_id == "exit":
                break
        
        if check_item_exists(proj_id, "projects") == False:
            print("Please pick a project that exists")
            break
        
        while True:
            print("Adding Image to Project id " + proj_id)
            filepath = input("      Where is the image located (filepath)? ").strip()
            caption = input("      Provide a descriptive caption for the image: ").strip()      
            confirm = input("       Are you sure you would like to add this image? (yes/no/exit) ").strip()
                
            if confirm == "yes":
                display_order = str(add_image(proj_id, filepath, caption))
                view_item_display_order_by_project(proj_id, "images")
                print("image display order is #" + display_order + " in gallery ")
                print()
            elif confirm == "no":
                continue
            elif confirm =="exit":
                break # need handling to input either yes or no only
            
            break

def edit_image_prompt(proj_id: int):
    while True:
        if view_item_display_order_by_project(proj_id, "images") == False:
            break
        img_id = input("      Which image would you like to edit? ").strip()
        if img_id == "exit":
            break
        
        if check_item_exists(img_id, "images") == False:
            print("Please pick an image that exists")
            break
        
        while True:
            print("Editing image with id: " + img_id)
            filepath = input("      Where is the image located (new filepath)? ").strip()
            caption = input("      Provide a new descriptive caption for the image: ").strip()
            display_order = input("      New display order (#): ").strip()
            confirm = input("       Are you sure you would like to save this image edit? (yes/no/exit) ").strip()

            if filepath == "":
                filepath = None
            if caption  == "":
                caption = None
                
            
            if confirm == "yes":
                edit_image(img_id, filepath, caption)

                if display_order != "":
                    display_order = int(display_order)
                    move_image_or_document(proj_id, int(img_id), "image", display_order)
                break

            elif confirm == "no":
                continue
            elif confirm =="exit":
                break # need handling to input either yes or no only

def delete_image_prompt(proj_id: int):
    while True:
        if view_item_display_order_by_project(proj_id, "images") == False:
            break
        img_id = input("      Which image would you like to delete? ").strip()
        if img_id == "exit":
            break
        
        if check_item_exists(img_id, "images") == False: # insecure. Any image id from any project can be picked
            print("Please pick an image that exists")
            break
        
        confirm = input("   Are you sure you would like to delete image with id: " + img_id + "? (yes/no) ").strip()

        if confirm == "yes":
            delete_item_by_id(img_id, "images")
            continue
        else:
            continue
        

# DOCUMENT PROMPTS
def add_document_prompt(proj_id=None): # fix final exit break
    while True:
        print()
        print("-" * 50)
        print("DOCUMENT ENTRY")
        print("-" * 50)

        if proj_id is None:
            view_table("projects")
            proj_id = input("      Which project would you like to add images to? ").strip()
            if proj_id == "exit":
                break
        
        if check_item_exists(proj_id, "projects") == False:
            print("Please pick a project that exists")
            break
        
        while True:
            print("Adding Document to Project id " + proj_id)
            title = input("      What is the document's title? ").strip()
            filepath = input("      Where is the document located (filepath)? ").strip()
            summary = input("      Provide a descriptive summary for the document: ").strip()      
            confirm = input("       Are you sure you would like to add this document? (yes/no/exit) ").strip()
                
            if confirm == "yes":
                display_order = str(add_document(proj_id, title, filepath, summary))
                view_item_display_order_by_project(proj_id, "documents")
                print("document display order is #" + display_order + " in gallery ")
                print()
            elif confirm == "no":
                continue
            elif confirm =="exit":
                break # need handling to input either yes or no only

def edit_document_prompt(proj_id: int):
    while True:
        if view_item_display_order_by_project(proj_id, "documents") == False:
            break
        doc_id = input("      Which document would you like to edit? ").strip()
        if doc_id == "exit":
            break
        
        if check_item_exists(doc_id, "images") == False:
            print("Please pick a document that exists")
            break
        
        while True:
            print("Editing document with id: " + doc_id)
            print("Press Enter to skip")
            print()
            title = input("      What is the document's new title? ").strip()
            filepath = input("      Where is the document located (new filepath)? ").strip()
            caption = input("      Provide a new descriptive summary for the document: ").strip()
            display_order = input("      New display order (#): ").strip()
            confirm = input("       Are you sure you would like to save this document edit? (yes/no/exit) ").strip()

            if title == "":
                title = None
            if filepath == "":
                filepath = None
            if summary  == "":
                summary = None
                
            
            if confirm == "yes":
                edit_document(doc_id, title, filepath, summary)

                if display_order != "":
                    display_order = int(display_order)
                    move_image_or_document(proj_id, int(doc_id), "document", display_order)
                break

            elif confirm == "no":
                continue
            elif confirm =="exit":
                break # need handling to input either yes or no only

def delete_document_prompt(proj_id: int):
    while True:
        if view_item_display_order_by_project(proj_id, "documents") == False:
            break
        doc_id = input("      Which document would you like to delete? ").strip()
        if doc_id == "exit":
            break
        
        if check_item_exists(doc_id, "documents") == False: # insecure. Any document id from any project can be picked
            print("Please pick an image that exists")
            break
        
        confirm = input("   Are you sure you would like to delete image with id: " + doc_id + "? (yes/no) ").strip()

        if confirm == "yes":
            delete_item_by_id(doc_id, "documents")
            continue
        else:
            continue

# PROJTECH RELATIONSHIP PROMPTS
def add_projtech_relationship_prompt():
    while True:
        print()
        print("-" * 50)
        print("PROJECT TECHNOLOGY ENTRY")
        print("-" * 50)

        view_table("projects")
        proj_id = input("      Which project would you like to add technologies to? ").strip()
        if proj_id == "exit":
            break
        
        if check_item_exists(proj_id, "projects") == False:
            print("Please pick a project that exists")
            break
        
        while True:
            print("Adding Document to Project id " + proj_id)

            if view_table("technologies") == False:
                print("There are no technologies to choose from. ")
                choice = input("      Would you like to add some? (yes/no)").strip()

                if choice == "yes":
                    add_tech_prompt()
                    continue
                elif choice == "no":
                    break
            
            tech_id = input("      Which technology would you like to add? Provide id: ").strip()
            if tech_id == "exit":
                break
            add_projtech_relationship(proj_id, tech_id)
            continue


def export_prompt():
    pass

# MENUS

def edit_project_menu():
    if view_table("projects") == False:
        print("There are no projects to edit. Try creating one first")
        return

    proj_id = input("      Which project would you like to edit? ").strip()
    if proj_id == "exit":
        return
        
    if check_item_exists(proj_id, "projects") == False:
        print("Please pick a project that exists")
        return

    while True:

        print()
        print("-" * 50)
        print("Edit Project Menu")
        print("-" * 50)
        print("  1. Edit Project Info")
        print("  2. Edit Project Images")
        print("  3. Edit Project Documents")
        print("  4. Edit Project Technologies")
        print("  5. Back")
        print("-" * 50)

        choice = input("      What would you like to edit for project id: " + proj_id + "? Select an option (1-5): ").strip()

        if choice == "1":
            edit_project_prompt(proj_id)
        elif choice == "2":
            edit_image_menu(proj_id)
        elif choice == "3":
            edit_document_menu(proj_id)
        elif choice == "4":
            edit_technologies_prompt(proj_id)
        elif choice == "5":
            break
        else:
            print(" invalid option chosen. Pick an option from 1-5")

def edit_image_menu(proj_id: int):
    while True:
        print()
        print("-" * 50)
        print("Options")
        print("-" * 50)
        print("  1. Edit Project Image")
        print("  2. Add New Images to the Project")
        print("  3. Delete Project Image")
        print("  4. Back")
        print("-" * 50)

        choice = input("      What would you like to edit for project id:" + proj_id + "? Select an option (1-4): ").strip()

        if choice == "1":
            edit_image_prompt(proj_id)
        elif choice == "2":
            add_image_prompt(proj_id)
        elif choice == "3":
            delete_i
        elif choice == "4":
            break
        else:
            print("Please pick an option (1-4)")
    
def edit_document_menu(proj_id: int):
    while True:
        print()
        print("-" * 50)
        print("Options")
        print("-" * 50)
        print("  1. Edit Project Document")
        print("  2. Add New Documents to the Project")
        print("  3. Delete Project Document")
        print("  4. Back")
        print("-" * 50)

        choice = input("      What would you like to edit for project id:" + proj_id + "? Select an option (1-4): ").strip()

        if choice == "1":
            edit_document_prompt(proj_id)
        elif choice == "2":
            add_document_prompt(proj_id)
        elif choice == "3":
            delete_document_prompt(proj_id)
        elif choice == "4":
            break
        else:
            print("Please pick an option (1-4)")
        


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
        print()

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