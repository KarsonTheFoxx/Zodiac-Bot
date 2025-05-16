from disnake_plugins import Plugin
from disnake.ext import commands
from disnake import ui, ButtonStyle, TextInputStyle, Color, Embed, CommandInteraction, ModalInteraction, MessageInteraction, utils, TextChannel, CategoryChannel, PermissionOverwrite, Role
from asyncio import sleep
from random import randint

plugin = Plugin(name="tickets")

class closeTicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=0)
    
    @ui.button(label="Close ticket", style=ButtonStyle.red)
    async def close_ticket(self, button:ui.Button, inter:MessageInteraction):
        await inter.response.send_message(f"Closing ticket in <t:{int(utils.utcnow().timestamp())+5}:R>")
        await sleep(5)
        await inter.channel.delete(reason=f"Ticket close | Closed by {inter.author.name}")



class createTicketModal(ui.Modal):
    def __init__(self, category_channel, moderator_role):
        self.category_channel = category_channel
        self.moderator_role = moderator_role

        self.AUTHOR_PERMISSION_OVERWRITE = PermissionOverwrite()
        self.AUTHOR_PERMISSION_OVERWRITE.send_messages = True
        self.AUTHOR_PERMISSION_OVERWRITE.view_channel = True

        self.EVERYONE_PERMISSIONS_OVERWRITE = PermissionOverwrite()
        self.EVERYONE_PERMISSIONS_OVERWRITE.view_channel = False

        self.MODERATOR_PERMISSION_OVERWRITES = PermissionOverwrite()
        self.MODERATOR_PERMISSION_OVERWRITES.view_channel = True
        self.MODERATOR_PERMISSION_OVERWRITES.send_messages = True

        components = [
            ui.TextInput(label="Ticket name", custom_id="name", placeholder="Report hacker", required=True, max_length=100, style=TextInputStyle.single_line),
            ui.TextInput(label="Description", custom_id="description", placeholder="I caught 2known was hacking on camera!", required=True, max_length=2000, style=TextInputStyle.paragraph)
        ]
        super().__init__(title="Create ticket", components=components, timeout=500)
    
    async def callback(self, inter:ModalInteraction):
        embed = Embed(color=Color.red())
        embed.title = inter.text_values["name"]
        embed.description = inter.text_values["description"]
        embed.set_author(name=inter.author.name)

        user_tickets = [ticket for ticket in self.category_channel.channels if str(inter.author.id) in ticket.name]
        ticket_names = [ticket.name for ticket in user_tickets]
        ticket_name = "{0}-{1}".format(str(inter.author.id), len(user_tickets))

        while ticket_name in ticket_names:
            ticket_name += str(randint(0, 9))

        ticket = await inter.guild.create_text_channel(name=ticket_name, reason="Ticket creation", category=self.category_channel)

        await ticket.set_permissions(target=inter.author, overwrite=self.AUTHOR_PERMISSION_OVERWRITE)
        await ticket.set_permissions(target=inter.guild.default_role, overwrite=self.EVERYONE_PERMISSIONS_OVERWRITE)
        await ticket.set_permissions(target=self.moderator_role, overwrite=self.MODERATOR_PERMISSION_OVERWRITES)

        await ticket.send(f"{inter.author.mention}{self.moderator_role.mention}\n-# Ticket opened <t:{int(utils.utcnow().timestamp())}:R> (<t:{int(utils.utcnow().timestamp())}:F)", embed=embed, view=closeTicketView())
        await inter.response.send_message(embed=Embed(title="Ticket created", color=Color.green()), ephemeral=True)

class createTicketView(ui.View):
    def __init__(self, category_channel, moderator_role):
        self.category_channel = category_channel
        self.moderator_role = moderator_role
        super().__init__(timeout=0)
    
    @ui.button(label="Create ticket", style=ButtonStyle.green)
    async def create_ticket(self, button: ui.Button, inter:MessageInteraction):
        await inter.response.send_modal(createTicketModal(category_channel=self.category_channel, moderator_role=self.moderator_role))

class newTicketEmbedModal(ui.Modal):
    def __init__(self, embed_channel:TextChannel, category_channel:CategoryChannel, moderator_role):
        self.embed_channel = embed_channel
        self.category_channel = category_channel
        self.moderator_role = moderator_role
        components = [
            ui.TextInput(label="Embed title", custom_id="title", placeholder="Technical ticket", required=True, max_length=25, style=TextInputStyle.single_line),
            ui.TextInput(label="Description", custom_id="description", placeholder="When to create this ticket", required=True, max_length=2000, style=TextInputStyle.paragraph),
        ]
        super().__init__(title="Create New Ticket", components=components, timeout=600)
    
    async def callback(self, inter:ModalInteraction):
        embed = Embed()
        embed.color = Color.random()
        
        embed.title = inter.text_values["title"]
        embed.description = inter.text_values["description"]
        await self.embed_channel.send(embed=embed, view=createTicketView(category_channel=self.category_channel, moderator_role=self.moderator_role))
        await inter.response.send_message(embed=Embed(title="Created embed", color=Color.green()).set_footer(text="This command is temporary until a better solution is found"), ephemeral=True)

            

@plugin.slash_command(name="create-ticket-embed")
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(manage_channels=True, manage_permissions=True)
async def create_ticket_embed(inter:CommandInteraction, embed_channel:TextChannel, category_channel:CategoryChannel, moderator_role:Role):
    await inter.response.send_modal(newTicketEmbedModal(embed_channel, category_channel, moderator_role))


setup, teardown = plugin.create_extension_handlers()