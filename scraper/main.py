from autoria_scraper.src.autoria_scraper.scraper import AutoRiaScraper
import boto3
from datetime import datetime
import asyncio
import aiohttp
import json


s3 = boto3.client('s3')
bucket = "autoria-data-bucket"


def save_object(data, bucket, bn):
    now = datetime.now()
    objectPath = f"{now.strftime('%Y/%m/%d/%H:%M:%S')}.json"
    object_name = f"landing/ingestion_date={now.strftime('%Y-%m-%d')}/cars_data_lp_{bn:02d}.json"
    data_str = json.dumps(data)
    bytes_stream = bytes(data_str.encode('UTF-8'))
    s3.put_object(Bucket=bucket, Key=object_name, Body=bytes_stream)


async def main():
    bn = 0
    scraper = AutoRiaScraper()
    async with aiohttp.ClientSession() as session:
        async for batch in scraper.get_cars_data_in_batches_async(100, 0, session, deserialize=False):
            save_object(batch, bucket, bn)
            bn = bn + 1

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
