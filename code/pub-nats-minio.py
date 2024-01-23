import asyncio
import nats
import cv2
from minio import Minio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv

load_dotenv()
# MinIO Configuration
ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
ADDRESS = os.getenv('MINIO_ADDRESS')
MINIO_CLIENT = Minio(ADDRESS, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')

def save_and_upload(frame, frame_count, c_time):
    filename = f'index-{frame_count}_{BUCKET_NAME}_timestamp-{c_time}.jpg'
    cv2.imwrite(filename, frame)
    MINIO_CLIENT.fput_object(BUCKET_NAME, filename, filename)

async def main():
    # Check if bucket exists, else create
    if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
        MINIO_CLIENT.make_bucket(BUCKET_NAME)
    print("Bucket connected")

    nc = await nats.connect(os.getenv('NATS_ADDRESS'))
    js = nc.jetstream()
    await js.add_stream(name=os.getenv('NATS_STREAM_NAME'), subjects=[os.getenv('NATS_SUBJECT')])
    print("NATS connected")

    # Capture video from the default camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
    # Set capture frame rate
    cap.set(cv2.CAP_PROP_FPS, 60)
    print("Ready to capture")

    frame_count = 0
    executor = ThreadPoolExecutor(max_workers=10)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            c_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            # Offload the save and upload task to a thread
            executor.submit(save_and_upload, frame, frame_count, c_time)
            # Publish the filename to NATS
            filename = f'index-{frame_count}_{BUCKET_NAME}_timestamp-{c_time}.jpg'
            await js.publish(os.getenv('NATS_SUBJECT'), filename.encode())

            frame_count += 1
            # Adjust sleep time if necessary for your specific hardware
            if (frame_count%20) == 0 : print(filename); os.system(f'rm -rf *.jpg')
            await asyncio.sleep(1/60)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        await nc.close()
        executor.shutdown(wait=True)

if __name__ == '__main__':
    asyncio.run(main())
