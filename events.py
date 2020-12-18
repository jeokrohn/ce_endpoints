import os
import dotenv
import asyncio
import xows


async def main():
    dotenv.load()
    ce_host = os.getenv('CE_HOST') or 'insert device IP if not set in environment'
    ce_user = os.getenv('CE_USER') or 'insert user if not set in environment'
    ce_pass = os.getenv('CE_PASS') or 'insert password if not set in environment'
    async with xows.XoWSClient(ce_host, username=ce_user, password=ce_pass) as client:
        loop = asyncio.get_running_loop()
        stop = loop.create_future()

        def callback(data, id_):
            print(f'Feedback (Id {id_}): {data}')
            # end the program if we see a volume change
            status = data['Status']
            if status.get('Audio', {}).get('Volume') is not None:
                stop.set_result(True)

        async def subscribe(s, notify_current_value=False):
            return await client.subscribe(s.split(), callback, notify_current_value=notify_current_value)

        await subscribe('Status standby', True)
        await subscribe('Status audio volume')
        # only enable the following line to see all status updates
        # CAUTION: performance impacting. Only use in development
        await subscribe('status')

        print('Change audio volume to end script.')
        await stop


if __name__ == '__main__':
    asyncio.run(main())
