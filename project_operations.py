import pandas as pd
import shutil
from pathlib import Path

from db_initializer import get_connection

IMAGE_DST_PATH = "../Pico-8-Portfolio-Site/src/assets/images"
DOC_DST_PATH = "../Pico-8-Portfolio-Site/src/assets/documents"
DATA_DST_PATH = "../Pico-8-Portfolio-Site/public/data"

# HELPERS

def db_to_df(table: str) -> pd.DataFrame: 
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM " + table, conn)
    conn.close()

    if df_sql.empty:
        print("The " + table + " table is empty")
    
    return df_sql

def export_db_to_json():
    conn = get_connection()
    
    projects = pd.read_sql("SELECT * FROM projects WHERE ready_for_publish = TRUE", conn)
    technologies = pd.read_sql("SELECT * FROM projtechs NATURAL JOIN technologies", conn)
    images = pd.read_sql("SELECT * FROM images", conn)
    documents = pd.read_sql("SELECT * FROM documents", conn)
    conn.close()

    output = []
    for _, project in projects.iterrows():
        proj_id = project["proj_id"]

        project_dict = project.to_dict()

        project_dict["technologies"] = (technologies.loc[technologies.proj_id == proj_id, "name"].tolist())
        project_dict["images"] = (images.loc[images.proj_id == proj_id].drop(columns="proj_id").to_dict("records"))
        project_dict["documents"] = (documents.loc[documents.proj_id == proj_id].drop(columns="proj_id").to_dict("records"))

        output.append(project_dict)

    pd.DataFrame(output).to_json(DATA_DST_PATH + "/output.json", orient="records", indent=4)


    # df_sql.to_json('output.json', orient = 'records', indent = 4)
    print("JSON export successful!")

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

def set_dst_filepath(filepath:str, file_type:str) -> str | None:
    src = Path(filepath)

    if not src.exists():
        print("Source file does not exist")
        return None
    
    if file_type == "image":
        dst_dir = Path(IMAGE_DST_PATH)
    elif file_type == "document":
        dst_dir = Path(DOC_DST_PATH)
    else:
        print("File type does not exist")
        return None
    
    dst_dir.parent.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name

    shutil.copy2(src, dst)

    return str(dst)

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

# DELETE HELPERS

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

    cursor.execute(query, (id,))

    conn.commit()
    print(f"Rows deleted: {cursor.rowcount}")
    conn.close()

def delete_projtech_relationship(proj_id, tech_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM projtechs WHERE proj_id = ? AND tech_id = ?"

    cursor.execute(query, (proj_id, tech_id))
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

def view_projtech_relationships(proj_id: int) -> bool:
    conn = get_connection()
    df_sql = pd.read_sql("SELECT * FROM projtechs p NATURAL JOIN technologies WHERE proj_id = " + proj_id, conn)
    conn.close()

    if df_sql.empty:
        print("This project has no assigned technologies")
        return False
    else:
        print(df_sql)
        return True