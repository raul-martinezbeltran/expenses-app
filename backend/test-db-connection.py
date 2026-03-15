from database import engine, inspect

try:
    with engine.connect() as connection:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print("Connection sucessesful!")
        print("Existing tables: ", tables)
except Exception as e:
    print("Failed to connect to the database: ", str(e))

