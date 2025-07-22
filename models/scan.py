from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, index=True)
    mode = Column(String, index=True)
    tools = Column(Text)  # comma-separated or JSON string
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default="queued")

    findings = relationship("Finding", back_populates="scan")
    tool_runs = relationship("ToolRun", back_populates="scan")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    data = Column(Text)

    scan = relationship("Scan", back_populates="findings")


class ToolRun(Base):
    __tablename__ = "toolruns"

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    tool = Column(String)
    output = Column(Text)

    scan = relationship("Scan", back_populates="tool_runs")

