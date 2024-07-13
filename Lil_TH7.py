import discord
from discord.ext import commands
import asyncio
import random

intents=discord.Intents.all()
intents.dm_messages=True
bot=commands.Bot(command_prefix='th.', intents=intents)
discord_ID=657902105012600862
#762726610872827955

@bot.event
async def on_ready():
    print(f'Yo Yo Mr. Snow! I am your loyal bot {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself
    if isinstance(message.channel, discord.DMChannel) and message.author.id != discord_ID:
        # Forward the message to a specific user (replace USER_ID with the actual user ID)
        user = bot.get_user(discord_ID)
        if user:
            forward_message = f"**From {message.author} ({message.author.id}):** {message.content}"
            await user.send(forward_message)
    # Process other commands as usual
    await bot.process_commands(message)

@bot.command(name='pdm', hidden=True)
async def send_pdm(ctx, member_id: int, *, message: str):
    # Check if the command is used in a DM
    if ctx.guild is None:
        if ctx.author.id==discord_ID:
            # 'user' is now a Member object, which contains the user ID
            member=bot.get_user(member_id)
            if member:
                await member.send(f'**From {ctx.author.display_name}: **{message}')
                await ctx.send(f'**Message sent to** {member.name} **successfully!**')
            else:
                await ctx.send(f'**User {member} not found**')
        else:
            await ctx.send('**Only my creator, Mr. Snow, can use this command.**')
    else:
        await ctx.send('**This command can only be used in DMs.**')

@bot.command(name='dm')
async def send_dm(ctx, user: discord.Member, *, message: str):
    helper=discord.utils.get(ctx.guild.roles, name='Helper')
    staff=discord.utils.get(ctx.guild.roles, name='Staff')
    mod=discord.utils.get(ctx.guild.roles, name='Mod')
    admin=discord.utils.get(ctx.guild.roles, name='Admin')
    # Check if the user has the 'Administrator' permission or has the one of the 'Helper, Staff, Mod, Admin' roles
    if any(role in ctx.author.roles for role in(helper, staff, mod, admin)) or ctx.author.guild_permissions.administrator:
        # 'user' is now a Member object, which contains the user ID
        if user:
            await user.send(message)
            await ctx.send(f'**Message sent to** {user.name}')
        else:
            await ctx.send('**User not found**')
    else:
        await ctx.send('**You do not have the necessary permissions to use this command.**')

@bot.command(name='msg')
async def message(ctx, channel_id:int, *, message:str):
    helper=discord.utils.get(ctx.guild.roles, name='Helper')
    staff=discord.utils.get(ctx.guild.roles, name='Staff')
    mod=discord.utils.get(ctx.guild.roles, name='Mod')
    admin=discord.utils.get(ctx.guild.roles, name='Admin')
    if any(role in ctx.author.roles for role in(helper, staff, mod, admin)) or ctx.author.guild_permissions.administrator:
        channel=bot.get_channel(channel_id)
        if channel:
            await channel.send(f"{message}")
            await ctx.send(f"**Your message was sent to {channel.name} successfully!**")
        else:
            await ctx.send("**Channel not found.")
    else:
        await ctx.send("**You do not have the necessary permissions to use this command.**")


@bot.command(name='pmsg', hidden=True)
async def send_pdm(ctx, channel_id: int, *, message: str):
    # Check if the command is used in a DM
    if ctx.guild is None:
        if ctx.author.id==discord_ID:
            # 'user' is now a Member object, which contains the user ID
            channel=bot.get_channel(channel_id)
            if channel:
                await channel.send(message)
                await ctx.send(f'**Message sent to** {channel.name} **successfully!**')
            else:
                await ctx.send(f'**User {channel} not found**')
        else:
            await ctx.send('**Only my creator, Mr. Snow, can use this command.**')
    else:
        await ctx.send('**This command can only be used in DMs.**')


@bot.command(name='ban')
async def ban_member(ctx, user: discord.Member, *, reason: str='No reason provided'):
    mod=discord.utils.get(ctx.guild.roles, name='Mod')
    admin=discord.utils.get(ctx.guild.roles, name='Admin')
    if any(role in ctx.author.roles for role in(mod, admin)) or ctx.author.guild_permissions.administrator:
        if user.guild_permissions.administrator:
            await ctx.send('**You cannot ban this user.**')
        await user.ban(reason=reason)
        await ctx.send(f'**{user.name} have been banned. Reason:{reason}**')
    else:
        await ctx.send('**You do not have the necessary permissions to use this command.**')

@bot.command(name='kick')
async def kick_member(ctx, user: discord.Member, *, reason: str='No reason provided'):
    staff=discord.utils.get(ctx.guild.roles, name='Staff')
    mod=discord.utils.get(ctx.guild.roles, name='Mod')
    admin=discord.utils.get(ctx.guild.roles, name='Admin')
    if any(role in ctx.author.roles for role in(staff, mod, admin)) or ctx.author.guild_permissions.administrator:
        if user.guild_permissions.administrator:
            await ctx.send('**You cannot kick this user.**')
        await user.kick(reason=reason)
        await ctx.send(f'**{user.name} have been kicked. Reason:{reason}**')
    else:
        await ctx.send('**You do not have the necessary permissions to use this command.**')

@bot.command(name='mute')
async def timeout_member(ctx, user: discord.Member, duration: int=1, *, reason: str='No reason provided'):
    helper = discord.utils.get(ctx.guild.roles, name='Helper')
    staff = discord.utils.get(ctx.guild.roles, name='Staff')
    mod = discord.utils.get(ctx.guild.roles, name='Mod')
    admin = discord.utils.get(ctx.guild.roles, name='Admin')
    muted = discord.utils.get(ctx.guild.roles, name='Muted')
    
    if any(role in ctx.author.roles for role in (helper, staff, mod, admin)) or ctx.author.guild_permissions.administrator:
        if user.guild_permissions.administrator:
            await ctx.send('**You cannot mute this user.**')
        mute_time = duration * 60   # Convert duration to minutes
        await user.add_roles(muted, reason=reason)
        await ctx.send(f'**{user.name} has been put in muted for {duration} minutes. Reason: {reason}**')
        
        await asyncio.sleep(mute_time)
        
        if muted in user.roles:
            await user.remove_roles(muted)
            await ctx.send(f'**{user.name} has been released from timeout.**')
    else:
        await ctx.send('**You do not have the necessary permissions to use this command.**')

@bot.command(name='about')
async def about_bot(ctx):
    if ctx:
        embed=discord.Embed(
            title=f"Hello there, **{ctx.author.display_name}**!",
            description=("I was created by Mr. Snow. Yep, he is my master and the owner of this server. "
                         "My name is Lil TH7 and I can only serve this server for now."
                         "I'm just a teeny tiny bot made out of fun and as a way for my"
                         "master to practice his coding skills. Visit the link below to know more.\n"
                         "https://trados77.github.io/LilTH7BotTOS/TOS.html"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text='Last updated: May 6, 2024')
        await ctx.send(embed=embed)


@bot.command(name='kiss')
async def kiss_member(ctx, user: discord.Member):
    kiss=['https://cdn.weeb.sh/images/H1e7nadP-.gif',
          'https://trados77.github.io/gifs/kiss2.gif',
          'https://trados77.github.io/gifs/kiss3.gif',
          'https://trados77.github.io/gifs/kiss4.gif',
          'https://trados77.github.io/gifs/kiss5.gif',
          'https://trados77.github.io/gifs/kiss6.gif'
          ]
    get_kiss=random.choice(kiss)
    if user:
        embed=discord.Embed(
            title=f'**{ctx.author.display_name}** gave **{user.display_name}** a kiss! Lovely',
            color=discord.Color.blurple()
            )
        embed.set_image(url=get_kiss)
        await ctx.send(embed=embed)

@bot.command(name='wkiss')
async def wkiss_member(ctx, user: discord.Member):
    wkiss=['https://cdn.weeb.sh/images/H1e7nadP-.gif',
          'https://trados77.github.io/gifs/wkiss2.gif',
          'https://trados77.github.io/gifs/wkiss3.gif',
          'https://trados77.github.io/gifs/wkiss4.gif',
          'https://trados77.github.io/gifs/wkiss5.gif',
          'https://trados77.github.io/gifs/wkiss6.gif',
          'https://trados77.github.io/gifs/wkiss7.gif',
          'https://trados77.github.io/gifs/wkiss8.gif',
          'https://trados77.github.io/gifs/wkiss9.gif',
          'https://trados77.github.io/gifs/wkiss10.gif',
          'https://trados77.github.io/gifs/wkiss11.gif'
          ]
    get_wkiss=random.choice(wkiss)
    if user:
        embed=discord.Embed(
            title=f'**{ctx.author.display_name}** gave **{user.display_name}** a wilde kiss👀 how brave',
            color=discord.Color.blurple()
            )
        embed.set_image(url=get_wkiss)
        await ctx.send(embed=embed)

@bot.command(name='hug')
async def hug_member(ctx, user: discord.Member):
    hug=['https://trados77.github.io/gifs/hug1.gif',
         'https://trados77.github.io/gifs/hug2.gif',
         'https://trados77.github.io/gifs/hug3.gif',
         'https://trados77.github.io/gifs/hug4.gif',
         'https://trados77.github.io/gifs/hug5.gif',
         'https://trados77.github.io/gifs/hug6.gif',
         'https://trados77.github.io/gifs/hug7.gif',
         'https://trados77.github.io/gifs/hug8.gif',
         'https://trados77.github.io/gifs/hug9.gif',
         'https://trados77.github.io/gifs/hug10.gif',
         'https://trados77.github.io/gifs/hug11.gif',
         'https://trados77.github.io/gifs/hug12.gif',
         'https://trados77.github.io/gifs/hug13.gif',
         'https://trados77.github.io/gifs/hug14.gif',
         'https://trados77.github.io/gifs/hug15.gif',
         'https://trados77.github.io/gifs/hug16.gif',
         'https://trados77.github.io/gifs/hug17.gif',
         'https://trados77.github.io/gifs/hug18.gif',
         'https://trados77.github.io/gifs/hug19.gif',
         'https://trados77.github.io/gifs/hug20.gif',
         'https://trados77.github.io/gifs/hug21.gif',
         'https://trados77.github.io/gifs/hug22.gif',
         'https://trados77.github.io/gifs/hug23.gif',
         'https://trados77.github.io/gifs/hug24.gif',
         'https://trados77.github.io/gifs/hug25.gif',
         'https://trados77.github.io/gifs/hug26.gif',
         'https://trados77.github.io/gifs/hug27.gif',
         'https://trados77.github.io/gifs/hug28.gif',
         'https://trados77.github.io/gifs/hug29.gif',
         'https://trados77.github.io/gifs/hug30.gif',
         'https://trados77.github.io/gifs/hug31.gif'
         ]
    get_hug=random.choice(hug)
    if user:
        embed=discord.Embed(
            title=f"**{ctx.author.display_name}** hugs **{user.display_name}**! Lovely💖",
            color=discord.Color.blurple()
        )
        embed.set_image(url=get_hug)
        await ctx.send(embed=embed)

@bot.command(name='pat')
async def pat_member(ctx, user: discord.Member):
    pat=['https://trados77.github.io/gifs/pat1.gif',
         'https://trados77.github.io/gifs/pat2.gif',
         'https://trados77.github.io/gifs/pat3.gif',
         'https://trados77.github.io/gifs/pat4.gif',
         'https://trados77.github.io/gifs/pat5.gif',
         'https://trados77.github.io/gifs/pat6.gif',
         'https://trados77.github.io/gifs/pat7.gif',
         'https://trados77.github.io/gifs/pat8.gif'
         ]
    get_pat=random.choice(pat)
    if user:
        embed=discord.Embed(
            title=f'**{ctx.author.display_name}** pats **{user.display_name}**. *pat pat*',
            color=discord.Color.blurple()
            )
        embed.set_image(url=get_pat)
        await ctx.send(embed=embed)

@bot.command(name='bonk')
async def bonk_member(ctx, user: discord.Member):
    bonk=['https://trados77.github.io/gifs/bonk1.gif',
         'https://trados77.github.io/gifs/bonk2.gif',
         'https://trados77.github.io/gifs/bonk3.gif',
         'https://trados77.github.io/gifs/bonk4.gif',
         'https://trados77.github.io/gifs/bonk5.gif',
         'https://trados77.github.io/gifs/bonk6.gif',
         'https://trados77.github.io/gifs/bonk7.gif',
         'https://trados77.github.io/gifs/bonk8.gif',
         'https://trados77.github.io/gifs/bonk9.gif',
         'https://trados77.github.io/gifs/bonk10.gif',
         'https://trados77.github.io/gifs/bonk11.gif',
         'https://trados77.github.io/gifs/bonk12.gif',
         'https://trados77.github.io/gifs/bonk13.gif',
         'https://trados77.github.io/gifs/bonk14.gif',
         ]
    get_bonk=random.choice(bonk)
    if user:
        embed=discord.Embed(
            title=f"**{ctx.author.display_name}** bonks **{user.display_name}**, that must've hurt",
            color=discord.Color.blurple()
            )
        embed.set_image(url=get_bonk)
        await ctx.send(embed=embed)

@bot.command(name='boop')
async def boop_member(ctx, user: discord.Member):
    boop=['https://trados77.github.io/gifs/boop1.gif',
          'https://trados77.github.io/gifs/boop2.gif',
          'https://trados77.github.io/gifs/boop3.gif',
          'https://trados77.github.io/gifs/boop4.gif',
          'https://trados77.github.io/gifs/boop5.gif',
          'https://trados77.github.io/gifs/boop6.gif',
          'https://trados77.github.io/gifs/boop7.gif',
          'https://trados77.github.io/gifs/boop8.gif',
          'https://trados77.github.io/gifs/boop9.gif'
          ]
    get_boop=random.choice(boop)
    if user:
        embed=discord.Embed(
            title=f"**{ctx.author.display_name}** boops **{user.display_name}**! Don't press too hard!",
            color=discord.Color.blurple()
        )
        embed.set_image(url=get_boop)
        await ctx.send(embed=embed)

@bot.command(name='blush')
async def reaction_blush(ctx, user: discord.Member= None):
    blush=['https://trados77.github.io/gifs/blush1.gif',
           'https://trados77.github.io/gifs/blush2.gif',
           'https://trados77.github.io/gifs/blush3.gif',
           'https://trados77.github.io/gifs/blush4.gif',
           'https://trados77.github.io/gifs/blush5.gif',
           'https://trados77.github.io/gifs/blush6.gif',
           'https://trados77.github.io/gifs/blush7.gif',
           'https://trados77.github.io/gifs/blush8.gif',
           'https://trados77.github.io/gifs/blush9.gif',
           'https://trados77.github.io/gifs/blush10.gif',
           'https://trados77.github.io/gifs/blush11.gif',
           'https://trados77.github.io/gifs/blush12.gif',
           'https://trados77.github.io/gifs/blush13.gif',
           'https://trados77.github.io/gifs/blush14.gif',
           'https://trados77.github.io/gifs/blush15.gif'
           ]
    get_blush=random.choice(blush)
    embed=discord.Embed(
        title=f"Ehhh, Why are you blushing **{ctx.author.display_name}?**",
        color=discord.Color.blurple()
    )
    embed.set_image(url=get_blush)
    await ctx.send(embed=embed)

@bot.command(name='pout')
async def reaction_pout(ctx, user: discord.Member= None):
    pout=['https://trados77.github.io/gifs/pout1.gif',
          'https://trados77.github.io/gifs/pout2.gif',
          'https://trados77.github.io/gifs/pout3.gif',
          'https://trados77.github.io/gifs/pout4.gif',
          'https://trados77.github.io/gifs/pout5.gif',
          'https://trados77.github.io/gifs/pout6.gif',
          'https://trados77.github.io/gifs/pout7.gif',
          'https://trados77.github.io/gifs/pout8.gif',
          'https://trados77.github.io/gifs/pout9.gif',
          'https://trados77.github.io/gifs/pout10.gif',
          'https://trados77.github.io/gifs/pout11.gif',
          'https://trados77.github.io/gifs/pout12.gif',
          'https://trados77.github.io/gifs/pout13.gif',
          'https://trados77.github.io/gifs/pout14.gif',
          'https://trados77.github.io/gifs/pout15.gif'
          ]
    get_pout=random.choice(pout)
    embed=discord.Embed(
        title=f'Who made **{ctx.author.display_name}** upset??',
        color=discord.Color.blurple()
    )
    embed.set_image(url=get_pout)
    await ctx.send(embed=embed)

@bot.command(name='sbonk')
async def super_bonk_member(ctx, user: discord.Member):
    super_bonk=['https://trados77.github.io/gifs/sbonk1.gif',
                'https://trados77.github.io/gifs/sbonk2.gif',
                'https://trados77.github.io/gifs/sbonk3.gif',
                'https://trados77.github.io/gifs/sbonk4.gif'
                ]
    get_super_bonk=random.choice(super_bonk)
    if ctx.author.id==discord_ID:
            embed=discord.Embed(
                title=f'Wow! My owner bonks **{user.display_name}**',
                color=discord.Color.blurple()
            )
            embed.set_image(url=get_super_bonk)
            await ctx.send(embed=embed)
    else:
        await ctx.send("**Only my creator, Mr. Snow, can use this command.**")


bot.run('MTE4NDE4Mjc2NjExNjUzNjQxMA.GP20dF.PwYv4YLY3WhAewAwthsuZHRnZYONBfnfMEEdrs')