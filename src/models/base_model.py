from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles

class BaseModel(DeclarativeBase):
    pass

@compiles(expression.func.now(), 'postgresql')
def pg_utc_now(element, compiler, **kw):
    return "TIMEZONE('UTC', CURRENT_TIMESTAMP)"