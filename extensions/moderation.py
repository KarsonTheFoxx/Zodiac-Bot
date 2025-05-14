from disnake.ext import commands
from disnake_plugins import Plugin
from disnake import Embed, Member, Role, Color, CommandInteraction
from datetime import datetime
plugin = Plugin(name="Moderation")


@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
@plugin.slash_command(name="ban", description="Bans selected user")
async def ban(inter:CommandInteraction, member:Member, reason:str=None):
    if not reason:
        reason = f"No reason provided | requested by {inter.author.name}({inter.author.id}) | {datetime(datetime.now("UTC"))}"

    await member.ban(clean_history_duration=604800, reason=reason)
    await inter.response.send_message(embed=Embed(title=f"Banned {member.name}({member.id})", description=reason, color=Color.red()), ephemeral=True)

@ban.error
async def on_ban_error(inter:CommandInteraction, error):
    embed = Embed(title="Error", color=Color.red())
    if isinstance(error, commands.MissingPermissions):
        embed.description = "You do not have permission to ban this member"
        ban.reset_cooldown()
    elif isinstance(error, commands.BotMissingPermissions):
        embed.description="Bot does not have permission to do this"
    elif isinstance(error, commands.CommandOnCooldown):
        embed.description = f"Command on cooldown! retry after {round(error.retry_after, 2)} seconds!"
        embed.set_footer("You can use this command once every 60 seconds")
    
    await inter.response.send_message(embed=embed, ephemeral=True)

setup, teardown = plugin.create_extension_handlers()
print(type(ban))