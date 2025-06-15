```python
import logging
from typing import Dict, Any

class ProcessControlAgent:
    def __init__(self, agent_id: str, config: Dict, rag_engine: Any):
        """
        Initializes the ProcessControlAgent.

        Args:
            agent_id: Unique identifier for the agent.
            config: Configuration dictionary containing parameters like pressure thresholds.
            rag_engine: An instance of a RAG engine for querying documents.
        """
        self.agent_id = agent_id
        self.config = config
        self.rag_engine = rag_engine
        self.logger = logging.getLogger(f"ProcessControlAgent-{self.agent_id}")
        logging.basicConfig(level=logging.INFO) # Basic config for demo
        self.logger.info(f"ProcessControlAgent {self.agent_id} initialized with config: {self.config}")

    def monitor_injection_rates(self, sensor_data: Dict) -> Dict:
        """
        Monitors injection rates and other sensor data.

        Args:
            sensor_data: A dictionary containing sensor readings (e.g., {'pressure': 150, 'flow_rate': 100}).

        Returns:
            A dictionary containing the status or actions taken.
        """
        self.logger.info(f"Received sensor data: {sensor_data}")

        pressure_threshold = self.config.get('critical_pressure_threshold', 200) # Example threshold

        if 'pressure' in sensor_data and sensor_data['pressure'] > pressure_threshold:
            self.logger.warning(
                f"Pressure {sensor_data['pressure']} exceeds threshold {pressure_threshold}."
            )
            anomaly_event = {
                'type': 'CriticalPressure',
                'details': f"Pressure at {sensor_data['pressure']}",
                'equipment_id': sensor_data.get('equipment_id', 'EQP-001')
            }
            self.detect_process_anomalies(anomaly_event)
            return {"status": "anomaly_detected", "event": anomaly_event}

        return {"status": "nominal", "data": sensor_data}

    def calculate_optimal_dosage(self, pipeline_conditions: Dict) -> float:
        """
        Calculates the optimal DRA dosage based on pipeline conditions.

        Args:
            pipeline_conditions: A dictionary with pipeline data (e.g., {'pipeline_flow_rate': 5000}).

        Returns:
            The calculated optimal DRA dosage.
        """
        # Placeholder formula: Dosage is 0.05% of pipeline flow rate
        pipeline_flow_rate = pipeline_conditions.get('pipeline_flow_rate', 0)
        optimal_dosage = pipeline_flow_rate * 0.0005

        self.logger.info(
            f"Calculating optimal dosage for conditions: {pipeline_conditions}. "
            f"Calculated dosage: {optimal_dosage}"
        )
        return optimal_dosage

    def detect_process_anomalies(self, event: Dict) -> bool:
        """
        Detects and handles process anomalies.

        Args:
            event: A dictionary describing the anomaly event.

        Returns:
            True if a critical action (like shutdown) was triggered, False otherwise.
        """
        self.logger.info(f"Analyzing anomaly event: {event}")

        if event.get('type') == 'CriticalPressure':
            # Google AI Integration: Query RAG engine for emergency procedure
            # procedure = self.rag_engine.query(
            #     f"What is the emergency procedure for a {event['type']} event "
            #     f"related to {event.get('equipment_id')}?"
            # )
            # self.logger.info(f"Retrieved procedure from RAG: {procedure}")

            # Mocked procedure for demonstration
            mock_procedure = "Initiate controlled shutdown as per SOP-789."
            self.logger.info(f"Using mocked procedure: {mock_procedure}")

            # Based on the (mocked) procedure, decide whether to trigger emergency_shutdown_protocol
            if "shutdown" in mock_procedure.lower():
                self.logger.info(f"Critical event {event['type']} requires shutdown.")
                self.emergency_shutdown_protocol(
                    f"Critical anomaly detected: {event['type']} - {event['details']}"
                )
                return True

        self.logger.warning(f"Non-critical anomaly or no specific action defined for: {event}")
        return False

    def emergency_shutdown_protocol(self, reason: str):
        """
        Initiates the emergency shutdown protocol.

        Args:
            reason: The reason for the shutdown.
        """
        self.logger.critical(f"EMERGENCY SHUTDOWN PROTOCOL INITIATED. Reason: {reason}")
        # Placeholder for actual shutdown commands:
        # self.logger.info("Sending stop command to pump PLC...")
        # self.logger.info("Closing emergency valve V-101...")
        # self.logger.info("Notifying operations team...")
        print(f"CRITICAL: Emergency Shutdown due to: {reason}") # For console visibility in demo

    def generate_process_report(self) -> Dict:
        """
        Generates a mock report of process KPIs.

        Returns:
            A dictionary containing the report.
        """
        report = {
            "agent_id": self.agent_id,
            "report_type": "ProcessControlSummary",
            "kpis": {
                "average_pressure_psi": 155.0, # Mock data
                "total_dra_injected_gallons": 1250.75, # Mock data
                "uptime_percentage": 99.98, # Mock data
                "anomalies_detected_last_24h": 1 # Mock data
            }
        }
        self.logger.info(f"Generated process report: {report}")
        return report

# --- Demonstration Block ---
if __name__ == '__main__':
    # Mock RAGEngine class for demonstration
    class MockRAGEngine:
        def query(self, question: str) -> str:
            self.logger = logging.getLogger("MockRAGEngine")
            self.logger.info(f"MockRAGEngine received query: {question}")
            if "CriticalPressure" in question:
                return "SOP-789: Initiate controlled shutdown. Close inlet valve. Notify supervisor."
            return "Standard Operating Procedure applies."

    # Configuration for the agent
    agent_config = {
        "critical_pressure_threshold": 180, # Lower threshold for testing
        "target_flow_rate": 150
    }

    # Instantiate the mock RAG engine
    mock_rag_engine = MockRAGEngine()

    # Instantiate the ProcessControlAgent
    process_agent = ProcessControlAgent(
        agent_id="PCA-001",
        config=agent_config,
        rag_engine=mock_rag_engine
    )

    # Simulate monitoring
    print("\n--- Simulating Normal Operation ---")
    normal_data = {"pressure": 150, "flow_rate": 145, "equipment_id": "PMP-001"}
    process_agent.monitor_injection_rates(normal_data)

    # Simulate calculating optimal dosage
    print("\n--- Simulating Dosage Calculation ---")
    pipeline_data = {"pipeline_flow_rate": 6000}
    dosage = process_agent.calculate_optimal_dosage(pipeline_data)
    print(f"Calculated optimal dosage: {dosage} units")

    # Simulate a high-pressure event to trigger anomaly detection and emergency logic
    print("\n--- Simulating High-Pressure Event ---")
    high_pressure_data = {"pressure": 190, "flow_rate": 130, "equipment_id": "PMP-002"}
    process_agent.monitor_injection_rates(high_pressure_data)

    # Generate and print a process report
    print("\n--- Generating Process Report ---")
    report = process_agent.generate_process_report()
    import json
    print(json.dumps(report, indent=2))

    print("\n--- Simulation Complete ---")
```
