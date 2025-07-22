from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from threading import Thread

from models import scan as scan_models
from models.database import Base, engine, SessionLocal
from schemas import scan as scan_schemas
from workers import manager

Base.metadata.create_all(bind=engine)

app = FastAPI()

worker_thread = Thread(target=manager.worker_loop, daemon=True)
worker_thread.start()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/scans/", response_model=scan_schemas.ScanRead)
def create_scan(scan: scan_schemas.ScanCreate, db: Session = Depends(get_db)):
    db_scan = scan_models.Scan(target=scan.target, mode=scan.mode, tools=",".join(scan.tools))
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    manager.enqueue_scan(db_scan.id, db_scan.target, scan.tools)
    return scan_schemas.ScanRead(
        id=db_scan.id,
        target=db_scan.target,
        mode=db_scan.mode,
        tools=scan.tools,
        start_time=db_scan.start_time,
        end_time=db_scan.end_time,
        status=db_scan.status,
    )


@app.get("/scans/", response_model=list[scan_schemas.ScanRead])
def list_scans(db: Session = Depends(get_db)):
    scans = db.query(scan_models.Scan).all()
    result = []
    for s in scans:
        result.append(
            scan_schemas.ScanRead(
                id=s.id,
                target=s.target,
                mode=s.mode,
                tools=s.tools.split(",") if s.tools else [],
                start_time=s.start_time,
                end_time=s.end_time,
                status=s.status,
            )
        )
    return result


@app.get("/scans/{scan_id}", response_model=scan_schemas.ScanRead)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(scan_models.Scan).get(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan_schemas.ScanRead(
        id=scan.id,
        target=scan.target,
        mode=scan.mode,
        tools=scan.tools.split(",") if scan.tools else [],
        start_time=scan.start_time,
        end_time=scan.end_time,
        status=scan.status,
    )

