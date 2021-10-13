from datetime import date
from numpy import int16
import pandas as pd
import os 

#/home/armando/colektia/clientes.csv
    
def main():
  #Read path for data source
  data_source = input("Ingrese ruta/path del data source: ")
  df = read_data('/home/armando/colektia/clientes.csv')
  clean_df = clean_data(df)
  if etl_process(clean_df):
    print("ETL process complete")
  else:
    print("Algo salió mal")
 
  
def read_data(data_source):
  df = pd.read_csv(data_source, sep=';')
  return df
  

def clean_data(df):
  #DATA REMOVING    
  del df['altura'], df['peso']
  #DATA COLUMN RENAME
  df = df.rename(columns={
    'fecha_nacimiento': 'birth_date',
    'fecha_vencimiento': 'due_date',
    'deuda': 'due_balance',
    'direccion': 'address',
    'correo': 'email',
    'estatus_contacto': 'status',
    'prioridad': 'priority',
    'telefono': 'phone'
  })
  #DATA MISSING HANDLING
  df[['email', 'status']] = df[['email', 'status']].fillna(value='None')
  df[['priority', 'phone']] = df[['priority', 'phone']].fillna(value=0)
  #DATA STRUCTURE
  df[['fiscal_id', 'first_name', 'last_name', 'gender', 'address', 'email', 'status', 'phone']] = df[[
    'fiscal_id', 'first_name', 'last_name', 'gender', 'address', 'email', 'status', 'phone'
  ]].astype('string')
  df['birth_date'] = pd.to_datetime(df['birth_date'])
  df['due_date'] = pd.to_datetime(df['due_date'])
  df['priority'] = df['priority'].astype(int16)
  return df


def etl_process(df):
  clients_df = transform_clientes_df(df)
  print(clients_df)
  return 1
  

def load_data(df):
  dir_path = os.path.dirname(os.path.realpath(__file__)) + '/output/'
  location_file = dir_path + 'clientes.xlsx'
  df.to_excel(location_file)

 
def transform_clientes_df(df):
  df['age'] = df['birth_date'].apply(lambda x: get_age(x))
  df['age_group'] = df['age'].apply(lambda x: get_age_group(x))
  clients_df = df[['age', 'age_group']]
  return clients_df


def get_age(born):
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age
  

def get_age_group(age):
    if age <= 20:
      age_group = 1
    elif age > 20 & age <= 30:
      age_group = 2
    elif age > 30 & age <= 40:
      age_group = 3
    elif age > 40 & age <= 50:
      age_group = 4
    elif age > 50 & age <= 60:
      age_group = 5
    else:
      age_group = 6
    return age_group

if __name__ == '__main__':
  main()