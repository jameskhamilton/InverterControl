# Inverter Control

## Introduction

Welcome to my Inverter Control project! This project is dedicated to interfacing with a Solis inverter to manage and optimise battery charging and discharging schedules.

## Purpose

The primary goal of the Inverter Control project is to:

- **Read dataset from the Solis inverter:** To understand the current energy generation and usage patterns.
- **Update the time to charge and discharge the battery:** Ability to adjusts the battery's charging and discharging times to ensure efficient energy use.
- **Read dataset from Octopus Agile tariff:** This feature integrates the pricing data from the Octopus Agile tariff, to read upcoming prices.

## To-Do

- **Add more detail about setting up credentials for Octopus and Solis API:** Documenting the steps needed to get credentials for API access.
- **Integrate Octopus Agile daily tariff to charge the battery when it's cheap:** The next step in the project is to fully integrate the Octopus Agile tariff data. This will allow the system to charge the battery during periods of lower energy costs.

## Installation and Running the Project

To get started with the Inverter Control project, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jameskhamilton/InverterControl
   ```

2. **Run Setup**

Navigate to the cloned directory and run the setup file:

   ```bash
   python __setup__.py
   ```

This will prompt for the credentials needed to work with the Solis and Octopus APIs.

3. **Run the Project**

After the setup is complete, start the project using:

   ```bash
   python __run__.py
   ```

This script initiates the main functionality of the project.