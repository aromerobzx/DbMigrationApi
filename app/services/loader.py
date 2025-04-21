import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)

def process_csv(filepath, table_name):
    id_col = 'id'
    schemas = {
        'departments':['id', 'department'],
        'jobs':['id','job'],
        'hired_employees':['id','name','datetime','department_id','job_id']
    }
    print('reading csv file...')
    df = pd.read_csv(filepath, header=None) # read csv file
    df.columns = schemas[table_name] # assign names to columns
    print('csv file was read')

    row_count = len(df)
    if row_count == 0:
        raise ValueError('CSV must contain at least 1 row')
    if row_count > 1000:
        raise ValueError('Maximum 1000 rows allowed per request')

    # transform datetime col for employees
    if table_name == 'hired_employees':
        df['datetime'] = pd.to_datetime(df['datetime'], utc=True)

    # find already existing ids
    print(f'find already existing ids...')
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT {id_col} FROM {table_name}"))
        existing_ids = set(row[0] for row in result.fetchall())

    
    # filter duplicates
    duplicate_rows = df[df[id_col].isin(existing_ids)]
    new_rows = df[~df[id_col].isin(existing_ids)]
    print(f'skip existing ids...')
    print(f'duplicated ids found: {len(duplicate_rows)}')
    print(f'new ids found: {len(new_rows)}')

    if len(new_rows) > 0:
        with engine.begin() as conn:
            new_rows.to_sql(table_name, con=conn, if_exists='append', index=False)

    return {
        'inserted_count': len(new_rows),
        'skipped_duplicates': duplicate_rows[id_col].tolist()
    }