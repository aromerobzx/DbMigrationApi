from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    department = Column(String, nullable=False)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job = Column(String, nullable=False)

class Employee(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    datetime = Column(DateTime(timezone=True), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'),nullable=True)
    job_id = Column(Integer, ForeignKey('jobs.id'),nullable=True)