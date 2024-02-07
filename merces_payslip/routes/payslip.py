# routes/payslip.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from schemas import Payslip, PayslipCreate,employee_record,PayslipRequest
from database import SessionLocal
from models import PayslipModel
from typing import List
from reportlab.pdfgen import canvas
import pdfkit
from pdfkit.configuration import Configuration
import io
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import Request
from starlette.staticfiles import StaticFiles
import os
from io import BytesIO
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import base64
import requests
from PyPDF2 import PdfWriter, PdfReader
from datetime import datetime



router = APIRouter()


#Jinja2template path
templates = Jinja2Templates(directory="templates")


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
                            #-------------------create_payslip endpoint------------------
                            
@router.post("/create-payslip/", response_model=Payslip)
def create_payslip_endpoint(payslip: PayslipCreate, db: Session = Depends(get_db)):
    try:
        db_payslip = PayslipModel(**payslip.dict())
        db.add(db_payslip)
        #db.refresh(db_payslip)
        db.commit()
       
        return db_payslip
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
    
    
    
    
                            #--------------get payslip by employee_id and  month---------------
                                
@router.post("/get_employee_data",response_model=Payslip)
def get_employee_data(user_data : employee_record,
                      db: Session = Depends(get_db)):
    payslip = db.query(PayslipModel).filter(
        PayslipModel.employee_id == user_data.employee_id,
        PayslipModel.month == user_data.month,
        PayslipModel.year == user_data.year
    ).first()

    if payslip is None:
        raise HTTPException(status_code=200, detail="Payslip not found for this month")
    
    # Use jsonable_encoder to convert the SQLAlchemy model to JSON
    payslip_json = jsonable_encoder(payslip)

    # Create a custom response model with an additional key
    custom_response = {"data": payslip_json}

    return JSONResponse(content=custom_response)
 


    
                            #-----------get_payslip by employee_id endpoint------------
                            
@router.get("/get-payslip/{employee_id}")
def get_payslip_by_employee_id_endpoint(employee_id: int, db: Session = Depends(get_db)):
    payslips = db.query(PayslipModel).filter(PayslipModel.employee_id == employee_id).all()
    if not payslips:
        raise HTTPException(status_code=404, detail="Payslip not found")
    
    return payslips





                            #---------------Download_payslip endpoint-----------------
                            
@router.post("/download-payslip-pdf", response_model=Payslip)
def download_payslip_pdf(
    payslip_request: PayslipRequest,
    db: Session = Depends(get_db)
):
    employee_id = payslip_request.employee_id
    month = payslip_request.month
    year = payslip_request.year

    # Check if the Payslip exists in the database
    payslips = db.query(PayslipModel).filter(
        PayslipModel.employee_id == employee_id,
        PayslipModel.month == month,
        PayslipModel.year == year
    ).first()

    if not payslips:
        raise HTTPException(status_code=200, detail="Payslip not found")

    # Load and render the HTML template
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    template = templates.get_template("payslip_template.html")
    html_content = template.render(request=None, payslips=payslips, timestamp=timestamp)

    # Provide the correct path to wkhtmltopdf executable
    wkhtmltopdf_path = r'E:\my work\pr_test - Copy\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    # Generate PDF from HTML using pdfkit
    pdf_data = pdfkit.from_string(html_content, False, configuration=config)

    # Add password protection using PyPDF2
    encrypted_pdf_buffer = BytesIO()
    encrypt_pdf(BytesIO(pdf_data), encrypted_pdf_buffer, generate_password(payslips))

    # Set the encrypted PDF buffer to the beginning for reading
    encrypted_pdf_buffer.seek(0)

    # Return the encrypted PDF file as a response
    pdf_filename = f"payslip_employee_{employee_id}_{month}_{year}_{timestamp}.pdf"
    response = StreamingResponse(encrypted_pdf_buffer, media_type='application/pdf')
    response.headers["Content-Disposition"] = f"attachment; filename={pdf_filename}"
    return response

def generate_password(employee_data: PayslipModel) -> str:
    # Extract the first four letters of employee_name in uppercase
    employee_name_prefix = employee_data.employee_name[:4].upper()

    # Extract the last four digits of uan_pf_number
    uan_pf_number_suffix = employee_data.uan_pf_number[-4:]

    # Concatenate the two parts to form the password
    password = f"{employee_name_prefix}{uan_pf_number_suffix}"

    return password

def encrypt_pdf(input_buffer, output_buffer, password):
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(input_buffer)
    
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    pdf_writer.encrypt(password)

    pdf_writer.write(output_buffer)





# @router.post("/download-payslip-pdf", response_model=Payslip)
# def download_payslip_pdf(
#     payslip_request: PayslipRequest,
#     db: Session = Depends(get_db)
# ):
#     employee_id = payslip_request.employee_id
#     month = payslip_request.month
#     year = payslip_request.year

#     # Fetch employee details from the database based on employee_id
#     payslips= db.query(PayslipModel).filter(PayslipModel.employee_id == employee_id).first()

#     if not payslips:
#         # Handle the case where employee_id is not found
#         raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

#     # Generate password dynamically based on employee details
#     password = generate_password(payslips)

#     # Load and render the HTML template
#     template = templates.get_template("payslip_template.html")
#     html_content = template.render(request=None, payslips=payslips)

#     # Provide the correct path to wkhtmltopdf executable
#     wkhtmltopdf_path = r'E:\my work\pr_test - Copy\wkhtmltopdf\bin\wkhtmltopdf.exe'
#     config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

#     # Generate PDF from HTML using pdfkit
#     pdf_data = pdfkit.from_string(html_content, False, configuration=config)

#     # Add password protection using PyPDF2
#     pdf_buffer = BytesIO()
#     pdf_buffer.write(pdf_data)
#     pdf_buffer.seek(0)

#     encrypted_pdf_buffer = BytesIO()
#     encrypt_pdf(pdf_buffer, encrypted_pdf_buffer, password)
#     encrypted_pdf_buffer.seek(0)

#     # Return the encrypted PDF file as a response
#     pdf_filename = f"payslip_employee_{employee_id}_{month}_{year}.pdf"
#     response = StreamingResponse(encrypted_pdf_buffer, media_type='application/pdf')
#     response.headers["Content-Disposition"] = f"attachment; filename={pdf_filename}"
#     return response



