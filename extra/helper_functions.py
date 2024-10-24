from db.db_session import engine
from sqlalchemy.orm import sessionmaker

Session=sessionmaker(engine)

def execute_get(query):
    with Session() as session:
        result=session.execute(query).first()
        return result