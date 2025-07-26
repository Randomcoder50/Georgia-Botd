import discord
from discord.ext import commands
from discord import app_commands
import json

class sendMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(msg="Message to send.")
    async def lock_slash(self, interaction: discord.Interaction, msg: str):
        if interaction.user.guild_permissions.manage_messages:
            await interaction.channel.send(msg)
            await interaction.response.send_message("✅ Message sent!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(sendMsg(bot))

