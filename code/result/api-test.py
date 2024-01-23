import asyncio
import httpx

async def main():
    moto_file = 'index-22_test-bucket_timestamp-2024-01-23-17-55-49.jpg'
    file_path = './data/'+moto_file
    async with httpx.AsyncClient() as client:
        # Open the image file in binary read mode and read its content
        with open(file_path, "rb") as file:
            files = {"init_image": (moto_file, file, "image/jpg")}
            response = await client.post('http://10.32.88.26/img2img', files=files, timeout=None)

        # If response is successful and contains binary data
        if response.status_code == 200:
            file_name = "./out/output.jpg"  # Name of the output file
            with open(file_name, "wb") as file:
                file.write(response.content)  # Write binary content to the file
            print(f"Successfully uploaded {file_name}")
        else:
            print(f"Failed to upload {file_name}. Status: {response.status_code}, Response: {response.text}")

if __name__ == '__main__':
    asyncio.run(main())
