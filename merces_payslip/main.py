# main.py
from fastapi import FastAPI
from routes.payslip import router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# Application settings
app = FastAPI(
    title="Self services",
    description="1Office API is an integrated HR and workforce management platform, offering extensive capabilities for managing human resources, employee data, time tracking, leave administration, and other HR-related functions. Harness the power of 1Office to optimize HR workflows, enhance workforce productivity, with AI-powered facial recognition attendance tracking and a smart video conferencing application.",
    version="1.0.0",
)

# Configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["payslip"])


#payslip_endpoint test
@app.get("/")
def test():
    return{"message" : "PaySlipTest"}


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.2.251", port=8010)
