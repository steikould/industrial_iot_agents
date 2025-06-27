from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime, timedelta

# --- General/Shared Enums and Models ---

class PumpType(str, Enum):
    PRIMARY = "PRIMARY"
    BACKUP = "BACKUP"

class PumpStatus(str, Enum):
    ON = "ON"
    OFF = "OFF"
    MAINTENANCE = "MAINTENANCE" # Added based on context

class SensorType(str, Enum):
    FLOW_RATE = "Flow Rate"
    PUMP_STATUS = "Pump Status"
    PRESSURE = "Pressure"

class ReportingMethod(str, Enum):
    EXCEPTION_BASED_MQTT = "Exception-based via MQTT"

# --- Physical Layer Components ---

class SensorConfig(BaseModel):
    sensor_id: str = Field(..., description="Unique identifier for the sensor, e.g., F1, F2, S1, P1")
    sensor_type: SensorType = Field(..., description="Type of the sensor")
    location: str = Field(..., description="Location of the sensor")
    purpose: str = Field(..., description="Purpose of the sensor")
    reporting_method: ReportingMethod = Field(default=ReportingMethod.EXCEPTION_BASED_MQTT, description="How the sensor reports data")

class Pump(BaseModel):
    pump_id: str = Field(..., description="Identifier for the pump")
    pump_type: PumpType = Field(..., description="Primary or Backup pump")
    horsepower: Optional[float] = Field(None, description="Horsepower of the pump, if variable or known")
    continuous_operation_capability: bool = Field(True, description="Whether the pump is capable of continuous operation")
    current_status: PumpStatus = Field(default=PumpStatus.OFF, description="Current operational status of the pump")
    # Add other relevant pump characteristics from pump curve if needed later

class InjectionUnit(BaseModel):
    unit_id: str = Field(default="IU01", description="Identifier for the injection unit")
    variable_rate_capability: bool = Field(True, description="Can inject DRA at variable rates")
    # Add other relevant characteristics if needed

class HMInterface(BaseModel):
    interface_id: str = Field(default="HMI01", description="Identifier for the HMI")
    local_control_enabled: bool = Field(True, description="Allows local operator control")
    monitoring_capabilities: List[str] = Field(default_factory=lambda: ["pump_status", "flow_rate", "pressure", "dra_rate"], description="What can be monitored via HMI")

class DRAInjectionSkid(BaseModel):
    skid_id: str = Field(..., description="Identifier for the DRA injection skid, e.g., 'ATL_SKID_01'")
    primary_pump: Pump
    backup_pump: Pump
    injection_unit: InjectionUnit
    hmi_interface: HMInterface
    piping_incoming_connections: int = Field(default=2, description="Number of incoming connections (one for each pump)")
    piping_outgoing_connections: int = Field(default=2, description="Number of outgoing connections (one for each pump)")
    sensors: List[SensorConfig] = Field(..., description="Configuration of sensors on the skid")

# --- Data Processing Layer ---

class SensorDataPoint(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the sensor reading")
    sensor_id: str = Field(..., description="Identifier of the sensor reporting the data (e.g., F1, P1)")
    value: Any = Field(..., description="Actual value reported by the sensor (can be float, bool for status, etc.)")
    units: Optional[str] = Field(None, description="Units of the sensor value, if applicable (e.g., 'GPM', 'PSI')")

class MinuteLevelData(BaseModel):
    timestamp: datetime = Field(..., description="Minute-level timestamp (YYYY-MM-DD HH:MM:00)")
    flow_rate_f1: Optional[float] = Field(None, description="Incoming fuel flow rate at F1")
    flow_rate_f2: Optional[float] = Field(None, description="Outgoing fuel flow rate at F2")
    pump_status_s1: Optional[PumpStatus] = Field(None, description="Status of the pump(s)")
    pressure_p1: Optional[float] = Field(None, description="System pressure at P1")
    # Potentially other interpolated/calculated values
    dra_injection_rate_actual: Optional[float] = Field(None, description="Actual DRA injection rate for this minute")
    energy_cost_per_minute: Optional[float] = Field(None, description="Calculated energy cost for this minute")
    pump_power_kw: Optional[float] = Field(None, description="Calculated pump power in kW for this minute")
    pump_efficiency_factor: Optional[float] = Field(None, description="Calculated pump efficiency factor for this minute")


class EnergyCostFactors(BaseModel):
    # Factors used in energy cost calculation: Pump Power (kW) × Efficiency Factor × Operating Time × Energy Rate ($/kWh)
    # Pump Power = f(Flowrate, Pressure, Pump Curve)
    # Efficiency Factor = f(Operating Point, Pump Age, Maintenance History)
    # Energy Rate = Static Rate (Phase 1) → Variable Time-of-Use Pricing (Future)
    flow_rate: float # Current flow rate
    pressure: float # Current pressure
    pump_age_years: float
    maintenance_history_summary: Optional[str] = None # Could be a more structured model
    static_energy_rate_per_kwh: float # $/kWh

class DRAEffectivenessFactors(BaseModel):
    dra_concentration_percentage: float
    drag_reduction_achieved: Optional[float] = None # To be correlated

class LabAnalysisResult(BaseModel):
    sample_id: str
    timestamp: datetime
    dra_concentration_percentage: float
    is_compliant: bool

class ExternalData(BaseModel):
    energy_pricing_schedule: Optional[Dict[str, float]] = Field(None, description="Time-of-use energy rates") # e.g. {"00:00-06:00": 0.05, ...}
    operational_schedules: Optional[Dict[str, Any]] = Field(None, description="Pipeline operational schedules") # e.g., planned maintenance

# --- GCP Cloud Analytics Platform ---

class ModelType(str, Enum):
    ARIMA = "ARIMA"
    PROPHET = "Prophet"
    LSTM = "LSTM"
    LINEAR_PROGRAMMING = "Linear Programming"
    GENETIC_ALGORITHMS = "Genetic Algorithms"
    ISOLATION_FOREST = "Isolation Forest"
    AUTOENCODERS = "Autoencoders"

class TargetVariable(str, Enum):
    ENERGY_COST_PER_MINUTE = "energy_cost_per_minute"
    DRA_INJECTION_RATE = "dra_injection_rate"
    PUMP_EFFICIENCY = "pump_efficiency"

class VertexAITrainingConfig(BaseModel):
    training_data_source: str = Field(default="8_years_historical + real_time_stream", description="Source of training data")
    model_types: List[ModelType]
    target_variables: List[TargetVariable]
    # Add other Vertex AI specific configurations like machine type, regions etc.

class OptimizationConstraints(BaseModel):
    min_dra_concentration_ppm: float # Parts per million, or percentage if preferred
    max_dra_concentration_ppm: float
    max_continuous_pump_runtime_hours: Optional[float] = None
    maintenance_windows: Optional[List[Dict[str, datetime]]] = Field(None, description="List of {'start': datetime, 'end': datetime}")
    # Other pump operational limits

class OptimizedInjectionSchedule(BaseModel):
    planning_horizon_days: int = Field(default=7)
    schedule: List[Dict[str, Any]] = Field(..., description="List of timed actions, e.g., {'timestamp': datetime, 'dra_injection_rate': float, 'active_pump': PumpType}")
    projected_total_energy_cost: Optional[float] = None
    projected_dra_utilization: Optional[float] = None # e.g., total DRA used

# --- User Interface Layer (Conceptual Models for data transfer to UI) ---

class RealTimeStatus(BaseModel):
    current_timestamp: datetime
    flow_rate_f1: Optional[float]
    flow_rate_f2: Optional[float]
    pump_status_s1: Optional[PumpStatus]
    pressure_p1: Optional[float]
    current_dra_injection_rate: Optional[float]
    system_health: str = Field(default="NOMINAL", description="e.g., NOMINAL, WARNING, CRITICAL")

class EnergyCostMonitoringData(BaseModel):
    current_cost_per_minute: Optional[float]
    projected_hourly_cost: Optional[float]
    projected_daily_cost: Optional[float]
    cost_trend_short_term: Optional[str] = Field(None, description="e.g., RISING, FALLING, STABLE") # Could be more complex

class DRAQualityMetrics(BaseModel):
    current_dra_concentration_ppm: Optional[float]
    compliance_status: bool # True if within spec, False otherwise
    time_in_spec_percentage_last_24h: Optional[float]

class PumpPerformanceAnalytics(BaseModel):
    pump_id: str
    current_efficiency: Optional[float]
    efficiency_trend: Optional[str] = Field(None, description="e.g., IMPROVING, DECLINING, STABLE")
    utilization_percentage_last_24h: Optional[float]
    last_maintenance_date: Optional[datetime]
    next_predicted_maintenance_date: Optional[datetime] = None # From Gemini/Predictive models

class SevenDayOptimizationPlan(BaseModel):
    plan_id: str
    generated_at: datetime
    recommended_schedules: List[OptimizedInjectionSchedule] # Could be one or multiple alternative schedules
    expected_total_cost_savings: Optional[float] = None
    what_if_scenarios_available: bool = Field(default=False)

class HistoricalTrendDataPoint(BaseModel):
    timestamp: datetime
    value: float
    metric_name: str

class CovariateCandidate(BaseModel):
    name: str
    description: Optional[str] = None
    current_impact_assessment: Optional[str] = Field(None, description="Summary of its evaluated impact")

# --- Technical Stack (for reference, not strictly a data model to be passed around) ---

class PythonLibraries(BaseModel):
    data_processing: List[str] = Field(default_factory=lambda: ["pandas", "numpy", "apache-beam"])
    machine_learning: List[str] = Field(default_factory=lambda: ["scikit-learn", "tensorflow", "xgboost"])
    optimization: List[str] = Field(default_factory=lambda: ["scipy", "pulp", "cvxpy"])
    time_series: List[str] = Field(default_factory=lambda: ["prophet", "statsmodels", "tensorflow-time-series"])
    visualization: List[str] = Field(default_factory=lambda: ["plotly", "dash", "streamlit"])
    cloud_integration: List[str] = Field(default_factory=lambda: ["google-cloud-bigquery", "google-cloud-pubsub"])

# --- Success Metrics & KPIs (Conceptual, for tracking) ---

class KPISet(BaseModel):
    energy_cost_per_barrel: Optional[float] = None
    dra_utilization_efficiency: Optional[float] = None # e.g., DRA used vs. theoretical minimum for target drag reduction
    pump_uptime_percentage: Optional[float] = None
    quality_compliance_percentage: Optional[float] = None # % of time DRA concentration is within spec

# Example of how a full system snapshot might look (very high level)
class DigitalTwinSnapshot(BaseModel):
    timestamp: datetime
    skid_state: DRAInjectionSkid
    live_data: RealTimeStatus
    current_kpis: KPISet
    active_optimization_plan_id: Optional[str] = None

# Placeholder for the future phases
class PhaseControl(BaseModel):
    phase_name: str = Field(..., description="e.g. Phase 1, Phase 2, Phase 3")
    bidirectional_control_enabled: bool = Field(default=False)
    automated_pump_control: bool = Field(default=False)
    real_time_injection_adjustment: bool = Field(default=False)

if __name__ == '__main__':
    # Example Usage / Validation
    sensor_f1 = SensorConfig(sensor_id="F1", sensor_type=SensorType.FLOW_RATE, location="Pipeline Entry", purpose="Monitor incoming fuel flow")
    sensor_s1 = SensorConfig(sensor_id="S1", sensor_type=SensorType.PUMP_STATUS, location="Pump Control Panel", purpose="ON/OFF status monitoring")

    pump1 = Pump(pump_id="PUMP001", pump_type=PumpType.PRIMARY, horsepower=1000, current_status=PumpStatus.ON)
    pump2 = Pump(pump_id="PUMP002", pump_type=PumpType.BACKUP, horsepower=1000, current_status=PumpStatus.OFF)

    skid = DRAInjectionSkid(
        skid_id="ATL_SKID_01",
        primary_pump=pump1,
        backup_pump=pump2,
        injection_unit=InjectionUnit(),
        hmi_interface=HMInterface(),
        sensors=[sensor_f1, sensor_s1]
    )
    print(skid.model_dump_json(indent=2))

    mqtt_message = SensorDataPoint(timestamp=datetime.now(), sensor_id="F1", value=1500.75, units="GPM")
    print(mqtt_message.model_dump_json(indent=2))

    minute_data = MinuteLevelData(
        timestamp=datetime.now().replace(second=0, microsecond=0),
        flow_rate_f1=1502.0,
        pump_status_s1=PumpStatus.ON,
        pressure_p1=300.5,
        energy_cost_per_minute=0.50,
        pump_power_kw=30,
        pump_efficiency_factor=0.85
    )
    print(minute_data.model_dump_json(indent=2))

    vertex_config = VertexAITrainingConfig(
        model_types=[ModelType.LSTM, ModelType.PROPHET],
        target_variables=[TargetVariable.ENERGY_COST_PER_MINUTE, TargetVariable.PUMP_EFFICIENCY]
    )
    print(vertex_config.model_dump_json(indent=2))

    optimization_constraints = OptimizationConstraints(
        min_dra_concentration_ppm=5.0,
        max_dra_concentration_ppm=15.0,
        max_continuous_pump_runtime_hours=168 # 1 week
    )
    print(optimization_constraints.model_dump_json(indent=2))

    # Example of how the models can be nested or used together
    # This is just a conceptual example.
    # In a real application, these would be populated by different services/modules.

    # Simulate some real-time data
    current_status_snapshot = RealTimeStatus(
        current_timestamp=datetime.now(),
        flow_rate_f1=1490.0,
        flow_rate_f2=1485.0,
        pump_status_s1=PumpStatus.ON,
        pressure_p1=295.0,
        current_dra_injection_rate=10.5, # ppm or other unit
        system_health="NOMINAL"
    )

    # Simulate energy cost data
    energy_data = EnergyCostMonitoringData(
        current_cost_per_minute=0.48,
        projected_hourly_cost=0.48 * 60,
        projected_daily_cost=0.48 * 60 * 24,
        cost_trend_short_term="STABLE"
    )

    # Simulate DRA quality
    quality_data = DRAQualityMetrics(
        current_dra_concentration_ppm=10.2,
        compliance_status=True,
        time_in_spec_percentage_last_24h=99.8
    )

    # Simulate pump analytics
    pump_analytics = PumpPerformanceAnalytics(
        pump_id="PUMP001",
        current_efficiency=0.84,
        efficiency_trend="STABLE",
        utilization_percentage_last_24h=95.0,
        last_maintenance_date=datetime(2023, 1, 15)
    )

    print("\n--- UI Layer Data Examples ---")
    print("RealTimeStatus:", current_status_snapshot.model_dump_json(indent=2))
    print("EnergyCostMonitoringData:", energy_data.model_dump_json(indent=2))
    print("DRAQualityMetrics:", quality_data.model_dump_json(indent=2))
    print("PumpPerformanceAnalytics:", pump_analytics.model_dump_json(indent=2))

    print("\nSuccessfully created and validated initial Pydantic models.")

# Note: Some fields like 'Pump Curve' for Pump Power, 'Operating Point' for Efficiency Factor
# are complex and might require their own sub-models or be handled by specific functions
# rather than being fully modeled in Pydantic if they are purely computational inputs.
# The current models provide a good structural foundation based on the specifications.
# 'Covariate Testing Framework' related models are also conceptual for now.
# The `PythonLibraries` model is more for documentation/reference from the spec rather than an active data model.
# `LabAnalysisResult` and `ExternalData` added for completeness of data sources.
# `KPISet` and `DigitalTwinSnapshot` added for high-level representation.
# `PhaseControl` to represent future phase capabilities.
