from db_manager import exists_in_db, register_new_user, update_all_users
from user_class import User
from config import active_users, db_connection
from discord.ext import commands
import random
import discord
import asyncio

def load_all_users():
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    for user_data in users:
        user = User(user_data[0])
        user.level = user_data[1]
        user.balance = user_data[2]
        user.xp = user_data[3]
        user.luck = user_data[4]
        user.name = user_data[5]  # Pet name
        active_users[user_data[0]] = user

def on_mention(member: discord.Member):
    if member.id not in active_users:
        user_data = exists_in_db(member.id)
        if user_data:
            print(f"Loaded user: {user_data}")
            new_user = User(user_data[0])
            new_user.level = user_data[1]
            new_user.balance = user_data[2]
            new_user.xp = user_data[3]
            new_user.luck = user_data[4]
            new_user.name = user_data[5]
            active_users[member.id] = new_user

# Registers all the bot commands
def register_commands(bot):

    load_all_users()

    @bot.command(name='plsdie', aliases=["end"], description="(Owner only) Ends the bot process.")
    @commands.is_owner()
    async def shutdown(ctx):
        print("Saving all data...")
        update_all_users(active_users)
        print("Shutting Down...")
        await ctx.send("Proceeding to die")
        await bot.close()

    @bot.command(name='register', aliases=["reg"], description="Registers you into the database.")
    async def register(ctx):
        user = exists_in_db(ctx.author.id)
        if user:
            await ctx.reply(f"{ctx.author.display_name}, you are already registered.")
            return
        if register_new_user(ctx.author):
            await ctx.reply(f"{ctx.author.display_name}, you have successfully registered, and have been given a free pet.")
        else:
            await ctx.reply(f"{ctx.author.display_name}, there was an issue with registering you.")

    @bot.command(name="show_db", description="Sends the current data of every user registered in the database.")
    async def show_db(ctx) -> None:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        if not users:
            await ctx.reply("No users in the database.")
            return
        for user in users:
            await ctx.send(f"ID: {user[0]}, Level: {user[1]}, Balance: {user[2]}, Petname: {user[5]}")

    @bot.command(name="changemoney", description="(Owner only) Changes a users money to any integer.")
    @commands.is_owner()
    async def changemoney(ctx, amount: float, member: discord.Member = None):
        if member is None:
            member = ctx.author
        on_mention(member)
        target_user: User = active_users.get(member.id)
        if target_user is None:
            await ctx.reply(f"Error: {member.display_name} is not registered.")
            return
        target_user.balance = round(target_user.balance + amount, 2)
        await ctx.send(f"You have changed ${amount} to {member.display_name}'s account.")

    # Command to check server latency
    @bot.command(name="ping", description="Pings the bot and displays the latency")
    async def ping(ctx):
        await ctx.send(f"Latency: {round(bot.latency * 1000)}ms")

    # Command to show user stats
    @bot.command(name="stats", aliases=["status", "s"], description="Displays your current stats.")
    async def stats(ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        on_mention(member)
        
        user: User = active_users.get(member.id)
        if user is None:
            await ctx.reply(f"{member.display_name}, you need to register first.")
            return
        
        embed = discord.Embed(
        title="Your Stats:",
        color=discord.Colour.fuchsia(),
        )
        # line 1
        embed.add_field(name="Pets Name", value=user.name)
        embed.add_field(name=" ", value=" ")  # break
        embed.add_field(name=f"Pet XP (Lv. {user.level})", value=user.xp)
        embed.add_field(name=f"Pet happiness", value=user.luck)        
        # line break
        embed.add_field(name="-----------------------------------", value=" ", inline=False)
        # line 2
        embed.add_field(name="Bank", value=f"${user.balance}", inline=False)
        
        embed.set_footer(text="Subject to change")
        embed.set_author(name=member.display_name, icon_url=ctx.author.avatar.url)
        
        await ctx.send(embed=embed)

    @bot.command(name="remove", description="(Owner only) Removes a user from the database.")
    @commands.is_owner()
    async def remove(ctx, member: discord.Member = None):
        user = exists_in_db(member.id)
        if user:
            cursor = db_connection.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (member.id,))
            db_connection.commit()
            active_users.pop(member.id, None)
            await ctx.send(f"User {member.display_name} removed from the database.")
        else:
            await ctx.reply(f"xsxirib, you need to register first.")

    ##########################################################
    ###################### GAME COMMANDS #####################
    ##########################################################
    
    @bot.command(name="namepet", description="Assigns a new name to your pet.")
    async def name_pet(ctx, name: str):
        target_user: User = active_users.get(ctx.author.id)
        if target_user is None:
            await ctx.reply(f"Error: {ctx.author.display_name} is not registered.")
            return
        
        target_user.name = name
        
        cursor = db_connection.cursor()
        cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, ctx.author.id))
        db_connection.commit()
        
        await ctx.send(f"You have changed your pet's name to {name}")