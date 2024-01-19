import asyncio
from minio import Minio
import os
import nats
from dotenv import load_dotenv
from minio.error import S3Error

load_dotenv()

# Initialize MinIO client
ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_CLIENT = Minio(os.getenv('MINIO_ADDRESS'), access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

async def download_from_minio(bucket_name, object_name, dest_file_name, retries=5, delay=1):
    for attempt in range(retries):
        try:
            MINIO_CLIENT.fget_object(bucket_name, object_name, dest_file_name)
            print(f"Successfully downloaded {object_name} to {dest_file_name}")
            print("i runnging API!!!") # Insert Stable Diffusion API
            break
        except S3Error as e:
            if e.code == "NoSuchKey" and attempt < retries - 1:
                print(f"Object {object_name} not found, retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                print(f"Failed to download {object_name}. Reason: {e}")
                break

async def message_handler(msg):
    object_name = msg.data.decode()
    bucket_name = os.getenv('MINIO_BUCKET_NAME')
    dest_file_name = "./data/" + object_name

    # Schedule the download task
    asyncio.create_task(download_from_minio(bucket_name, object_name, dest_file_name))

async def main():
    # Initialize NATS client
    nc = await nats.connect(os.getenv('NATS_ADDRESS'))

    # Subscribe to NATS topic and handle messages
    await nc.subscribe("cctv.detect", cb=message_handler)

    try:
        # Keep the coroutine running
        await asyncio.Future()
    finally:
        # Close NATS connection
        await nc.close()

if __name__ == '__main__':
    asyncio.run(main())
