from flaskexample.a_Model import ModelIt
from flask import render_template
from flask import request
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import spacy
import pandas as pd
import random
import numpy as np
import spacy


# Python code to connect to Postgres
# You may need to modify this based on your OS, 
# as detailed in the postgres dev setup materials.
user = 'postgres' #add your Postgres username here      
host = 'localhost'
dbname = 'birth_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user, password='tnaegres')
nlp = spacy.load('en_core_web_lg')

@app.route('/')
@app.route('/index')
def cesareans_input():
    return render_template("index.html")


@app.route('/output')
def cesareans_output():
    #pull 'birth_month' from input field and store it
    patient = request.args.get('search_entry')
    #nlp = spacy.load('en_core_web_lg')
    #new_word='Raphael Alabi'
    global nlp
    doc=nlp(patient)
    for ent in doc.ents:
        a=[ent.text,ent.label_,ent.vector, ent.vector_norm]
    
    # Load cleaned and processed data
    import pandas as pd
    floc = '/Users/Jay/AnacondaProjects/histpod/flaskapp/dbs/'
    fname = 'clean_df.csv'
    clean_df = pd.read_csv(floc+fname)
    clean_df=clean_df.drop(columns=['Unnamed: 0'])
    clean_df.head()
    
    #Check the NER tag for the input and load the relevant DB
    import numpy as np
    import pandas as pd
    floc = '/Users/Jay/AnacondaProjects/histpod/flaskapp/dbs/'
    dist_list=pd.DataFrame()
    if a[1] == 'PERSON':
        fname = 'PERSON.pkl'
        vec_final = pd.read_pickle(floc+fname)
        print('Loaded ' + str(fname))
    elif a[1]=='ORG' or a[1]=='NORP':
        fname = 'ORG_NORP.pkl'
        vec_final = pd.read_pickle(floc+fname)
        print('Loaded ' + str(fname))
    elif a[1]=='GPE' or a[1]=='LOC':
        fname = 'GPE_LOC.pkl'
        vec_final = pd.read_pickle(floc+fname)
        print('Loaded ' + str(fname))
    elif a[1]=='EVENT':
        fname = 'EVENT.pkl'
        vec_final = pd.read_pickle(floc+fname)
        print('Loaded ' + str(fname))
    
    #Process the similarity
    dist_list=pd.DataFrame()
    name_parts = list(map(lambda x: x.strip(), patient.split()))
    for ii in range(len(vec_final)):
        dist=np.dot(ent.vector, vec_final.Vectors[ii]) / (ent.vector_norm * vec_final.Vec_norm[ii])
        if dist < 1 and vec_final['Word'][ii] not in ent.text:
            cont = False
            if a[1]=='PERSON':
                for name in name_parts:
                    if name in vec_final['Word'][ii]:
                        cont = True
            if cont:
                continue

            dist_list=dist_list.append({'ep_index':vec_final['ep_index'][ii],
                                    'Word':vec_final['Word'][ii],
                          'Distance':(dist)}, 
                         ignore_index=True)
    dist_df=dist_list.sort_values(by='Distance', ascending=False).head(3)
    dist_df=dist_df.reset_index(drop=True)
    print('Similarity Processed')
    #Combine distances and podcast episode info, and return into a table
    import random
    results=pd.DataFrame()
    words=[]
    for i in range(len(dist_df)):
        words.append(dist_df['Word'][i])
        if len(dist_df['ep_index'][i]) >= 3:
               for ii in range(3):
                ep_list=random.choices(dist_df['ep_index'][i], k=3)
                ep_i=ep_list[ii]
                results=results.append({'Description':clean_df['description'][ep_i],
                                         'ep_title':clean_df['ep_title'][ep_i],
                                          'Word':dist_df['Word'][i],
                                         'pod_title':clean_df['pod_title'][ep_i]},
                                            ignore_index=True)
        else:
            for ii in range(len(dist_df['ep_index'][i])):
                ep_i=dist_df['ep_index'][i]
                results=results.append({'Description':clean_df['description'][ep_i],
                                         'ep_title':clean_df['ep_title'][ep_i],
                                          'Word':dist_df['Word'][i],
                                         'pod_title':clean_df['pod_title'][ep_i]},
                                            ignore_index=True)
            
    return render_template("output.html",results=results, words=words)