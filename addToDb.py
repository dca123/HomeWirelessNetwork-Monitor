from pprint import pprint
import boto3
import botocore
import uuid
import re
import io
import os
from datetime import date
import psycopg2

ipPattern = "([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
timePattern = "(\d+:\d+:\d+)"
firstValPattern = "(\d+:\d+:\d+.\d+)"

def getLogFile():    
    objs = s3.list_objects_v2(Bucket='hwnm')['Contents']
    latest = max(objs, key=lambda x: x['LastModified'])
    print(latest)
    try:
        file = boto3.resource('s3').Object(
            'hwnm', latest['Key']).get()['Body'].read()
        return file
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("Object doesn't exist")
            return False
        else:
            print("Something went wrong downloading the log file!")
            return False


def parseFile(logFile):
    buf = io.BytesIO(logFile)
    with buf as fp:
        line = fp.readline().decode("utf-8")
        # print(line)
        lineNum = 1
        while line:            

            lineVals = line.strip().split(" ")
            # print(lineVals)
            if not re.match(firstValPattern, lineVals[0]) or lineVals[1] != 'IP':
                line = fp.readline().decode("utf-8")
                continue

            lineTwo = fp.readline().decode("utf-8")
            if not lineTwo:
                line = fp.readline().decode("utf-8")
                continue
            lineTwoVals = lineTwo.strip().split(" ")


            # print(lineTwoVals)

            # dateToday = date.today()
            # time = lineVals[0]
            # protocol = 'IPv4' if lineVals[1] == 'IP' else 'IPv6'
            
            sourceIPVals = re.split(ipPattern, lineTwoVals[0])
            destinationIPVals = re.split(ipPattern, lineTwoVals[2])
            
            # sourceIP = sourceIPVals[1]
            # sourceIPPort = sourceIPVals[2].replace(".", "")

            # destinationIP = destinationIPVals[1]
            # destinationIPPort = destinationIPVals[2].replace(".", "")

            # flags = lineVals[11]
            # packetProtocol = lineTwoVals[3]
            # packetSize = lineTwoVals[5]
            
            if lineTwoVals[4][0] == '[':
                flags = list(lineTwoVals[4].replace("[", "").replace("],", ""))
            else:
                flags = ""
            

            # dataDict = {
            #     'id': str(uuid.uuid1()),
            #     'date': date.today().strftime("%d-%m-%Y"),
            #     'time': re.split(timePattern, lineVals[0])[1],
            #     'protocol': 'IPv4' if lineVals[1] == 'IP' else 'IPv6',
            #     'sourceIP': sourceIPVals[1],
            #     'sourcePort': sourceIPVals[2].replace(".", ""),
            #     'destinationIP': destinationIPVals[1],
            #     'destinationPort': destinationIPVals[2].replace(".", "").replace(":", ""),
            #     'flags': flags,
            #     'packetProtocol': lineVals[13].replace(",", ""),
            #     'packetSize': lineVals[16].replace(")", "")
            # }

            sql = """
                INSERT INTO traffic(id, logdatetime, protocol, sourceip, sourceport, destinationip, destinationport, flags, packetprotocol, packetsize) 
                VALUES (%s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """
            # currentDate = date.today().strftime("%m-%d-%Y ") + re.split(timePattern, lineVals[0])[1]
            currentDate = "12-20-2020 " + re.split(timePattern, lineVals[0])[1]
            data = (
                str(uuid.uuid1()),
                currentDate,
                # date.today().strftime("%m-%d-%Y "+ re.split(timePattern, lineVals[0])[1]),
                'IPv4' if lineVals[1] == 'IP' else 'IPv6',
                sourceIPVals[1],
                sourceIPVals[2].replace(".", ""),
                destinationIPVals[1],
                destinationIPVals[2].replace(".", "").replace(":", ""),
                flags,
                lineVals[13].replace(",", ""),
                lineVals[16].replace(")", "")
            )
            print(data)
            cur.execute(sql, data)
            conn.commit()
            # print(dataDict)
            # if not add_log(dataDict):
            #     print("Error pushing to DB")

            line = fp.readline().decode("utf-8")
            lineNum +=2 
        print(lineNum)

def add_log(dataDict):
    # dataDict = {
    #     'id': str(uuid.uuid1()),
    #     'date': '20-12-2020',
    #     'time': '09:56',
    #     'protocol': 'IPv4',
    #     'sourceIP': '192.168.0.6',
    #     'sourcePort':  '50314',
    #     'destinationIP': '13.225.41.143',
    #     'destinationPort': '443',
    #     'flags': ['P', 'R'],
    #     'packetProtocol': 'TCP',
    #     'packetSize': '40'
    # }

    
    table = dynamodb.Table('Traffic')
    response = table.put_item(Item=dataDict)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        print("Something went wrong uploading to the database")
        return False
    
if __name__ == "__main__":
    # dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    conn = psycopg2.connect(
        host="",
        database="",
        user="",
        password=""
        )
    cur = conn.cursor()
    cur.execute('Select version()')
    db_version = cur.fetchone()
    print(db_version)

    s3 = boto3.client('s3', region_name='us-east-1')

    parseFile(getLogFile())
