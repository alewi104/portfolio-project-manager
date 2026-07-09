# ================================================================================
# main.py
# quieries the user for required input of a tech project's info and transforms the resultant dataframe into json input
# ================================================================================

from db_initializer import init_db
from project_operations import view_table, view_all_tables, check_item_exists
from prompts import add_project_prompt, add_tech_prompt, add_image_prompt, add_document_prompt, add_projtech_relationship_prompt
from prompts import edit_project_prompt, edit_image_prompt, edit_document_prompt
from prompts import delete_project_prompt, delete_tech_prompt, delete_image_prompt, delete_document_prompt, delete_projtech_relationship_prompt
from prompts import export_prompt



# TODO: Add error handling to functions that interact with the database
# TODO: After the error handling is complete make those functions return a boolean
# TODO: Add input validation for yes/no and integer inputs. Can try for all str inputs
# TODO: Add appropriate comments for the file and methods
# TODO: conn.close() should be in 'finally' section of error handling try block
# TODO: Fix exit conditions of all while loops 


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
            edit_projtech_menu(proj_id)
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
            delete_image_prompt(proj_id)
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
        
def edit_projtech_menu(proj_id: int):
    while True:
        print()
        print("-" * 50)
        print("Options")
        print("-" * 50)
        print("  1. Add Technologies to the Project")
        print("  2. Delete Project Technologies")
        print("  3. Back")
        print("-" * 50)

        choice = input("      What would you like to edit for project id:" + proj_id + "? Select an option (1-4): ").strip()

        if choice == "1":
            add_projtech_relationship_prompt(proj_id)
        elif choice == "2":
            delete_projtech_relationship_prompt(proj_id)
        elif choice == "3":
            break
        else:
            print("Please pick an option (1-3)")


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
            export_prompt()
        elif choice == "7":
            view_tech_menu()
        elif choice == "8":
            break
        else:
            print(" invalid option chosen. Pick an option from 1-8")



if __name__ == "__main__":
    init_db()
    main()