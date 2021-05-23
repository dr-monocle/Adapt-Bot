import discord
from discord.ext import commands
import json
from github import Github

x = open("config.json", "r")
configuration = json.load(x)

intents = discord.Intents(messages=True, guilds=True, members=True)

bot = commands.Bot(
    command_prefix=configuration['DiscordBotCommandPrefix'], case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ad.help"))
    print("Bot ready!")
bot.remove_command("help")


@bot.command()
@commands.has_role(configuration['GitHubManagerRole'])
async def gh(ctx, mode=None, user=None, permissions=None):
    if mode is None:
        embed = discord.Embed(title="GH Help", description="")
        embed.add_field(name='`add` command', value="ad.gh add [username] [permissions (admin/member)]", inline=False)
        embed.add_field(name='`remove` command', value="ad.gh remove [username]", inline=False)
        embedError = discord.Embed(title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
        await ctx.send(embed=embedError)
        await ctx.send(embed=embed)
    elif mode == 'add':
        if user is None or permissions is None:
            embed = discord.Embed(title="GH Help", description="")
            embed.add_field(name='`add` command', value="ad.gh add [username] [permissions (admin/member)]", inline=False)
            embed.add_field(name='`remove` command', value="ad.gh remove [username]", inline=False)
            embedError = discord.Embed(title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
            await ctx.send(embed=embedError)
            await ctx.send(embed=embed)
        else:
            try:
                GithubInstance = Github(configuration['GitHubAccessToken'])
                nUser = GithubInstance.get_user(user)
                org = GithubInstance.get_organization(configuration['RepositoryName'])
                if org.has_in_members(nUser):
                    embed = discord.Embed(title='Warning!', description='User is already in the organization.', color=discord.Color.gold())
                    await ctx.send(embed=embed)
                else:
                    org.add_to_members(member=nUser, role=permissions)
                    embed = discord.Embed(title='Success!', description='User invited to the organization successfully.', color=discord.Color.green())
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title='Error!', description='User not invited to the organization.', color=discord.Color.red())
                await ctx.send(embed=embed)
                print('ERROR: ' + e)
    elif mode == 'remove':
        if user is None or permissions is not None:
            embed = discord.Embed(title="GH Help", description="")
            embed.add_field(name='`add` command', value="ad.gh add [username] [permissions (admin/member)]", inline=False)
            embed.add_field(name='`remove` command', value="ad.gh remove [username]", inline=False)
            embedError = discord.Embed(title='Bad usage', description='Parameters missing.\nPlease check bellow the correct usage of this command.', color=discord.Color.red())
            await ctx.send(embed=embedError)
            await ctx.send(embed=embed)
        else:
            try:
                GithubInstance = Github(configuration['GitHubAccessToken'])
                nUser = GithubInstance.get_user(user)
                org = GithubInstance.get_organization(configuration['RepositoryName'])
                mExists = org.has_in_members(nUser)

                if mExists:
                    org.remove_from_members(member=nUser)
                    embed = discord.Embed(title='Success!', description='User removed from the organization.', color=discord.Color.green())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='Warning!', description='User is not in the organization.', color=discord.Color.gold())
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title='Error!', description='User not removed from the organization.', color=discord.Color.red())
                await ctx.send(embed=embed)
                print('ERROR: ' + e)

@bot.command()
@commands.has_role(844572494132150274)
async def purge(ctx, amount = 5, fMessage = 'true'):

    deleted = await ctx.channel.purge(limit = amount)

    if fMessage == '-n':
        pass
    else:
        await ctx.send(f'Done! {len(deleted)} messages cleared!')


@bot.command()
async def help(ctx, arg=None):
    if arg is not None:
        if arg.lower() == 'gh' or arg.lower() == 'github':
            embed = discord.Embed(title="GH Help", description="")
            embed.add_field(name='`add` command', value="ad.gh add [username] [permissions (admin/member)]", inline=False)
            embed.add_field(name='`remove` command', value="ad.gh remove [username]", inline=False)
            await ctx.send(embed=embed)

        if arg.lower() == 'purge':
            embed = discord.Embed(title="Purge Help", description="")
            embed.add_field(name='`purge` command', value="ad.purge [amount (default 5)] [final message (`-n` to not show)]", inline=False)
            await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(title="Help", description="")
            embed.add_field(name='`gh` command', value="**ad.gh** | Manage users in GitHub organisation.\n> Check **ad.help gh** or **ad.help github** for more info.", inline=False)
            embed.add_field(name='`purge` command', value="**ad.purge** | Clear certain amount of messages in the current channel.\n> Check **ad.help purge** for more info.", inline=False)
            await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(title="Help", description="")
        embed.add_field(name='`gh` command', value="**ad.gh** | Manage users in GitHub organisation.\n> Check **ad.help gh** or **ad.help github** for more info.", inline=False)
        embed.add_field(name='`purge` command', value="**ad.purge** | Clear certain amount of messages in the current channel.\n> Check **ad.help purge** for more info.", inline=False)
        await ctx.send(embed=embed)

bot.run(configuration['DiscordBotToken'])
