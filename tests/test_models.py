import pytest
from datetime import datetime
from pydantic import ValidationError

from src.models.digital_twin_models import (
    PumpType,
    PumpStatus,
    SensorType,
    ReportingMethod,
    SensorConfig,
    Pump,
    InjectionUnit,
    HMInterface,
    DRAInjectionSkid,
    SensorDataPoint,
    MinuteLevelData,
    EnergyCostFactors,
    DRAEffectivenessFactors,
    LabAnalysisResult,
    ExternalData,
    ModelType,
    TargetVariable,
    VertexAITrainingConfig,
    OptimizationConstraints,
    OptimizedAction,
    OptimizedSchedule,
    RealTimeStatus,
    EnergyCostMonitoringData,
    DRAQualityMetrics,
    PumpPerformanceAnalytics,
    SevenDayOptimizationPlanDisplay,
    HistoricalTrendDataPoint,
    CovariateCandidate,
    KPISet,
    DigitalTwinState,
    ImplementationPhase,
    PythonLibraries
)

# Need to import timedelta for OptimizedSchedule test
from datetime import timedelta

def test_pump_creation():
    """Test basic Pump model instantiation."""
    pump = Pump(pump_id="P001", pump_type=PumpType.PRIMARY, horsepower=500.0, current_status=PumpStatus.ON)
    assert pump.pump_id == "P001"
    assert pump.pump_type == PumpType.PRIMARY
    assert pump.current_status == PumpStatus.ON

def test_sensor_config_creation():
    """Test basic SensorConfig model instantiation."""
    sensor = SensorConfig(
        sensor_id="F1",
        sensor_type=SensorType.FLOW_RATE,
        location="Pipeline Entry",
        purpose="Monitor incoming fuel flow",
        reporting_method=ReportingMethod.EXCEPTION_BASED_MQTT
    )
    assert sensor.sensor_id == "F1"
    assert sensor.sensor_type == SensorType.FLOW_RATE

def test_dra_injection_skid_creation():
    """Test DRAInjectionSkid model with nested models."""
    pump1 = Pump(pump_id="P001", pump_type=PumpType.PRIMARY, current_status=PumpStatus.OFF)
    pump2 = Pump(pump_id="P002", pump_type=PumpType.BACKUP, current_status=PumpStatus.OFF)
    sensor_f1 = SensorConfig(sensor_id="F1", sensor_type=SensorType.FLOW_RATE, location="Entry", purpose="Test")

    skid = DRAInjectionSkid(
        skid_id="SKID01",
        primary_pump=pump1,
        backup_pump=pump2,
        injection_unit=InjectionUnit(),
        hmi_interface=HMInterface(),
        sensors=[sensor_f1]
    )
    assert skid.skid_id == "SKID01"
    assert skid.primary_pump.pump_id == "P001"
    assert len(skid.sensors) == 1
    assert skid.sensors[0].sensor_id == "F1"

def test_sensor_data_point_creation():
    """Test SensorDataPoint model."""
    now = datetime.now()
    data_point = SensorDataPoint(timestamp=now, sensor_id="T1", value=25.5, units="Celsius")
    assert data_point.sensor_id == "T1"
    assert data_point.value == 25.5
    assert data_point.timestamp == now

def test_minute_level_data_creation():
    """Test MinuteLevelData model."""
    ts = datetime.now().replace(second=0, microsecond=0)
    minute_data = MinuteLevelData(
        timestamp=ts,
        flow_rate_f1=1200.5,
        pump_status_s1=PumpStatus.ON, # Assuming S1 directly reports PumpStatus enum
        pressure_p1=250.7,
        dra_injection_rate_actual=10.2,
        energy_cost_per_minute=0.75,
        pump_power_kw=45.0,
        pump_efficiency_factor=0.85
    )
    assert minute_data.timestamp == ts
    assert minute_data.flow_rate_f1 == 1200.5
    assert minute_data.pump_status_s1 == PumpStatus.ON

def test_energy_cost_factors_creation():
    """Test EnergyCostFactors model."""
    factors = EnergyCostFactors(
        flow_rate=1000.0,
        pressure=200.0,
        pump_age_years=2.0,
        pump_operating_point_efficiency=0.75,
        maintenance_history_factor=0.98,
        static_energy_rate_per_kwh=0.12,
        operating_time_minutes=1.0
    )
    assert factors.flow_rate == 1000.0
    assert factors.static_energy_rate_per_kwh == 0.12

def test_vertex_ai_training_config():
    """Test VertexAITrainingConfig model."""
    config = VertexAITrainingConfig(
        model_types=[ModelType.LSTM, ModelType.PROPHET],
        target_variables=[TargetVariable.ENERGY_COST_PER_MINUTE],
        feature_columns=["feat1", "feat2"]
    )
    assert ModelType.LSTM in config.model_types
    assert TargetVariable.ENERGY_COST_PER_MINUTE in config.target_variables

def test_optimization_constraints():
    """Test OptimizationConstraints model."""
    constraints = OptimizationConstraints(
        min_dra_concentration_ppm=5.0,
        max_dra_concentration_ppm=15.0
    )
    assert constraints.min_dra_concentration_ppm == 5.0

def test_optimized_schedule():
    """Test OptimizedSchedule with OptimizedAction."""
    now = datetime.now()
    constraints = OptimizationConstraints(min_dra_concentration_ppm=5.0, max_dra_concentration_ppm=15.0)
    action1 = OptimizedAction(
        timestamp=now,
        duration_minutes=60,
        dra_injection_rate_ppm=10.0,
        active_pump=PumpType.PRIMARY
    )
    schedule = OptimizedSchedule(
        plan_id="TestPlan001",
        planning_horizon_start=now,
        planning_horizon_end=now + timedelta(days=7),
        actions=[action1],
        constraints_details=constraints
    )
    assert schedule.plan_id == "TestPlan001"
    assert len(schedule.actions) == 1
    assert schedule.actions[0].dra_injection_rate_ppm == 10.0

def test_real_time_status_aliases():
    """Test RealTimeStatus model with aliases."""
    now = datetime.now()
    status = RealTimeStatus(
        current_timestamp=now,
        flowRateF1GPM=1500.0, # Using alias
        pumpStatusPrimary=PumpStatus.ON,
        pressureP1PSI=300.0
    )
    assert status.flow_rate_f1_gpm == 1500.0
    assert status.model_dump(by_alias=True)['flowRateF1GPM'] == 1500.0

def test_kpi_set_aliases():
    """Test KPISet model with aliases."""
    kpis = KPISet(
        energyCostPerBarrelUSD=2.50,
        pumpUptimePercentage=99.9
    )
    assert kpis.energy_cost_per_barrel_usd == 2.50
    assert kpis.model_dump(by_alias=True)['energyCostPerBarrelUSD'] == 2.50

# Example of a validation error test (optional, but good for completeness)
def test_sensor_config_missing_required_field():
    """Test that a required field missing raises ValidationError."""
    with pytest.raises(ValidationError):
        SensorConfig(
            sensor_type=SensorType.PRESSURE, # sensor_id is missing
            location="Test Location",
            purpose="Test Purpose"
        )

def test_python_libraries_default():
    """Test PythonLibraries model uses default factory."""
    libs = PythonLibraries()
    assert "pandas" in libs.data_processing
    assert "tensorflow" in libs.machine_learning

# Add more tests for other models as needed to ensure basic instantiation.
# This provides a basic check that models are defined and can be used.
# More comprehensive tests would validate specific business logic within model methods or validators if they exist.
