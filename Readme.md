
![Wireless Network Monitor](https://i.imgur.com/wox8I10.png)

# Table of Contents
- [Problem](#problem)
- [Solution](#solution)
- [Technologies](#technologies)
- [Screenshots](#screenshots)
- [Usage](#usage)

# Problem
Wireless network monitoring in the practical field has traditionally fallen under the purview of network administrators. Network administrators would have to be able to overlook their networks and be able to diagnose a problem when it occurred and thus much of the tools available in the current market are geared towards network administrators. In the modern world, with the introduction of smart devices and data-heavy websites (i.e streaming content), home networks have to support much more devices and a larger volume of data. However, data is a valuable resource - many internet providers offer a metered connection or an unlimited data plan with a limited high-speed capacity. Therefore it is quite common for households to run out of monthly data without knowing where and on what the data was utilized. 

# Solution
This project will aim to address this issue by implementing a novel wireless network monitoring plug and play solution targeted at small network owners such that they can better manage their data utilization. The WNM project consists of two separate implementations working together. The first is an onsite raspberry pi with a wireless network sniffer that gathers information from the network and uploads it to the second implementation - a distributed data processing pipeline that is powered in the cloud. 
![Implementation Architecture](https://camo.githubusercontent.com/9d860940fc1d5d0a45118895d709b7b90a4687514cef581ed430ad8de89ee43d/68747470733a2f2f692e696d6775722e636f6d2f79564544334c592e706e67)


# Technologies
- [Python](https://www.python.org/)
- [AWS](https://aws.amazon.com/)
- [tcpdump](https://www.tcpdump.org/)
- [Grafana](https://grafana.com/)

# Screenshots
Dashboard
![Dashboard](https://i.imgur.com/cL1e0QZ.png)

Locations Visited
![Locations Visited](https://i.imgur.com/BfdadA9.png)

# Usage
1. Clone the repo onto the raspberry pi
```
git clone https://github.com/dca123/HomeWirelessNetwork-Monitor
```
2. Configure the raspberry as seen in [rasppi.config](https://github.com/dca123/HomeWirelessNetwork-Monitor/blob/main/rasppi.config)
3. Create an AWS Lambda function with the code provided in [addToDb.py](https://github.com/dca123/HomeWirelessNetwork-Monitor/blob/main/addToDb.py)
4. Configure the S3 bucket
5. Run the script on the raspberry
```
python script.py
``` 
