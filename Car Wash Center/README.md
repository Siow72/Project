# Car Wash Queue Simulator

This project simulates a **car wash center** with **three wash bays** and a single queue system. Customers (cars) arrive randomly, each requiring a different type of service. The simulation uses user-selected random number generators to determine inter-arrival times, service types, and wash durations. Results are printed with detailed timing logs and statistical evaluations.

---

## File Structure

| File           | Description |
|----------------|-------------|
| `Main.m`       | Main program entry point where user selects RNG and runs the simulation |
| `Simulation.m` | Runs the core simulation: event queue, service, departure, and output |
| `LCG.m`        | Linear Congruential Generator (LCG) implementation |
| `UD.m`         | Uniform Distribution random number generator |
| `randProb.m`   | Maps random numbers to CDF-based values for time/type |
| `interTable.m` | Generates inter-arrival time table |
| `bayTable.m`   | Generates service time tables for all three wash bays |
| `typeTable.m`  | Generates service type table |
| `separate.m`   | Assigns cars to wash bays and generates bay-specific output |

---

## Simulation Features

- Queue simulation for a car wash with **3 wash bays**
- Randomly generated:
  - **Inter-arrival times**
  - **Service times** (per bay)
  - **Service type** (user-specific)
- Custom RNG options:
  - `LCG`: Linear Congruential Generator
  - `UD`: Uniform distribution via built-in `rand`
- Simulation output includes:
  - Arrival, service start, departure messages
  - Detailed event table for each bay
  - Final statistical evaluation

---

## Statistical Evaluation Outputs

- Average inter-arrival time
- Average waiting time
- Average time spent in the system
- Average service time per wash bay
- Probability a car had to wait

---
