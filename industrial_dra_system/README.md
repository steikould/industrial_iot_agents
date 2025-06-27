# Industrial DRA Skid Monitoring System

**A comprehensive Python-based industrial monitoring system for a Drag Reducing Agent (DRA) injection skid using a multi-agent architecture, AI-powered analysis, and scalable cloud deployment on Google Cloud Platform (GCP).**

## Project Overview
This system is an end-to-end solution for optimizing the performance, reliability, and efficiency of an industrial DRA injection skid. It uses a multi-agent architecture and is built on GCP.

### Key Features
- **Multi-Agent Architecture:** Three specialized AI agents (Process Control, Predictive Maintenance, Operational Intelligence) work in concert to manage the system.
- **AI-Powered Analysis:** A Retrieval-Augmented Generation (RAG) engine integrated with Google's Vertex AI provides expert-level insights by querying technical manuals, SOPs, and safety documents.
- **Scalable Cloud Deployment:** Architected for the cloud using GCP services like Cloud Run, Pub/Sub, and BigQuery to ensure high availability and auto-scaling.
- **Industrial IoT Integration:** Natively ingests data from a wide range of industrial sensors using standard protocols like MQTT, Modbus, and OPC UA.
- **Real-time Monitoring & Alerting:** Provides sub-second response times for critical alerts and real-time dashboards for operational visibility.

## System Architecture
This section describes the overall architecture of the Industrial DRA Skid Monitoring System.

#### Core Components
1. **Process Control Agent:** Monitors and controls real-time injection processes, optimizes dosage, and handles safety protocols.
2. **Predictive Maintenance Agent:** Analyzes equipment health data (vibration, temperature) to predict failures and schedule maintenance proactively.
3. **Operational Intelligence Agent:** Analyzes operational data, tracks KPIs, generates reports, and provides business intelligence for decision-making.

#### Technology Stack
- **Backend:** Python 3.9+
- **AI/ML:** Google AI SDK (Vertex AI), Scikit-learn, Pandas
- **Cloud Platform:** Google Cloud Platform (GCP)
    - **Compute:** Cloud Run, Cloud Functions
    - **Messaging:** Pub/Sub
    - **Database:** Cloud SQL (Operational), BigQuery (Analytics)
    - **Storage:** Cloud Storage
    - **Observability:** Cloud Monitoring, Cloud Logging
- **IoT Protocols:** MQTT, Modbus TCP/IP, OPC UA

## Project Structure
```
industrial_dra_system/
├── agents/
│   ├── process_control_agent.py
│   ├── predictive_maintenance_agent.py
│   └── operational_intelligence_agent.py
├── a2a_integration/
│   ├── agent_communication.py
│   └── message_routing.py
├── google_ai/
│   ├── rag_engine.py
│   ├── document_processing.py
│   └── knowledge_base.py
├── iot_integration/
│   ├── sensor_data_ingestion.py
│   ├── data_validation.py
│   └── real_time_processing.py
├── gcp_deployment/
│   ├── cloud_functions/
│   ├── cloud_run/
│   └── terraform_configs/
├── monitoring/
│   ├── alerting.py
│   └── logging.py
├── tests/
└── pyproject.toml
└── README.md
```

## Getting Started
This section will guide you through setting up and running the project.

### Prerequisites
- Python 3.9 or higher
- Poetry for dependency management (https://python-poetry.org/docs/#installation)
- A Google Cloud Platform (GCP) project with billing enabled
- Google Cloud SDK (`gcloud` CLI) installed and authenticated (https://cloud.google.com/sdk/docs/install)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/industrial_dra_system.git
   cd industrial_dra_system
   ```
2. **Set up GCP authentication:**
   ```bash
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```
3. **Install dependencies:**
   ```bash
   poetry install
   ```
4. **Configure Environment Variables:**
   Create a `.env` file in the root of the project. This file will store your environment-specific configurations. Example:
   ```env
   GCP_PROJECT_ID="your-gcp-project-id"
   PUBSUB_TOPIC_NAME="dra-system-events"
   DB_USER="your-db-user"
   DB_PASSWORD="your-db-password"
   # Add other necessary environment variables
   ```

### Running the Agents
To run the agents and other components:
```bash
# Run the Process Control Agent
poetry run python industrial_dra_system/agents/process_control_agent.py

# Run the Predictive Maintenance Agent
poetry run python industrial_dra_system/agents/predictive_maintenance_agent.py
# Run the IoT Data Ingestor
poetry run python industrial_dra_system/iot_integration/sensor_data_ingestion.py
```
