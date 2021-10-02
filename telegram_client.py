from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from asyncio import gather, sleep

from time import strftime
from json import load as json_load

with open('client-config.json') as f:
	CONFIG = json_load(f)

client = TelegramClient('telegram-group-client', CONFIG['telegram']['api_id'], CONFIG['telegram']['api_hash'])


async def groups_input_parse(groups_file_path):
	groups_input_data = []

	with open(groups_file_path) as f:
		for row in f.readlines():
			row = row.rstrip().split('|')
			row = [await client.get_entity(row[0])] + row
			groups_input_data.append(row)

	return groups_input_data


async def join_groups(groups_input_data):
	for row in groups_input_data:
		await client(JoinChannelRequest(row[0]))


async def send_message_process(channel, message, delay):
	while True:
		try:
			await client.send_message(channel, message)
			print('[Info] Send message to ->', channel.title + ' ', strftime(strftime("%d.%m.%Y, %H:%M:%S")))
			await sleep(delay)

		except Exception as e:
			print('[Error] ', e)


async def main():
	groups_input_data = await groups_input_parse(CONFIG['script']['input_file_path'])
	await join_groups(groups_input_data)

	# - Send messages run
	await gather(*[send_message_process(data[0], data[2], int(data[3])) \
		for data in groups_input_data]
	)


with client:
	client.loop.run_until_complete(main())