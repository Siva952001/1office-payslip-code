# schemas.py
from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class PayslipCreate(BaseModel):
    
    employee_name: Optional[str]
    employee_id :Optional [str]
    department : Optional[str]
    designation: Optional[str]
    uan_pf_number : Optional[str]
    esi_number: Optional[str]
    total_worked_days: Optional[int]
    lop_days: Optional[int]
    basic_amount: Optional[Decimal]
    hra_amount: Optional[Decimal]
    conveyance_allowance  :Optional [Decimal]
    lta_amount     : Optional[Decimal]
    education_allowance  : Optional[Decimal]
    special_allowance  : Optional[Decimal]
    vehicle_expense : Optional[Decimal]
    incentives : Optional[Decimal]
    total_gross  : Optional[Decimal]
    epf_deduction : Optional[Decimal]
    esi_deduction  : Optional[Decimal]
    salary_advances  : Optional[Decimal]
    professional_tax : Optional[Decimal]
    tds: Optional[Decimal]
    lwf  : Optional[Decimal]
    arrears  : Optional[Decimal]
    total_deductions :Optional [Decimal]
    net_salary  :Optional [Decimal]
    created_at  :datetime
    updated_at  : datetime
    updated_by: Optional[str] 
    month : Optional[str]
    year:Optional[str]
   

class Payslip(BaseModel):
   
    employee_name: Optional[str]
    employee_id :Optional [str]
    department : Optional[str]
    uan_pf_number : Optional[str]
    designation : Optional[str]
    esi_number: Optional[str]
    total_worked_days: Optional[int]
    lop_days: Optional[int]
    basic_amount: Optional[Decimal]
    hra_amount: Optional[Decimal]
    conveyance_allowance  :Optional [Decimal]
    lta_amount     : Optional[Decimal]
    education_allowance  : Optional[Decimal]
    special_allowance  : Optional[Decimal]
    vehicle_expense : Optional[Decimal]
    incentives : Optional[Decimal]
    total_gross  : Optional[Decimal]
    epf_deduction : Optional[Decimal]
    esi_deduction  : Optional[Decimal]
    salary_advances  : Optional[Decimal]
    professional_tax : Optional[Decimal]
    tds: Optional[Decimal]
    lwf  : Optional[Decimal]
    arrears  : Optional[Decimal]
    total_deductions :Optional [Decimal]
    net_salary  :Optional [Decimal]
    created_at  :datetime
    updated_at  : datetime
    updated_by: Optional[str]
    month:Optional[str]
    year:Optional[str]
    

class employee_record(BaseModel):
    employee_id : str
    month : str
    year : str
    
class PayslipRequest(BaseModel):
    employee_id: str
    month: str
    year: str
    
# class PdfResponse(BaseModel):
#     content: bytes
     
    
   
class Config:
    from_attributes = True

