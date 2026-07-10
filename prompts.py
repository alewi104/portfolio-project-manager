from project_operations import add_project, add_technology, add_projtech_relationship, add_image, add_document
from project_operations import edit_project, edit_image, edit_document
from project_operations import delete_item_by_id, delete_projtech_relationship
from project_operations import view_table, view_all_tables, view_item_display_order_by_project, view_item, view_projtech_relationships
from project_operations import export_db_to_json, check_item_exists, move_image_or_document, set_dst_filepath

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
    thumbnail = input("     8. Enter thumbnail filepath: ").strip().strip("")
    thumbnail_alt = input("     9. Enter thumbnail alt description: ").strip()
    github_link = input("     10. Enter github repo url: ").strip()
    demo_video = input("     11. Enter a demo video url: ").strip()
    ready_for_publish = input("     12. Is this project ready to publish? (True/False): ").strip().lower()


    print()
    done = input("     done? (y/n): ").strip()

    if ready_for_publish in ("true", "t"):
        ready_for_publish = True
    elif ready_for_publish in ("false", "f"):
        ready_for_publish = False
    
    if done == "y":
        thumbnail = set_dst_filepath(thumbnail, "image")
        if thumbnail == None:
            return
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
    thumbnail = input("     8. Enter a new thumbnail filepath: ").strip().strip('"')
    thumbnail_alt = input("     9. Enter a new thumbnail alt description: ").strip()
    github_link = input("     10. Enter a new github repo url: ").strip()
    demo_video = input("     11. Enter a new demo video url: ").strip()
    ready_for_publish = input("     12. Is this project ready to publish? (True/False): ").strip().lower()


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
    
    if ready_for_publish in ("true", "t"):
        ready_for_publish = True
    elif ready_for_publish in ("false", "f"):
        ready_for_publish = False
    elif ready_for_publish == "":
        ready_for_publish = None
    

    if done == "y":
        thumbnail = set_dst_filepath(thumbnail, "image")
        if thumbnail == None:
            return
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
        
        
        print("Adding Image to Project id " + proj_id)
        filepath = input("      Where is the image located (filepath)? ").strip().strip('"')
        caption = input("      Provide a descriptive caption for the image: ").strip()      
        confirm = input("       Are you sure you would like to add this image? (yes/no/exit) ").strip()
            
        if confirm == "yes":
            filepath = set_dst_filepath(filepath, "image")
            if filepath == None:
                break
            
            display_order = str(add_image(proj_id, filepath, caption))
            view_item_display_order_by_project(proj_id, "images")
            print("image display order is #" + display_order + " in gallery ")
            print()
        elif confirm == "no":
            continue
        elif confirm =="exit":
            break # need handling to input either yes or no only

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
            filepath = input("      Where is the image located (new filepath)? ").strip().strip('"')
            caption = input("      Provide a new descriptive caption for the image: ").strip()
            display_order = input("      New display order (#): ").strip()
            confirm = input("       Are you sure you would like to save this image edit? (yes/no/exit) ").strip()
                
            
            if confirm == "yes":
                if filepath == "":
                    filepath = None
                else:
                    filepath = set_dst_filepath(filepath, "image")
                    if filepath == None:
                        break
                    
                if caption  == "":
                    caption = None
                
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
        
        print("Adding Document to Project id " + proj_id)
        title = input("      What is the document's title? ").strip()
        filepath = input("      Where is the document located (filepath)? ").strip().strip('"')
        summary = input("      Provide a descriptive summary for the document: ").strip()      
        confirm = input("       Are you sure you would like to add this document? (yes/no/exit) ").strip()
            
        if confirm == "yes":
            filepath = set_dst_filepath(filepath, "document")
            if filepath == None:
                break
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
        
        if check_item_exists(doc_id, "documents") == False:
            print("Please pick a document that exists")
            break
        
        while True:
            print("Editing document with id: " + doc_id)
            print("Press Enter to skip")
            print()
            title = input("      What is the document's new title? ").strip()
            filepath = input("      Where is the document located (new filepath)? ").strip().strip('"')
            summary = input("      Provide a new descriptive summary for the document: ").strip()
            display_order = input("      New display order (#): ").strip()
            confirm = input("       Are you sure you would like to save this document edit? (yes/no/exit) ").strip()
                
            
            if confirm == "yes":
                if title == "":
                    title = None
                if filepath == "":
                    filepath = None
                else:
                    filepath = set_dst_filepath(filepath, "document")
                    if filepath == None:
                        break
                if summary == "":
                    summary = None

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
def add_projtech_relationship_prompt(proj_id=None):
    while True:
        print()
        print("-" * 50)
        print("PROJECT TECHNOLOGY ENTRY")
        print("-" * 50)

        if proj_id is None:
            view_table("projects")
            proj_id = input("      Which project would you like to add technologies to? ").strip()
            if proj_id == "exit":
                break
        
        if check_item_exists(proj_id, "projects") == False:
            print("Please pick a project that exists")
            break
        
        print("Adding Technology to Project id " + proj_id)

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

def delete_projtech_relationship_prompt(proj_id=None):
    while True:
        print()
        print("-" * 50)
        print("PROJECT TECHNOLOGY ENTRY")
        print("-" * 50)

        if proj_id is None:
            view_table("projects")
            proj_id = input("      Which project would you like to delete technologies from? ").strip()
            if proj_id == "exit":
                break
        
        if check_item_exists(proj_id, "projects") == False:
            print("Please pick a project that exists")
            break
        
        if view_projtech_relationships(proj_id) == False:
            print("There are no technologies to choose from. ")
            break
        
        print("Deleting Technology from Project id " + proj_id)
        
        tech_id = input("      Which technology would you like to delete? Provide id: ").strip()
        if tech_id == "exit":
            break
        
        confirm = input("      Are you sure you would like to delete technology id:" + tech_id + "? (yes/no)").strip()
        if confirm == "yes":
            delete_projtech_relationship(proj_id, tech_id)
            continue
        if confirm == "no":
            continue



def export_prompt():
        choice = input("      Would you like to export all projects ready for publishing? (yes/no) ").strip()

        if choice == "yes":
            export_db_to_json()
        elif choice == "no":
            print("Request cancelled")
        else:
            print("Please choose either 'yes' or 'no' ")