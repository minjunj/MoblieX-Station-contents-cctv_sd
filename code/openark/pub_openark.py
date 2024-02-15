import argparse
import asyncio
import os
from pprint import pprint as print

from openark import OpenArk


async def publish_image(
    ark: OpenArk,
    filename: str,
    function_name: str
) -> None:
    # define a model
    model = await ark.get_model_channel(function_name)

    # check file
    if not os.path.exists(filename):
        raise ValueError(f"Image file {filename:?} not found!")

    # load payload files
    payload_image_key = 'detect-image.jpg'
    payloads = {
        f'{payload_image_key}': open(filename, 'rb').read(),
    }

    # make an input value
    input = {
        "images": [f"@data:image,{payload_image_key}"],
    }

    # publish image data into the model
    await model.publish(
        input,
        payloads=payloads,
    )


if __name__ == '__main__':
    # define command-line parameters
    parser = argparse.ArgumentParser(
        prog='OpenARK',
        description='OpenARK Python',
    )
    parser.add_argument(
        'filename',
        type=str,
        help='an image file',
    )
    parser.add_argument(  # function_name에 대한 인수를 추가
        '--function_name',
        type=str,
        default='face-detection-sd',  # 기본값 지정
        help='function name to call',
    )

    # parse command-line parameters
    args = parser.parse_args()
    ark = OpenArk()

    asyncio.run(publish_image(ark, args.filename, args.function_name))
