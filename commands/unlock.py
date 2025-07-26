import discord
from discord.ext import commands
from discord import app_commands
import json

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def unlock_channel(self, ctx_or_interaction, channel, author):
        everyone = channel.guild.default_role

        try:
            await channel.set_permissions(everyone, send_messages=True)

            embed = discord.Embed(
                description=f"✅ {channel.mention} has been unlocked.",
                color=discord.Color.green()
            )



            if isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)


        except Exception as e:
            error_embed = discord.Embed(
                description=f"❌ Failed to unlock the channel:\n``{e}``",
                color=discord.Color.red()
            )
            if isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(embed=error_embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=error_embed)

    @app_commands.command(name="unlock", description="Unlock the current channel")
    @commands.has_permissions(manage_messages=True)
    async def unlock_slash(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.manage_messages:
            await self.unlock_channel(interaction, interaction.channel, interaction.user)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        


async def setup(bot):
    await bot.add_cog(Unlock(bot))
