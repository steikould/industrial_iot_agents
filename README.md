# DRA Injection Skid Digital Twin

This project implements a digital twin for a DRA (Drag Reducing Agent) injection skid, focusing on optimizing pump energy costs while maintaining fuel quality standards. This initial phase targets a pilot location in Atlanta on a 5000-mile fuel pipeline, with the goal of eventual expansion to the full network.

## Overview

The system is designed to provide:
- Semi-realtime monitoring of DRA injection skid parameters.
- 7-day forward planning and optimization of DRA injection schedules.
- Analytics based on historical (8 years) and real-time operational data.
- Integration with GCP Cloud Analytics Platform, including Vertex AI and potentially Gemini AI models.

## Project Structure

- `src/`: Contains the core Python source code.
  - `models/`: Pydantic models defining the data structures for the system (`digital_twin_models.py`).
  - `core/`: Core logic for data processing (e.g., `time_spine.py`, `energy_calculation.py`).
  - `gcp_integration/`: Modules for interacting with Google Cloud Platform services (e.g., `optimization.py` for Vertex AI based optimization).
  - `utils/`: Utility functions.
- `tests/`: Unit and integration tests.
- `docs/`: Project documentation, including system architecture diagrams (e.g., `system_architecture.svg`).
- `config/`: Configuration files for the application.

## Technical Specifications

Refer to the detailed technical specifications document (provided in the initial request) and the system architecture diagram (`docs/system_architecture.svg`) for a comprehensive understanding of the system components, data flows, and optimization strategies. The Pydantic models in `src/models/digital_twin_models.py` are derived directly from these specifications.

## Setup and Installation

(Details on setting up the environment, installing dependencies like Pydantic, and configuring GCP credentials will be added here.)

```bash
# Example (conceptual)
# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# gcloud auth application-default login
```

## Usage

(Instructions on how to run specific modules, trigger optimization tasks, or interact with potential APIs will be detailed here.)

Example of running a placeholder module:
```bash
# python src/core/time_spine.py
# python src/core/energy_calculation.py
# python src/gcp_integration/optimization.py
```

## Phases

- **Phase 1: Monitoring & Analytics (Current Focus)**
  - ✅ MQTT sensor integration (conceptualized in models)
  - ✅ Time spine generation and data processing (placeholder in `src/core/time_spine.py`)
  - ✅ Historical data analysis and modeling (models defined, implementation pending)
  - ✅ Semi-realtime optimization engine (placeholder in `src/gcp_integration/optimization.py`)
  - ✅ 7-day forward planning capability (placeholder in `src/gcp_integration/optimization.py`)
  - ✅ Operations dashboard and analytics (models defined, UI implementation pending)
- **Phase 2: Bidirectional Control (Future)**
- **Phase 3: Full Pipeline Digital Twin (Future)**

## Technology Stack (Key Components)

- **Language**: Python 3.9+
- **Core Data Models**: Pydantic
- **Cloud Platform**: Google Cloud Platform (GCP)
- **ML Platform**: Vertex AI
- **Data Warehouse**: BigQuery
- **Streaming**: Pub/Sub + Apache Beam (conceptual)
- **Communication (Physical Layer)**: MQTT over SCADA (conceptual)

(A full list of Python libraries is outlined in the technical specifications and will be formalized in `requirements.txt`.)
