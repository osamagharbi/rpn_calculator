from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.rpn_calculator import evaluate_rpn
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String, index=True)
    result = Column(Float)

class CalculationRequest(BaseModel):
    expression: str

@app.post("/calculate/")
def calculate(calculation: CalculationRequest):
    try:
        result = evaluate_rpn(calculation.expression)
        db = SessionLocal()
        db_calculation = Calculation(expression=calculation.expression, result=result)
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)
        return {"expression": calculation.expression, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/export_csv/")
def export_csv():
    db = SessionLocal()
    calculations = db.query(Calculation).all()
    csv_content = "id,expression,result\n"
    for calc in calculations:
        csv_content += f"{calc.id},{calc.expression},{calc.result}\n"
    db.close()
    return Response(content=csv_content, media_type="text/csv")

@app.get("/expressions/")
def get_expressions():
    db = SessionLocal()
    calculations = db.query(Calculation).all()
    db.close()
    return JSONResponse([{"id": calc.id, "expression": calc.expression, "result": calc.result} for calc in calculations])

app.mount("/", StaticFiles(directory="/app/web_app", html=True), name="web_app")
