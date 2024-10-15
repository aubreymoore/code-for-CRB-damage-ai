###############################################################################
# labeltool.py
#
# Launch in a terminal window using "python3 labeltool.py"
#
# This Python script runs labelImg.py for annotating images within a YOLOv8 dataset.
#
# Requirements:
#
# 1. python3 installed
# 2. labelImg installed (simply clone https://github.com/HumanSignal/labelImg.git)
# 3. A YOLO dataset
# 4. A custom SQLite database
#
###############################################################################

import subprocess
import sqlite3
import pandas as pd
import sys
import click

DATASET_PATH = '/home/aubrey/Desktop/Guam07-training-set/datasets/active_learning2'
LABELIMG_PATH = '/home/aubrey/labelImg/labelImg.py'
DB_PATH = '/home/aubrey/Desktop/Guam07-training-set/code/active_learning2.sqlite3'

def run_labelImg(subset: str, filename: str):
    """
    Opens a single image for annotation by labelImg
    """
    imagepath = f'{DATASET_PATH}/{subset}/{filename}'
    # subprocess.call(['python3', LABELIMG_PATH, imagepath], stdout=subprocess.DEVNULL)
    subprocess.run(['python3', LABELIMG_PATH, imagepath], stdout=sys.stdout)
    return

def get_lowest_conf_obj(conn: sqlite3.Connection):
    """
    Returns a pandas series for the detected object within the database which has the lowest confidence level
    """
    sql = '''
    SELECT img.subset, obj.* FROM obj LEFT JOIN img ON img.filename = obj.filename
    WHERE edit_flag=0
    ORDER BY conf ASC
    LIMIT 1;
    '''
    df = pd.read_sql_query(sql, conn)
    return df.iloc[0]

def get_objects_str(conn: sqlite3.Connection, filename: str):
    """
    Returns a string containing data for all setected objects in an image
    """
    sql = f'''
    SELECT * FROM obj
    WHERE filename = "{filename}"
    ORDER BY x - (w / 2);
    '''
    df = pd.read_sql_query(sql, conn)
    return df.to_string(float_format=lambda x: '%.2f' % x)

def raise_edit_flag(conn: sqlite3.Connection, filename: str):
    """
    Sets img.edit_flag to 1, indicating that image annotations have been edited 
    """
    sql = f'UPDATE img SET edit_flag=1 WHERE filename="{filename}";'
    conn.execute(sql)
    conn.commit()
    
def reset_edit_flags(conn: sqlite3.Connection):
    """
    Resets img.edit_flag to 0 for all images in database
    """
    sql = 'UPDATE img SET edit_flag=0;'
    conn.execute(sql)
    conn.commit()
    
def get_editted_img_count(conn: sqlite3.Connection) -> int:
    sql = 'SELECT COUNT(*) FROM img WHERE edit_flag=1;'
    n = conn.execute(sql).fetchone()[0]
    return(n)
    
#####################################################################
# MAIN
#####################################################################

conn = sqlite3.connect(DB_PATH)
c = ''
while c != 'q':
    click.clear()
    editted_img_count = get_editted_img_count(conn)
    print(f'{editted_img_count=}\nPress q to quit; <space> to annotate; r to reset edit_flags to 0')
    c = click.getchar()
    
    if c == ' ':
        click.clear()
        r = get_lowest_conf_obj(conn)
        subset, filename = r.subset, r.filename
        print(f'{get_objects_str(conn, filename)}') 
        run_labelImg(subset, filename) 
        raise_edit_flag(conn, filename)
         
    if c == 'r':
        reset_edit_flags(conn)
conn.close()