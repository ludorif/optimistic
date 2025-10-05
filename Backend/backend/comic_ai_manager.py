from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from magic_hour import Client
import os

import os.path

import boto3
from botocore.exceptions import NoCredentialsError, ClientError


async def generate(summary_content):
    await upload_results()
    return
    client = Client(token=os.environ["MAGIC_HOUR_KEY"])

    result = client.v1.ai_image_generator.generate(
        image_count=4,
        orientation="landscape",
        style={
            "prompt": summary_content
        },
        wait_for_completion=True, # wait for the render to complete
        download_outputs=True, # download the outputs to local disk
        download_directory="outputs", # save the outputs to the "outputs" directory
    )

    print(f"created image with id {result.id}, spent {result.credits_charged} credits. Outputs are saved at {result.downloaded_paths}")
    await upload_results()

async def upload_results():
    s3_client = boto3.client('s3')

    for x in range(1, 5):
        try:
            filename = f"output-{x}.png"
            s3_client.upload_file(
                Filename=f'outputs/{filename}',
                Bucket='optimisticimages',
                Key=filename,
                ExtraArgs={'ACL': 'public-read'}
            )

            print(f"{filename} successfully uploaded")

        except FileNotFoundError:
            print("The file was not found.")
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print("Error uploading file:", e)