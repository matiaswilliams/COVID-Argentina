import sys
import os
sys.path.append("../..")
import model 
import geopandas as gpd
import pandas as pd
import numpy as np
import scipy
from model.sim import location, state, contacts
from IPython.display import display
from timeit import default_timer as timer
import swifter
from tqdm import tqdm_notebook as tqdm
import dask.dataframe as dd
from dask.multiprocessing import get


def calculate_contacts(polygon, points, date):
    _people = points[points.geometry.centroid.within(polygon.geometry.buffer(100))]
    data = {
        'date': np.repeat(date, len(_people)),
        'patient1': np.repeat(polygon['patient'], len(_people)),
        'patient2': list(_people['patient'])
    }
    
    exposure_df = pd.DataFrame(data=data, columns = ["date","patient1","patient2"])
    return exposure_df

def extrapolation(df):
    transformation_table = []
    for i, value in df.sort_values("patient").iterrows():
        original_index = value['patient']
        new_index = 0
        step = value['SEXO_TOTAL']
        transformation_table[original_index] = [np.arange(new_index,new_index+step-1)]
        new_index = new_index + step
    return transformation_table

def create_people_df_from_mnz_data(mnz_data, create_contacts=True, time=True):
#     people_df = dummy_row
#     people_df.patient = [0]

    people_df = pd.DataFrame()
    contacts_df_list = []
    i = 0
    first_pass = True
    for idx, row in tqdm(mnz_data.iterrows()):
        
        if time: t_s = timer()
        n_ppl_in_mnz = row["SEXO_TOTAL"]
        if not n_ppl_in_mnz:
            continue
        
#         print("row.geometry.centroid",row.geometry.centroid)
#         dummy_row.geometry = row.geometry
        person_row = pd.DataFrame({"patient": [0], "position": [row.geometry.centroid]})
        
#         dummy_row["calculated_centroid"] = row.geometry.centroid
#         print(dummy_row.columns)
        ppl_in_mnz = pd.concat([person_row]*n_ppl_in_mnz)
        ids = np.arange(i, i+n_ppl_in_mnz)
        ppl_in_mnz.patient = ids
        i+=n_ppl_in_mnz
        if first_pass:
            people_df = ppl_in_mnz
            first_pass = False
        else:
            people_df = people_df.append(ppl_in_mnz, ignore_index=True)
            
        
        if create_contacts:
            for date in range(90):
                for id_ in ids:
                    data = {
                            'date': np.repeat(date, n_ppl_in_mnz),
                            'patient1': np.repeat(id_, n_ppl_in_mnz),
                            'patient2': ids
                        }
                    patient_contact = pd.DataFrame(data=data, columns = ["date", "patient1", "patient2"])
                    csv_name = "contacts/contacts_patient%d_date%d.csv" % (id_, date)
                    if not os.path.exists(csv_name):
                        patient_contact.to_csv(csv_name)
#                     contacts_df_list.append(pd.DataFrame(data=data, columns = ["date", "patient1", "patient2"]))
                    
    
    contacts_df = pd.concat(contacts_df_list, sort=False)
    contacts_df.reset_index(drop=True, inplace=True)
    
    print("Final shape of people_df:",people_df.shape)
    return people_df, contacts_df




def instantiate_sim(mnz_data, people_df, T=100, reindex = True): 
    print("Instantiating Simulation")
    
    print(len(people_df), people_df[people_df["patient"].duplicated()])
#     print("type(people_df), len(people_df)",type(people_df), len(people_df))
    sim = {"map":mnz_data}
    pop_per_neigh = sim["map"]['SEXO_TOTAL']
    N0 = len(people_df)
    
    if reindex:
        people_df['patient'] = np.arange(len(people_df))
    #N0 = people.SEXO_TOTAL.sum()
    #people = people.reindex(people.index.repeat(people.SEXO_TOTAL))

    lat = people_df.position.apply(lambda point: point.y)
    lng = people_df.position.apply(lambda point: point.x)

#     people_df['calculated_centroid'] = people_df.centroid

    sim["location"] = pd.DataFrame(
        {
        "patient": np.repeat(people_df["patient"].to_numpy(), T),
        "date": np.tile(np.arange(T), N0),
        "latitude": np.repeat(lat, T),
        "longitude": np.repeat(lng, T),
        }
    )

#     people_points = people_df.centroid
    distance_cutoff = 0.012
    sim["patients"] = pd.DataFrame({"patient": np.unique(sim["location"]["patient"])})
    sim["dates"] = pd.DataFrame({"date": np.unique(sim["location"]["date"])})
    
    return sim


def get_mnz2ids(mnz_data):
    i = 0
    mnz2ids = {}
    c=0
    for idx, row in tqdm(mnz_data.iterrows()):
        n_ppl_in_mnz = row["SEXO_TOTAL"]
        mnz2ids[idx] =  np.arange(i, i+n_ppl_in_mnz)
        i += n_ppl_in_mnz
        
#         print()
#         print(n_ppl_in_mnz)
#         print(len(mnz2ids[idx]))
#         c+=1
#         if c> 20: break
    return mnz2ids

def get_id2mnz(mnz2ids):
    id2mnz = {}
    for mnz,ids in tqdm(mnz2ids.items()):
        for i in ids:
            id2mnz[i] = mnz
        
    return id2mnz