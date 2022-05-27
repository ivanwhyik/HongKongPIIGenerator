# HongKongPIIGenerator
Create Dummy PII CSV file for Exfiltration Testing

Types of file:
- Name, HKID, Date of Birth, Address, Phone Number 

# Usage
`python HongKongPIIGenerator.py -n <number of records>`

Generate 100MB data (1MB = ~10000 record)

`python HongKongPIIGenerator.py -n 1000000`

Update building and street list

`python HongKongPIIGenerator.py -n <number of records> -u`
  
# To-do
HKID check digit
Credit Card Number
