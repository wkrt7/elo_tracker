import os

from dotenv import load_dotenv
from models import Base
from sqlalchemy import create_engine, inspect
from sqlalchemy.dialects.postgresql import BOOLEAN, FLOAT, INTEGER, TIMESTAMP, VARCHAR

load_dotenv()  # loads .env into environment variables

DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_ID = os.environ["DB_ID"]

connection_string = f"postgresql://postgres.vkqxkuvqhzlsocnncoik:{DB_PASSWORD}@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(connection_string)

# Inspect the DB
inspector = inspect(engine)

TYPE_MAP = {
    VARCHAR: "VARCHAR",
    FLOAT: "FLOAT",
    BOOLEAN: "BOOLEAN",
    INTEGER: "INTEGER",
    TIMESTAMP: "TIMESTAMP",
}


def simplify_type(col_type):
    # Converts SQLAlchemy type object to string
    for t, name in TYPE_MAP.items():
        if isinstance(col_type, t):
            return name
    return str(col_type)


print("=== DB vs Model Comparison ===\n")

for table in Base.metadata.sorted_tables:
    model_table_name = table.name
    print(f"Table: {model_table_name}")

    # DB table columns
    if model_table_name not in inspector.get_table_names():
        print(f"  WARNING: Table '{model_table_name}' does not exist in DB!")
        continue

    db_columns = inspector.get_columns(model_table_name)
    db_col_dict = {c["name"]: c for c in db_columns}

    # Compare each model column
    for col in table.columns:
        col_name = col.name
        model_type = simplify_type(col.type)
        model_nullable = col.nullable
        model_default = col.default.arg if col.default is not None else None

        if col_name not in db_col_dict:
            print(f"  MISSING in DB: column '{col_name}'")
            continue

        db_col = db_col_dict[col_name]
        db_type = str(db_col["type"]).upper()
        db_nullable = db_col["nullable"]
        db_default = db_col.get("default")

        # Compare type, nullable, default
        mismatches = []
        if model_type not in db_type:
            mismatches.append(f"type(model='{model_type}', db='{db_type}')")
        if model_nullable != db_nullable:
            mismatches.append(f"nullable(model={model_nullable}, db={db_nullable})")
        if model_default != db_default:
            mismatches.append(f"default(model={model_default}, db={db_default})")

        if mismatches:
            print(f"  Column '{col_name}' mismatch: {', '.join(mismatches)}")
        else:
            print(f"  Column '{col_name}' OK")

    print("\n")
