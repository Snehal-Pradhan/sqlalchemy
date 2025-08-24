from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import declarative_base

# Connect to the persistent database we just created
engine = create_engine('sqlite:///relative_database.db')
Base = declarative_base()

# Method 1: Using Inspector
inspector = inspect(engine)
table_names = inspector.get_table_names()
print("Tables in the database:", table_names)


for table_name in table_names:
    columns = inspector.get_columns(table_name)
    print(f"\nColumns in table '{table_name}':")
    for column in columns:
        print(f"  - {column['name']}: {column['type']}")
