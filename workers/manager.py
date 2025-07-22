from queue import Queue
from threading import Thread
from typing import Dict, Type

from utils.plugin_loader import load_plugins

job_queue: Queue = Queue()
plugins: Dict[str, Type] = load_plugins()


def enqueue_scan(scan_id: int, target: str, tools: list):
    job_queue.put({"scan_id": scan_id, "target": target, "tools": tools})


def worker_loop():
    from models.database import SessionLocal
    from models import scan as scan_models

    session = SessionLocal()
    while True:
        job = job_queue.get()
        if job is None:
            break
        scan = session.query(scan_models.Scan).get(job["scan_id"])
        if not scan:
            continue
        scan.status = "running"
        session.commit()
        results = []
        for tool in job["tools"]:
            plugin_cls = plugins.get(tool)
            if not plugin_cls:
                continue
            plugin = plugin_cls()
            output = plugin.run(job["target"])
            tool_run = scan_models.ToolRun(scan_id=scan.id, tool=tool, output=output)
            session.add(tool_run)
            results.append(output)
        scan.status = "finished"
        session.commit()
    session.close()

