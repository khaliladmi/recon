# Reconnaissance Platform Architecture

This document outlines the initial design for a local-only reconnaissance platform.

## Section A – Architecture Diagram

```
+-----------+        +---------+        +---------+        +---------+        +------------+
| Frontend  | <----> |  API    | <----> |  Queue  | <----> | Workers | <----> | Plugins/DB |
+-----------+        +---------+        +---------+        +---------+        +------------+
```

* **Frontend** – Optional web UI used to start scans and view results.
* **API** – FastAPI server exposing endpoints for launching scans and retrieving history.
* **Queue** – Redis or simple in-memory queue for distributing work to workers.
* **Workers** – Separate processes for passive or active scans executing tools.
* **Plugins/DB** – Executable modules for each tool and persistent storage via PostgreSQL.

## Section B – Folder Structure

```
recon/
├── api/            # FastAPI application
├── workers/
│   ├── passive/
│   └── active/
├── plugins/        # Tool definitions and manifests
├── history/        # Scan logs and artifacts
├── docs/           # Project documentation
└── tests/
```

## Section C – Core Components

### Scan Launching Logic

1. API receives a scan request with target domain(s), mode (passive/active/full), and selected tools.
2. API enqueues a task in Redis containing this configuration.
3. Worker pulls the task, loads the necessary tool modules, and executes them sequentially.
4. Results are stored in PostgreSQL and artifacts/logs written to the `history/` directory.

### Plugin Loading and Execution

* Each tool has a manifest (`yaml` or `json`) describing its invocation method.
* Workers dynamically load available plugins by scanning the `plugins/` folder.
* On execution, the worker spawns a subprocess with the specified command and gathers output.

### History Persistence

* A `scans` table in PostgreSQL tracks start time, end time, domain, mode, selected tools, and status.
* Detailed logs are stored as files inside `history/<scan_id>/`.
* API provides endpoints to list scans, retrieve results, and delete history entries.

### Tool Selection and Recon Mode

* The frontend presents all available tools under Passive or Active categories.
* User selections, along with the chosen mode, are sent to the API.
* Workers enforce the mode: passive workers only load passive tools; active workers handle network traffic.

## Section D – What to Build First

1. **API & Worker Skeleton** – Implement FastAPI endpoints to submit a scan and start a background worker process.
2. **Basic Plugin Interface** – Create a simple plugin structure to define at least two tools (e.g., `theHarvester` for passive and `subfinder` for active).
3. **History Storage** – Set up PostgreSQL models for scans and write basic log files.
4. With these pieces, you can trigger a scan and view minimal results, enabling iterative testing.

## Section E – Bonus: Tool Mapping to ARWAD

| ARWAD Stage               | Passive Tools                    | Active Tools                        |
|---------------------------|---------------------------------|------------------------------------|
| Roots/Seeds               | crt.sh, Shodan                  | assetfinder                        |
| Subdomain Enumeration     | theHarvester, SecurityTrails    | subfinder, amass                   |
| Live-check & Sort         | n/a                             | httpx                              |
| Subdomain Takeover        | n/a                             | subjack                            |
| Port Scan                 | n/a                             | nmap, masscan                      |
| Content Discovery         | waybackurls                     | ffuf, dirsearch                    |
| Wayback/Spidering         | waybackmachine                 | gau, hakrawler                     |
| GitHub Leaks              | github-search API               | truffleHog                         |
| OSINT (Shodan, FOFA)      | Shodan API, FOFA API            | n/a                                |
| Nuclei                    | n/a                             | nuclei                             |

