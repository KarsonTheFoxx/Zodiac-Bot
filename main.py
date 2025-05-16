from disnake.ext import commands
from disnake import Activity, ActivityType, Intents
from asyncio import run

async def main():
    from dotenv import load_dotenv
    load_dotenv("./.env")
    from os import environ
    intents = Intents(members=True, messages=True, message_content=True, guilds=True)
    bot = commands.InteractionBot(owner_id=855948446540496896, intents=intents)

    @bot.event
    async def on_ready():
        await bot.wait_until_first_connect()
        await bot.change_presence(activity=Activity(name="Zodiac SMP", type=ActivityType.playing))
        print("Ready")

    bot.load_extensions("./extensions/")
    bot.reload = True
    await bot.start(token=environ.get("TOKEN"))


if __name__ == "__main__":
    run(main())