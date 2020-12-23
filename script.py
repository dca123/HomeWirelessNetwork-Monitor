import subprocess, asyncio
import uuid, sys, time
import boto3
from datetime import datetime


def upload_to_aws(file):
    s3 = boto3.client('s3')
    filename = 'test' + uuid.uuid1().hex + '.txt'
    try:
        s3.upload_file(file, "hwnm", filename)
        print("upload success")
        return True
    except FileNotFoundError:
        print("File not found")
        return False

async def stream_tcpdump():
    p = await asyncio.create_subprocess_exec(
        'tcpdump', '-i', 'enp3s0', '-v', '-ln',
        stdout=asyncio.subprocess.PIPE
    )
    while True:
        line = await p.stdout.readuntil(b' IP ')
        sys.stdout.write(line.decode('utf-8'))

async def create_file(timeout):
    while True:
        sys.stdout.close()
        time = datetime.now().strftime("%d%m%Y%H%M%S")
        fileName = 'test' + time + '.txt'
        sys.stdout = open(fileName, "w")
        await asyncio.sleep(timeout)
        upload_to_aws(fileName)


async def main():
    reportingFreq = 30
    task = asyncio.create_task(stream_tcpdump())
    task2 = asyncio.create_task(create_file(reportingFreq))
    await asyncio.gather(task, task2)


asyncio.run(main())


# upload_to_aws("test.txt")
