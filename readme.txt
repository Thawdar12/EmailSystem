CSCI262
==========================
Program Description: 
The Email System Event Modeler & Intrusion Detection System monitors email activity for potential security threats. It processes input email logs, tracks events like logins and email exchanges, and analyzes suspicious patterns. If a security threat is detected, such as unusual login attempts or phishing, the system triggers alerts for administrators. The system is implemented in Python and aims to enhance email system security through real-time monitoring and analysis.


==========================
What I learnt:
- Read and Write Files: Handle input/output files for event and statistical data.
- Libraries and modules: sys, re, scipy, math 
- Event Simulation: Generate random event data using statistical distributions. 
- Statistical Analysis: Calculate mean and standard deviation for baseline event data.
- Anomaly Detection: Identify anomalies by comparing new data to the baseline using a weighted anomaly score.
- Error Handling: Check for inconsistencies in input data.
- Intrusion Detection: Flag unusual events or potential intrusions based on statistical analysis.
- User Interaction: Allow user input for file handling and control the program flow.


==========================
Before executing and running the file, please ensure that you have installed scipy.
If you haven't installed, please follow the steps below:
1. Open your command prompt
2. Type in: "python -m pip install scipy"
3. After installed, you can proceed to the subsequent steps


To execute and run the program for the first time, below are the steps:
1. Open your command prompt
2. Locate the files where you store it. For example: C:\Users\thawdars>
3. Determine how many days you want
4. Type: "IDS.py Events.txt Stats.txt 10" (where 10 is number of days, 
you can replace this with any number)
5. Enter the filename for second stats file
6. Enter the number of days you want to generate for the second set
7.	a. Choose 1 if you want to continue to process another files
	b. Choose 2 if you want to quit the program

