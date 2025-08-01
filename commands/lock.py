import discord
from discord.ext import commands
from discord import app_commands
import json

class LockCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def lock_channel(self, target, channel, author):
        everyone = channel.guild.default_role

        try:
            await channel.set_permissions(everyone, send_messages=False)

            success_embed = discord.Embed(
                description=f"✅ {channel.mention} has been locked.",
                color=discord.Color.green()
            )

            if isinstance(target, discord.Interaction):
                await target.response.send_message(embed=success_embed)
            else:
                await target.send(embed=success_embed)


        except Exception as e:
            error_embed = discord.Embed(
                description=f"❌ Failed to lock the channel:\n``{e}``",
                color=discord.Color.red()
            )
            if isinstance(target, discord.Interaction):
                await target.response.send_message(embed=error_embed, ephemeral=True)
            else:
                await target.send(embed=error_embed)

    @app_commands.command(name="lock", description="Lock the current channel")
    @commands.has_permissions(manage_messages=True)
    async def lock_slash(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.manage_messages:
            await self.lock_channel(interaction, interaction.channel, interaction.user)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LockCommand(bot))
