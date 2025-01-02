# Email System Event Modeler & Intrusion Detection System

## Program Description
The **Email System Event Modeler & Intrusion Detection System** monitors email activity for potential security threats. It processes input email logs, tracks events like logins and email exchanges, and analyzes suspicious patterns. If a security threat is detected, such as unusual login attempts or phishing, the system triggers alerts for administrators. 

The system is implemented in Python and aims to enhance email system security through real-time monitoring and analysis.

## What I learnt
- **Read and Write Files**: Handle input/output files for event and statistical data.
- **Libraries and modules**: sys, re, scipy, math 
- **Event Simulation**: Generate random event data using statistical distributions. 
- **Statistical Analysis**: Calculate mean and standard deviation for baseline event data.
- **Anomaly Detection**: Identify anomalies by comparing new data to the baseline using a weighted anomaly score.
- **Error Handling**: Check for inconsistencies in input data.
- **Intrusion Detection**: Flag unusual events or potential intrusions based on statistical analysis.
- **User Interaction**: Allow user input for file handling and control the program flow.

## Prerequisites
Before executing the program, please ensure that you have installed the necessary Python library `scipy`.

To install `scipy`, follow these steps:
1. Open your command prompt.
2. Type the following command:
   ```bash
   python -m pip install scipy

