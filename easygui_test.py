import easygui as eg
import subprocess
import sqlite3
import pandas as pd
from icecream import ic
import sys
import random

DATASET_PATH = '/home/aubrey/Desktop/Guam07-training-set/datasets/active_learning2'
LABELIMG_PATH = '/home/aubrey/labelImg/labelImg.py'
DB_PATH = '/home/aubrey/Desktop/Guam07-training-set/code/active_learning2.sqlite3'

######

def run_labelImg(subset: str, filename: str):
    imagepath = f'{DATASET_PATH}/{subset}/{filename}'
    # classpath = f'{DATASET_PATH}/{subset}/classes.txt'
    ic(imagepath)
    # proc = subprocess.Popen(['python3', LABELIMG_PATH, imagepath, classpath])
    subprocess.call(['python3', LABELIMG_PATH, imagepath])
    ic('subprocess finished')
    return

# run_labelImg('val', 'IMG_20221115_111718.jpg')
# run_labelImg('train', 'IMG_20221115_122837.jpg')
# print('FINISHED')

######

def get_lowest_conf_obj(db_path: str):
    """
    Returns a pandas series for the detected object within the database which has the lowest confidence level
    """
    sql = '''
    SELECT img.subset, obj.* FROM obj LEFT JOIN img ON img.filename = obj.filename
    ORDER BY conf ASC
    LIMIT 1;
    '''
    df = pd.read_sql_query(sql, sqlite3.connect(db_path))
    return df.iloc[0]
       
r = get_lowest_conf_obj(DB_PATH)
ic(r.filename, r.cls, round(r.conf, 6))

######

# # MAIN

title = 'Annotator'
while True:
    msg = f'{random.randint(1, 1000000)} Press "continue" to edit annotations for an image containing a detected object with the following metadata.\n\n{r.to_dict()}'
    if eg.ccbox(msg, title):
        ic('continuing')
        r = get_lowest_conf_obj(DB_PATH)
        ic(r.subset, r.filename, r.cls, round(r.conf, 2))
        run_labelImg(r.subset, r.filename)
    else:
        sys.exit(0)
    



# r = get_lowest_conf_obj(DB_PATH)
# ic(r.subset, r.filename, r.cls, round(r.conf, 2))

# run_labelImg(r.subset, r.filename)

print('FINISHED')


    




