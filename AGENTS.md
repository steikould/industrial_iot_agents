# Agent Instructions for DRA Injection Skid Digital Twin Project

## General Guidelines

1.  **Understand the Goal:** The primary objective is to build a digital twin to optimize pump energy costs for DRA (Drag Reducing Agent) injection while maintaining fuel quality standards. Refer to the technical specifications and `docs/system_architecture.svg` for complete context.
2.  **Pydantic Models:** All data structures should be defined using Pydantic models located in `src/models/`. Ensure models are typed correctly and include descriptions where helpful.
3.  **Python Version:** Target Python 3.9+.
4.  **GCP Integration:** Components related to Google Cloud Platform services (Vertex AI, BigQuery, Pub/Sub, Cloud Functions) should be placed in `src/gcp_integration/`.
5.  **Core Logic:** Business logic, such as time spine generation, energy cost calculations, and DRA effectiveness modeling, should reside in `src/core/`.
6.  **Placeholders:** The initial structure contains placeholder functions. When implementing these, replace the placeholder logic with robust solutions according to the specifications. Clearly document any assumptions made.
7.  **Testing:** While not explicitly requested in the initial setup, new functionality should ideally be accompanied by tests in the `tests/` directory. (This is a general best practice).
8.  **Dependencies:** External Python library dependencies will eventually be managed in a `requirements.txt` file. For now, any new libraries used should be noted.
9.  **Commit Messages:** Follow standard conventions: a short subject line (50 chars max), a blank line, and a more detailed body if necessary.
10. **Branching:** Use descriptive branch names for features or significant changes (e.g., `feature/time-spine-impl`, `fix/energy-calc-bug`).

## Specific Instructions for Current Phase (Phase 1: Monitoring & Analytics)

*   **Focus on Placeholders:** The immediate next steps will likely involve fleshing out the placeholder functions in `src/core/` and `src/gcp_integration/`.
*   **Energy Calculation Logic:** Pay close attention to the energy cost calculation formula and the definitions of "Pump Power" and "Efficiency Factor" from the technical specifications. The placeholder in `src/core/energy_calculation.py` highlights some ambiguities that need careful resolution during actual implementation.
*   **Time Spine Generation:** The `create_time_spine` function in `src/core/time_spine.py` needs a robust implementation for sorting, forward-filling, and interpolation.
*   **Optimization Engine:** The `optimize_injection_schedule` in `src/gcp_integration/optimization.py` is a critical component. Its placeholder should eventually be replaced with code that interfaces with an optimization solver (e.g., using libraries like `PuLP`, `CVXPY`, or GCP's Vertex AI Optimization).

## Future Phases

*   **Phase 2 (Bidirectional Control):** Will involve implementing logic to send control signals back to the physical DRA skid. This will require careful design for safety and reliability.
*   **Phase 3 (Full Pipeline Digital Twin):** Will expand the scope to multiple locations and network-wide optimization.

## Questions and Clarifications

If any part of the technical specifications or requirements is unclear, please ask for clarification before proceeding with a complex implementation.
