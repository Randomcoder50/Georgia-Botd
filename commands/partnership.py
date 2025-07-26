import discord
from discord.ext import commands
from discord import app_commands

PARTNERSHIP_CHANNEL_ID = 1369100651946184847  # <<-- SET THIS POLICE TO THE PARTNERSHIP CHANNEL ID


class AdDropdown(discord.ui.View):
    def __init__(self, ad_text: str):
        super().__init__(timeout=None)
        self.ad_text = ad_text

        options = [
            discord.SelectOption(label="View Ad", description="Click to view the advertisement")
        ]

        self.add_item(AdSelect(ad_text, options))


class AdSelect(discord.ui.Select):
    def __init__(self, ad_text: str, options):
        super().__init__(placeholder="Choose an option", min_values=1, max_values=1, options=options)
        self.ad_text = ad_text

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"📢 **Ad Content:**\n{self.ad_text}",
            ephemeral=True
        )


class PartnershipModal(discord.ui.Modal, title="Submit Partnership"):
    def __init__(self, rep: discord.Member):
        super().__init__()
        self.rep = rep

        self.add_item(discord.ui.TextInput(
            label="Server Invite Link",
            placeholder="https://discord.gg/example",
            max_length=100
        ))

        self.add_item(discord.ui.TextInput(
            label="Advertisement Message",
            style=discord.TextStyle.paragraph,
            max_length=1000
        ))

    async def on_submit(self, interaction: discord.Interaction):
        invite_link = self.children[0].value
        advertisement = self.children[1].value

        channel = interaction.client.get_channel(PARTNERSHIP_CHANNEL_ID)
        if not channel:
            await interaction.response.send_message("❌ Partnership channel not found.", ephemeral=True)
            return

        message_content = f"REP: {self.rep.mention}\nServer Link: {invite_link}"
        view = AdDropdown(advertisement)
        await channel.send(content=message_content, view=view)

        await interaction.response.send_message("✅ Partnership submitted successfully!", ephemeral=True)


class Partnership(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="partnership_add", description="Submit a partnership ad.")
    @commands.has_permissions(Administrator=True)
    @app_commands.describe(rep="Mention the representative you're partnering with")
    async def partnership_add(self, interaction: discord.Interaction, rep: discord.Member):
        await interaction.response.send_modal(PartnershipModal(rep))


async def setup(bot):
    await bot.add_cog(Partnership(bot))
