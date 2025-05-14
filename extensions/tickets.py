TICKET_CATEGORY_ID = 1372062267415334963

from disnake_plugins import Plugin
from disnake.ext import commands
from disnake import ui, ButtonStyle, TextInputStyle, Color, Embed, CommandInteraction, ModalInteraction, MessageInteraction, utils, TextChannel, CategoryChannel
from asyncio import sleep

plugin = Plugin(name="tickets")

class closeTicketView(ui.View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=0)
    
    @ui.button(label="Close ticket", style=ButtonStyle.red)
    async def close_ticket(self, button:ui.Button, inter:MessageInteraction):
        await inter.response.send_message(f"Closing ticket in <t:{int(utils.utcnow().timestamp())+5}:R>")
        await sleep(5)
        await inter.channel.delete(reason=f"Ticket close | Closed by {inter.author.name}")



class createTicketModal(ui.Modal):
    def __init__(self):
        components = [
            ui.TextInput(label="Ticket name", custom_id="name", placeholder="Report hacker", required=True, max_length=20, style=TextInputStyle.single_line),
            ui.TextInput(label="Description", custom_id="description", placeholder="I caught 2known was hacking on camera!", required=True, max_length=2000, min_length=40, style=TextInputStyle.paragraph)
        ]
        super().__init__(title="Create ticket", components=components, timeout=500)
    
    async def callback(self, inter:ModalInteraction):
        embed = Embed(color=Color.red())
        embed.title = inter.text_values["name"]
        embed.description = inter.text_values["description"]
        embed.set_author(name=inter.author.name)

        category = inter.guild.get_channel(TICKET_CATEGORY_ID)
        user_ticket_count = len([ticket for ticket in category.channels if str(inter.author.id) in ticket.name])

        ticket = await inter.guild.create_text_channel(name=f"{inter.author.id}-{user_ticket_count}", reason="Ticket creation", category=category)
        await ticket.send(f"{inter.author.mention}\n-# Ticket opened <t:{int(utils.utcnow().timestamp())}:R>", embed=embed, view=closeTicketView())
        await inter.response.send_message(embed=Embed(title="Ticket created", color=Color.green()), ephemeral=True)

class createTicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=0)
    
    @ui.button(label="Create ticket", style=ButtonStyle.green)
    async def create_ticket(self, button: ui.Button, inter:MessageInteraction):
        await inter.response.send_modal(createTicketModal())

class newTicketEmbedModal(ui.Modal):
    def __init__(self, embed_channel:TextChannel, ticket_category:CategoryChannel):
        self.embed_channel = embed_channel
        self.ticket_category = ticket_category

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

        await self.embed_channel.send(embed=embed, view=createTicketView())
        await inter.response.send_message(embed=Embed(title="Created embed", color=Color.green()), ephemeral=True)

            

@plugin.slash_command(name="create-ticket-embed")
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(manage_channels=True, manage_permissions=True)
async def create_ticket_embed(inter:CommandInteraction, embed_channel:TextChannel, ticket_category:CategoryChannel):
    await inter.response.send_modal(newTicketEmbedModal(embed_channel, ticket_category))


setup, teardown = plugin.create_extension_handlers()