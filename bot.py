import discord
from discord.ext import commands
import json
from github import Github

x = open("config.json", "r")
configuration = json.load(x)

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix=configuration['DiscordBotCommandPrefix'], case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.mro, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{configuration['DiscordBotCommandPrefix']}help"))
    print("Bot ready!")
bot.remove_command("help")


@bot.event
async def on_raw_reaction_add(payload):
    msgId = payload.message_id
    if msgId == 845978150823657473:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == '\u2705':

            role = discord.utils.get(guild.roles, name='no-perms')

            await payload.member.remove_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    msgId = payload.message_id
    if msgId == 845978150823657473:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == '\u2705':

            role = discord.utils.get(guild.roles, name='no-perms')

            await bot.get_guild(payload.guild_id).get_member(payload.user_id).add_roles(role)

# GITHUB MANAGEMENT


@bot.command()
@commands.has_role(configuration['GitHubManagerRole'])
async def gh(ctx, mode=None, user=None, permissions=None):

    await ctx.message.delete()

    if mode is None:
        embed = discord.Embed(title="GH Help", description="")
        embed.add_field(name='`add` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}gh add [username] [permissions (admin/member)]", inline=False)
        embed.add_field(name='`remove` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}gh remove [username]", inline=False)
        embedError = discord.Embed(
            title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
        await ctx.send(embed=embedError)
        await ctx.send(embed=embed)
    elif mode == 'add':
        if user is None or permissions is None:
            embed = discord.Embed(title="GH Help", description="")
            embed.add_field(
                name='`add` command', value=f"{configuration['DiscordBotCommandPrefix']}gh add [username] [permissions (admin/member)]", inline=False)
            embed.add_field(name='`remove` command',
                            value=f"{configuration['DiscordBotCommandPrefix']}gh remove [username]", inline=False)
            embedError = discord.Embed(
                title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
            await ctx.send(embed=embedError)
            await ctx.send(embed=embed)
        else:
            try:
                GithubInstance = Github(configuration['GitHubAccessToken'])
                nUser = GithubInstance.get_user(user)
                org = GithubInstance.get_organization(
                    configuration['RepositoryName'])
                if org.has_in_members(nUser):
                    embed = discord.Embed(
                        title='Warning!', description='User is already in the organization.', color=discord.Color.gold())
                    await ctx.send(embed=embed)
                else:
                    org.add_to_members(member=nUser, role=permissions)
                    embed = discord.Embed(
                        title='Success!', description='User invited to the organization successfully.', color=discord.Color.green())
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title='Error!', description='User not invited to the organization.', color=discord.Color.red())
                await ctx.send(embed=embed)
                print('ERROR: ' + e)
    elif mode == 'remove':
        if user is None or permissions is not None:
            embed = discord.Embed(title="GH Help", description="")
            embed.add_field(
                name='`add` command', value="configuration['DiscordBotCommandPrefix']gh add [username] [permissions (admin/member)]", inline=False)
            embed.add_field(name='`remove` command',
                            value="configuration['DiscordBotCommandPrefix']gh remove [username]", inline=False)
            embedError = discord.Embed(
                title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
            await ctx.send(embed=embedError)
            await ctx.send(embed=embed)
        else:
            try:
                GithubInstance = Github(configuration['GitHubAccessToken'])
                nUser = GithubInstance.get_user(user)
                org = GithubInstance.get_organization(
                    configuration['RepositoryName'])
                mExists = org.has_in_members(nUser)

                if mExists:
                    org.remove_from_members(member=nUser)
                    embed = discord.Embed(
                        title='Success!', description='User removed from the organization.', color=discord.Color.green())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title='Warning!', description='User is not in the organization.', color=discord.Color.gold())
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title='Error!', description='User not removed from the organization.', color=discord.Color.red())
                await ctx.send(embed=embed)
                print('ERROR: ' + e)
    else:
        embed = discord.Embed(title="GH Help", description="")
        embed.add_field(name='`add` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}gh add [username] [permissions (admin/member)]", inline=False)
        embed.add_field(name='`remove` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}gh remove [username]", inline=False)
        embedError = discord.Embed(
            title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
        await ctx.send(embed=embedError)
        await ctx.send(embed=embed)

# PURGE COMMAND


@bot.command()
@commands.has_role(844572494132150274)
async def purge(ctx, amount=5, fMessage='true'):

    deleted = await ctx.channel.purge(limit=amount)

    if fMessage == '-n':
        pass
    else:
        embed = discord.Embed(
            title='Success!', description=f'Cleared {len(deleted)} messages successfuly.', color=discord.Color.green())
        await ctx.send(embed=embed)

# HIRING ROOMS COMMANDS


@bot.command()
@commands.has_any_role(844572494132150274, 844944216974557236)
async def hiring(ctx, mode=None):

    if mode is None:
        embed = discord.Embed(title="Hiring Help", description="")
        embed.add_field(name='`create` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}hiring create", inline=False)
        embed.add_field(name='`remove` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}hiring archive", inline=False)
        embedError = discord.Embed(
            title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
        await ctx.send(embed=embedError)
        await ctx.send(embed=embed)
    elif mode == 'create':

        if ctx.channel.id == 846053818037829642:

            await ctx.message.delete()

            category = discord.utils.get(
                ctx.guild.categories, id=844572495717728296)
            archiveCategory = discord.utils.get(
                ctx.guild.categories, id=845903157715533845)
            if len(category.channels) == 1 or len(category.channels) == 0:
                if len(archiveCategory.channels) == 0:
                    ticket_num = 1
                else:
                    ticket_num = len(archiveCategory.channels) + 1
            else:
                ticket_num = len(category.channels) + len(archiveCategory.channels)
            await ctx.guild.create_text_channel(f"room-{ticket_num}", overwrites=None, category=category)
            embed = discord.Embed(
                title='Success!', description=f'Channel `room-{ticket_num}` created successfuly.', color=discord.Color.green())
            await ctx.send(embed=embed)
    elif mode == 'archive':

        await ctx.message.delete()

        category = discord.utils.get(
            ctx.guild.categories, id=844572495717728296)
        if ctx.channel.category == category and ctx.channel.id != 846053818037829642:
            category = discord.utils.get(
                ctx.guild.categories, id=845903157715533845)
            name = ctx.channel.name
            await ctx.channel.edit(name=f'{name}-arch', category=category)
            embed = discord.Embed(
                title='Success!', description='Channel archived successfuly.', color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Error!', description='Channel cannot be archived.', color=discord.Color.red())
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Hiring Help", description="")
        embed.add_field(name='`create` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}hiring create", inline=False)
        embed.add_field(name='`remove` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}hiring archive", inline=False)
        embedError = discord.Embed(
            title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
        await ctx.send(embed=embedError)
        await ctx.send(embed=embed)

# CHANGE NICKNAME


@bot.command()
@commands.has_role(844572494132150274)
async def nick(ctx, user: discord.Member = None, position=None, name=None):

    await ctx.message.delete()

    if user is None or position is None or name is None:
        embed = discord.Embed(title="NickName Help", description="")
        embed.add_field(name='`nick` command',
                        value=f"{configuration['DiscordBotCommandPrefix']}nick [member] [position] [first_name]", inline=False)
        embedError = discord.Embed(
            title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
        await ctx.send(embed=embedError)
        await ctx.send(embed=embed)
    else:
        try:
            nick = f"{position} | {name}"
            await user.edit(nick=nick)
            embed = discord.Embed(
                title='Success!', description=f'Member\'s nick changed successfuly.', color=discord.Color.green())
            await ctx.send(embed=embed)
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Error!', description=f'Bot has no permissions to change {user.mention}\'s nick.```discord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions```', color=discord.Color.red())
            await ctx.send(embed=embed)
            pass

# BAN COMMAND

@bot.command()
@commands.has_role(844572494132150274)
async def ban(ctx, user: discord.Member = None, reason=None):
    await ctx.message.delete()

    if user is None or user == ctx.message.author:
        embedError = discord.Embed(
            title='Bad usage', description='You cannot ban yourself.', color=discord.Color.red())
        await ctx.send(embed=embedError)
    else:
        try:
            if reason is not None:
                msg = f"You habe been banned from {ctx.guild.name} for `{reason}`."
            else:
                msg = f"You habe been banned from {ctx.guild.name}.""
            
            await user.send(message)
            await ctx.guild.ban(user, reason=reason)
            
            embed = discord.Embed(
                title='Success!', description=f'Member banned successfuly.', color=discord.Color.green())
            await ctx.send(embed=embed)
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Error!', description=f'Bot has no permissions to ban {user.mention}.```discord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions```', color=discord.Color.red())
            await ctx.send(embed=embed)
            pass


# HELP


@bot.command()
async def help(ctx, arg=None):
    if arg is not None:
        if arg.lower() == 'gh' or arg.lower() == 'github':
            embed = discord.Embed(title="GH Help", description="")
            embed.add_field(
                name='`add` command', value=f"{configuration['DiscordBotCommandPrefix']}gh add [username] [permissions (admin/member)]", inline=False)
            embed.add_field(name='`remove` command',
                            value=f"{configuration['DiscordBotCommandPrefix']}gh remove [username]", inline=False)
            await ctx.send(embed=embed)

        if arg.lower() == 'purge':
            embed = discord.Embed(title="Purge Help", description="")
            embed.add_field(
                name='`purge` command', value=f"{configuration['DiscordBotCommandPrefix']}purge [amount (default 5)] [final message (`-n` to not show)]", inline=False)
            await ctx.send(embed=embed)

        if arg.lower() == 'hiring' or arg.lower() == 'hire':
            embed = discord.Embed(title="Hiring Help", description="")
            embed.add_field(name='`create` command',
                            value=f"{configuration['DiscordBotCommandPrefix']}hiring create", inline=False)
            embed.add_field(name='`remove` command',
                            value=f"{configuration['DiscordBotCommandPrefix']}hiring archive", inline=False)
            await ctx.send(embed=embed)

        if arg.lower() == 'nick':
            embed = discord.Embed(title="Nickname Help", description="")
            embed.add_field(
                name='`nick` command', value=f"{configuration['DiscordBotCommandPrefix']}nick [member] [position] [first_name]", inline=False)
            await ctx.send(embed=embed)

        if arg.lower() == 'ban':
            embed = discord.Embed(title="Ban Command Help", description="")
            embed.add_field(
                name='`ban` command', value=f"{configuration['DiscordBotCommandPrefix']}ban [member] [reason]" inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Help", description="")
            embed.add_field(
                name='`gh` command', value=f"**{configuration['DiscordBotCommandPrefix']}gh** | Manage users in GitHub organisation.\n> Check **{configuration['DiscordBotCommandPrefix']}help gh** or **{configuration['DiscordBotCommandPrefix']}help github** for more info.", inline=False)
            embed.add_field(name='`hiring` command',
                            value=f"**{configuration['DiscordBotCommandPrefix']}hiring** | Create/Archive hiring rooms.\n> Check **{configuration['DiscordBotCommandPrefix']}help hiring** or **{configuration['DiscordBotCommandPrefix']}help hire** for more info.", inline=False)
            embed.add_field(
                name='`nick` command', value=f"**{configuration['DiscordBotCommandPrefix']}nick** | Change the nickname of a  member.\n> Check **{configuration['DiscordBotCommandPrefix']}help nick** for more info.", inline=False)
            embed.add_field(
                name='`purge` command', value=f"**{configuration['DiscordBotCommandPrefix']}purge** | Clear certain amount of messages in the current channel.\n> Check **{configuration['DiscordBotCommandPrefix']}help purge** for more info.", inline=False)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Help", description="")
        embed.add_field(
            name='`gh` command', value=f"**{configuration['DiscordBotCommandPrefix']}gh** | Manage users in GitHub organisation.\n> Check **{configuration['DiscordBotCommandPrefix']}help gh** or **{configuration['DiscordBotCommandPrefix']}help github** for more info.", inline=False)
        embed.add_field(name='`hiring` command',
                        value=f"**{configuration['DiscordBotCommandPrefix']}hiring** | Create/Archive hiring rooms.\n> Check **{configuration['DiscordBotCommandPrefix']}help hiring** or **{configuration['DiscordBotCommandPrefix']}help hire** for more info.", inline=False)
        embed.add_field(name='`nick` command',
                        value=f"**{configuration['DiscordBotCommandPrefix']}nick** | Change the nickname of a  member.\n> Check **{configuration['DiscordBotCommandPrefix']}help nick** for more info.", inline=False)
        embed.add_field(name='`ban` command',
                        value=f"**{configuration['DiscordBotCommandPrefix']}ban** | Bans a member from the server.\n> Check **{configuration['DiscordBotCommandPrefix']}help ban** for more info.", inline=False)
        embed.add_field(name='`purge` command',
                        value=f"**{configuration['DiscordBotCommandPrefix']}purge** | Clear certain amount of messages in the current channel.\n> Check **{configuration['DiscordBotCommandPrefix']}help purge** for more info.", inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def welcome_message(ctx):

    await ctx.message.delete()

    embed = discord.Embed(title='Rules', description='The Executives and Mods will Mute/Kick/Ban per discretion. If you feel mistreated DM an Executive and we will resolve the issue.\n\nAll channels will have pinned messages explaining what they are there for and how everything works. If you don\'t understand something, feel free to ask!\n\nYour presence in this server implies accepting the following rules, including all further changes. These changes might be done at any time without notice, it is your responsibility to check for them.\n\n> By clicking on the ✅ emoji you agree with all the following rules:')

    embed.add_field(name='1 - Be Respectful',
                    value='You must respect all users, regardless of your liking towards them. Treat others the way you want to be treated.', inline=False)
    embed.add_field(name='2 - No Inappropriate Language',
                    value='The use of profanity should be kept to a minimum. However, any derogatory language towards any user is prohibited.', inline=False)
    embed.add_field(name='3 - No Spamming',
                    value='Don\'t send a lot of small messages right after each other. Do not disrupt chat by spamming.', inline=False)
    embed.add_field(name='4 - No Pornographic/Adult/Other NSFW',
                    value='This is a community server and not meant to share this kind of material.', inline=False)
    embed.add_field(name='5 - No Advertisements', value='We do not tolerate any kind of advertisements, whether it be for other communities or streams. You can post your content in the media channel if it is relevant and provides actual value (Video/Art)', inline=False)
    embed.add_field(name='6 - No Offensive Names and Avatars',
                    value='You will be asked to change your name or picture if the staff deems them inappropriate.', inline=False)
    embed.add_field(name='7 - Server Raiding',
                    value='Raiding or mentions of raiding are not allowed.', inline=False)
    embed.add_field(name='8 - Direct & Indirect Threats',
                    value='Threats to other users of DDoS, Death, DoX, abuse, and other malicious threats are absolutely prohibited and disallowed.', inline=False)
    embed.add_field(name='9 - Follow the Discord Community Guidelines',
                    value='You can find them (here)[https://discord.com/guidelines].', inline=False)
    embed.add_field(name='10 - Don\'t Join Voice Chat Channels Without Permission',
                    value='If you see that they have a free spot it is alright to join and ask whether they have an open spot, but leave if your presence is not wanted by whoever was there first.', inline=False)

    embed.set_author(name='Adapt Development Team',
                     icon_url='https://cdn.discordapp.com/attachments/842756273392975872/842756454482313226/logo_round.png')

    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/842756273392975872/843383573054881812/logo.png')

    embed.set_footer(text='Licenced under the Creative Commons Licence',
                     icon_url='https://probot.media/O31eqftBYL.png')

    msg = await ctx.send(embed=embed)

    await msg.add_reaction(emoji='✅')


"""@bot.command()
async def chat(ctx):

    await ctx.message.delete()

    embed = discord.Embed(title='Create Hiring Rooms', description='Use the following commands to create/archive hiring chat rooms.')

    embed.add_field(name='__Create__ command', value=f'Use `{configuration["DiscordBotCommandPrefix"]}hiring create` to create a channel.', inline=False)
    embed.add_field(name='__Archive__ command', value=f'Use `{configuration["DiscordBotCommandPrefix"]}hiring archive` in a specific hiring channel to move that channel to the **📚 HIRE ARCHIVES 📚** category.', inline=False)

    embed.set_author(name='Adapt Development Team',
                     icon_url='https://cdn.discordapp.com/attachments/842756273392975872/842756454482313226/logo_round.png')

    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/842756273392975872/843383573054881812/logo.png')

    embed.set_footer(text='Licenced under the Creative Commons Licence',
                     icon_url='https://probot.media/O31eqftBYL.png')

    msg = await ctx.send(embed=embed)

    await discord.Message.pin(msg)

    await ctx.channel.purge(limit=1)"""


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='no-perms')
    await member.add_roles(role)

bot.run(configuration['DiscordBotToken'])
