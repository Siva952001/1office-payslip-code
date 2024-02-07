# models.py
from sqlalchemy import Column, Integer, Float, DateTime,String,TIMESTAMP,VARCHAR,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.sql.expression import text
from database import engine


Base = declarative_base()

class PayslipModel(Base):
        __tablename__ = "merces_paylip"
        _table_args_ = {'extend_existing': True}
        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        employee_name = Column(String(20), index=True)
        employee_id = Column(String(20))
        department= Column(String(30))
        uan_pf_number = Column(String(20))
        designation = Column(String(100))
        esi_number = Column(String(30))
        total_worked_days = Column(Integer)
        lop_days = Column(Integer)
        basic_amount = Column(DECIMAL)
        hra_amount = Column(DECIMAL)
        conveyance_allowance   = Column(DECIMAL)
        lta_amount      = Column(DECIMAL)
        education_allowance  = Column(DECIMAL) 
        special_allowance  = Column(DECIMAL) 
        vehicle_expense  = Column(DECIMAL)
        incentives  = Column(DECIMAL)
        total_gross   = Column(DECIMAL)
        epf_deduction  = Column(DECIMAL)
        esi_deduction   = Column(DECIMAL)
        salary_advances   = Column(DECIMAL)
        professional_tax  = Column(DECIMAL) 
        tds = Column(DECIMAL)
        lwf   = Column(DECIMAL)
        arrears   = Column(DECIMAL)
        total_deductions  = Column(DECIMAL)
        
        net_salary  = Column(DECIMAL) 
        created_at   = Column(TIMESTAMP(timezone=True) , nullable = False, server_default=text('now()'))
        updated_at   = Column(TIMESTAMP(timezone=True) , nullable = False, server_default=text('now()'))
        updated_by = Column(String(200))
        month = Column(String(20))
        year = Column(String(20))
        
Base.metadata.create_all(bind=engine)

        
    