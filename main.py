# -- made by aydenn (.moonbot.) -- #

import discord
from discord import integrations
import os
import asyncio
from aiohttp import ClientSession, client
import concurrent.futures
from discord.ext import commands, tasks
from discord.ui import Button, View
from datetime import timezone
import datetime
import json

warnings_folder = "warnings"
user_warnings = {}

if not os.path.exists(warnings_folder):
    os.makedirs(warnings_folder)


# -- config -- #
bot_token = 'MTExMzA2MTk3NDIyMjMxOTcyNg.GhZOWa.5VX3B0AGSZyvTALYJBEen6ErDgHM0bpLATMe4k'
prefix = '-'

# -- source -- #

intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents, help_command=None) 

@client.event
async def on_ready():
  game = discord.Game("Moderation | V1") # change this to whatever
  await client.change_presence(activity=game, status=discord.Status.online) # more statuses: idle, invisible
  print(f'Logged in as {client.user.name}')
  print(f'===================================')
  print(f'do {prefix}help to see available commands!')
  print(f'===================================')
  invite_url = discord.utils.oauth_url(
      client.user.id, permissions=discord.Permissions(administrator=True))

  print(f'invite bot {invite_url}') 


# -- ban -- #
@client.command(name='ban', pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason="None"):
  member = ctx.guild.get_member(user.id)

  if member:
    try:
      await member.ban(reason=reason)

      embed = discord.Embed(
          title="User Banned",
          description=
          f"{member.mention} has been banned.\n**Reason:** {reason}",
          color=discord.Color.red()  
      )

      await ctx.reply(embed=embed)
    except discord.Forbidden:
      embed = discord.Embed(
          title="Cannot ban user",
          description=
          f"Cannot ban {member.mention} because their top role is above mine.",
          color=discord.Color.red()  
      )
      await ctx.reply(embed=embed)
  else:
    embed = discord.Embed(
        title="User Not Found",
        description="The specified user could not be found in this server.",
        color=discord.Color.red()  
    )
    await ctx.reply(embed=embed)

@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    embed = discord.Embed(
        title="Insufficient Permissions",
        description=
        "You don't have the required permissions to use this command.",
        color=discord.Color.red()  
    )
    await ctx.reply(embed=embed)



#-- unban -- #
@client.command(name='unban', pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id, *, reason="None"):
  try:
    user_id = int(user_id)
    banned_user = await ctx.guild.fetch_ban(discord.Object(id=user_id))
    await ctx.guild.unban(banned_user.user, reason=reason)

    embed = discord.Embed(
        title="User Unbanned",
        description=
        f"{banned_user.user.mention} has been unbanned.\n**Reason:** {reason}",
        color=discord.Color.green()  
    )

    await ctx.reply(embed=embed)
  except discord.NotFound:
    embed = discord.Embed(
        title="User Not Found",
        description=
        f"The specified user with ID {user_id} is not currently banned.",
        color=discord.Color.red()  
    )
    await ctx.reply(embed=embed)


@unban.error
async def unban_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    embed = discord.Embed(
        title="Insufficient Permissions",
        description=
        "You don't have the required permissions to use this command.",
        color=discord.Color.red() 
    )
    await ctx.reply(embed=embed)

# -- kick -- #
@client.command(name='kick', pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason="None"):
  member = ctx.guild.get_member(user.id)

  if member:
    try:
      await member.kick(reason=reason)

      embed = discord.Embed(
          title="User Kicked",
          description=
          f"{member.mention} has been kicked.\n**Reason:** {reason}",
          color=discord.Color.orange() 
      )

      await ctx.reply(embed=embed)
    except discord.Forbidden:
      embed = discord.Embed(
          title="Cannot kick user",
          description=
          f"Cannot kick {member.mention} because their top role is above mine.",
          color=discord.Color.red()  
      )
      await ctx.reply(embed=embed)
  else:
    embed = discord.Embed(
        title="User Not Found",
        description="The specified user could not be found in this server.",
        color=discord.Color.red()  
    )
    await ctx.reply(embed=embed)


@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    embed = discord.Embed(
        title="Insufficient Permissions",
        description=
        "You don't have the required permissions to use this command.",
        color=discord.Color.red() 
    )
    await ctx.reply(embed=embed)


# -- role remove -- #
@client.command(name='role_remove')
async def remove_role(ctx, member: discord.Member = None, role: discord.Role = None):
  if ctx.guild is None:
    await ctx.reply('Please do this in a server.')
    return

  if ctx.author.guild_permissions.manage_roles:
    bot_top_role = ctx.guild.me.top_role

    if member is None or role is None:
      await ctx.reply('Please @ a user and a role.')
      return

    if bot_top_role > role:
      if role in member.roles:
        await member.remove_roles(role)
        await ctx.reply(f'{member.mention} has been removed from the **{role.name}** role.')
      else:
        await ctx.reply(f'{member.mention} does not have the **{role.name}** role.')
    else:
      await ctx.reply('Cannot remove a role higher than or equal to my top role.')
  else:
    await ctx.reply('You do not have the "manage_roles" permission to use this command.')

# -- role add -- #
@client.command(name='roleadd')
async def give_role(ctx, member: discord.Member = None, role: discord.Role = None):
    if ctx.guild is None:
        await ctx.send('Please do this in a server.')
        return

    if ctx.author.guild_permissions.manage_roles:
        bot_top_role = ctx.guild.me.top_role

        if member is None or role is None:
            await ctx.send('Please select a user and/or a role.')
            return

        if bot_top_role > role:
            if role in member.roles:
                await ctx.send(f'{member.mention} already has the **{role.name}** role.')
            else:
                await member.add_roles(role)
                await ctx.send(f'{member.mention} has been given the **{role.name}** role.')
        else:
            await ctx.send('Cannot give a role higher than or equal to my top role.')
    else:
        await ctx.send('You do not have the "Manage Roles" permission to use this command.')



# -- warn -- #
def load_user_warnings(user_id):
    file_path = os.path.join(warnings_folder, f"{user_id}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def save_user_warnings(user_id, warnings):
    file_path = os.path.join(warnings_folder, f"{user_id}.json")
    with open(file_path, 'w') as file:
        json.dump(warnings, file)

@client.command(name='warn')
async def warn(ctx, user: discord.Member, *, reason: str):
    if ctx.author.guild_permissions.ban_members:
        if user.id not in user_warnings:
            user_warnings[user.id] = load_user_warnings(user.id)

        user_warnings[user.id].append(reason)
        save_user_warnings(user.id, user_warnings[user.id])

        embed = discord.Embed(
            title="User Warned",
            description=f"{user.mention} has been warned for: `{reason}`",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Insufficient Permissions",
            description="You don't have the required permissions to use this command.",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)


@client.command(name='warn_remove')
async def remove_warning(ctx, user: discord.Member, index: str):
    if ctx.author.guild_permissions.ban_members:
        try:
            index = int(index)
        except ValueError:
            embed = discord.Embed(
                title="Invalid Index",
                description=f"Please provide a valid integer index to remove a warning. ({prefix}warn_remove @UserName (number of warning) ({prefix}warn_remove @UserName 2)",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        warnings = load_user_warnings(user.id)

        if 0 <= index - 1 < len(warnings):
            removed_warning = warnings.pop(index - 1)
            save_user_warnings(user.id, warnings)

            embed = discord.Embed(
                title="Warning Removed",
                description=f"Removed warning `{removed_warning}` for {user.mention}.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Invalid Index",
                description=f"Invalid warning index. Use `{prefix}warnings {user.mention}` to view warnings.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title="Insufficient Permissions",
            description="You don't have the required permissions to use this command.",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)

@client.command(name='warnings')
async def view_warnings(ctx, user: discord.Member):
    if ctx.author.guild_permissions.ban_members:
        warnings = load_user_warnings(user.id)
        if warnings:
            formatted_warnings = "\n".join([f"{i + 1}. {reason}" for i, reason in enumerate(warnings)])
            embed = discord.Embed(
                title=f"Warnings for {user.name}",
                description=formatted_warnings,
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="No Warnings",
                description=f"{user.mention} has no warnings.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Insufficient Permissions",
            description="You don't have the required permissions to use this command.",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)


# -- purge --
@client.command(name='purge')
async def purge_messages(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        deleted = await ctx.channel.purge(limit=amount + 1) 

        embed = discord.Embed(
            title="Purge Successful",
            description=f"Purged {len(deleted) - 1} messages.",
            color=discord.Color.green()
        )
        purge_message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await purge_message.delete()
    else:
        embed = discord.Embed(
            title="Insufficient Permissions",
            description="You don't have the required permissions to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

       
# -- server info -- #
@client.command(name='serverinfo')
async def serverinfo(ctx):
    server_name = ctx.guild.name
    owner_name = ctx.guild.owner.name
    creation_time = ctx.guild.created_at.strftime("%Y-%m-%d")
    boosts = ctx.guild.premium_subscription_count
    member_count = ctx.guild.member_count
    bot_count = sum(member.bot for member in ctx.guild.members)
    channel_count = len(ctx.guild.channels)

    embed = discord.Embed(
        title=f"{server_name} Info",
        color=0xDAA520  
    )

    embed.add_field(name="Owner", value=f"```{owner_name}```", inline=True)
    embed.add_field(name="Server Created at", value=f"```{creation_time}```", inline=True)
    embed.add_field(name="Boosts", value=f"```{boosts}```", inline=True)
    embed.add_field(name="Members", value=f"```{member_count}```", inline=True)
    embed.add_field(name="Bots", value=f"```{bot_count}```", inline=True)
    embed.add_field(name="Channels", value=f"```{channel_count}```", inline=True)

    await ctx.send(embed=embed)



# -- user info -- #
@client.command(name='userinfo')
async def userinfo(ctx, user: discord.User):
    member = ctx.guild.get_member(user.id)

    if member:
        username = member.name
        creation_time = member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        roles = [role.name for role in member.roles]
        join_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC")

        embed = discord.Embed(
            title=f"{username} Info",
            color=0xDAA520
        )

        embed.add_field(name="Username", value=f"```{username}```", inline=True)
        embed.add_field(name="Account created at", value=f"```{creation_time}```", inline=True)
        embed.add_field(name="Roles", value=f"```{', '.join(roles)}```", inline=True)
        embed.add_field(name="Join Date", value=f"```{join_date}```", inline=True)

        await ctx.send(embed=embed)
    else:
        await ctx.send("This user is not a member of the server.")



# -- join message -- #
@client.event
async def on_guild_join(guild):
    integrations = await guild.integrations()
    for integration in integrations:
        if isinstance(integration, discord.BotIntegration):
            if integration.application.user.name == client.user.name:
                bot_inviter = integration.user

                embed = discord.Embed(
                    title="Thank You",
                    description=f"Thank You for choosing `{client.user.name}` to moderate your server. Hope you love the bot!!",
                    color=0xFF0000  
                )
                embed.set_footer(text="Made by virtual")

                await bot_inviter.send(content=None, embed=embed) 

# -- help cmd -- #
class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [ 
            discord.SelectOption(label='Moderation', value='Moderation', emoji='<:mod:1202366370440806400>'), # change the emojis the bot doesnt need to be in the server!
            discord.SelectOption(label='Utility', value='Utility', emoji='<:member:1202366373351919646>'), 
        ]
        super().__init__(placeholder='Select', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]

        if selected_option == 'Moderation':
            embed_data = {
                "title": "Moderation Commands",
                "description": (
                    f"`💜` `{prefix}ban @user (reason`   - bans that user\n`💜` `{prefix}kick @user (reason)` - kicks that user\n`💜` `{prefix}warn @user (reason)` - warns that user\n`💜` `{prefix}warnings @user ` - shows user warnings\n`💜` `{prefix}warn_remove (warn number)` - removes warning\n`💜` `{prefix}role_add @user (role)` -  gives role from that user\n`💜` `{prefix}role_remove @user (role)` - removes role from that user\n`💜` `{prefix}purge (amount)` - purge messages in a channnel"
                ),
                "color": discord.Color.green().value
            }
        elif selected_option == 'Utility':
            embed_data = {
                "title": "Utility Commands",
                "description": (
                    f"`🤍` `{prefix}userinfo @user`   - shows user info\n`🤍` `{prefix}serverinfo` - shows server info"
                ),
                "color": discord.Color.gold().value
            }
        else:
            return

        embed = discord.Embed(**embed_data)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())



@client.command()
async def help(ctx):
    view = Dropdown()

    help_embed = discord.Embed(
        title=f"Help Menu",
        description=f"""hello {ctx.author.mention} Select an option to get started with me!!!""", # change or keep this text up to u
        color=15856113
    )
    help_embed.set_footer(text='https://github.com/discordmo0n/moderation-bot')

    await ctx.send(embed=help_embed, view=DropdownView())

# command error
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    embed = discord.Embed(
        title="-- Error --",
        description=f"```This command doesn't exist, do {prefix}help to see available commands```",
        color=0xFF0000
    )
    await ctx.reply(embed=embed)


client.run(bot_token)
