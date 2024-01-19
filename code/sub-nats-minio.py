import asyncio
from minio import Minio
from nats.aio.client import Client as NATS
from dotenv import load_dotenv
import os
import nats

dat1a = ""  # Global variable to store data from NATS
message_received = asyncio.Event()  # Event to signal when a message is received

async def main():
    print("ready")
    load_dotenv()
    print("setting..")
    # Initialize MinIO client
    ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
    SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
    MINIO_CLIENT = Minio(os.getenv('MINIO_ADDRESS'), access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

    # Initialize NATS client
    nc = await nats.connect(os.getenv('NATS_ADDRESS'))
    print("start")
    while True:
        async def message_handler(msg):
            global dat1a
            dat1a = msg.data.decode()
            message_received.set()  # Signal that a message has been received

        # Subscribe to NATS topic
        await nc.subscribe("cctv.detect", cb=message_handler)

        # Wait for a message to be received
        await message_received.wait()
        await asyncio.sleep(1)
        print(dat1a)
        BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')
        OBJECT_NAME = dat1a  # Use the data received from NATS
        DEST_FILE_NAME = "./data/" + OBJECT_NAME  # Local file path

            # Download the object from MinIO
        try:
            MINIO_CLIENT.fget_object(BUCKET_NAME, OBJECT_NAME, DEST_FILE_NAME)
            print(f"Successfully downloaded {OBJECT_NAME} to {DEST_FILE_NAME}")
        except Exception as e:
            print(f"Failed to download {OBJECT_NAME}. Reason: {e}")

        # Close NATS connection
    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())
