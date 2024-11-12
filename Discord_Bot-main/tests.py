    # @bot.command(name = "mm")
    # async def mm(ctx):
    #     print("mm started")
    #     await ctx.send("yes or no")

    #     accepted_responses = ["yes", "no", "im sure", "im really sure", "im really really sure"]

    #     def check(m):
    #         if m.author == ctx.author:
    #             if m.content.lower() in accepted_responses:
    #                 return True
    #             else:
    #                 bot.loop.create_task(ctx.send("Invalid input."))
    #         return
    
    #     try:
    #         print("trying")
    #         msg = await bot.wait_for("message",check=check)

    #         ans = 0

    #         if msg.content.lower() == "yes":
    #             ans += 1
    #             print(ans)
    #         if msg.content.lower() == "no": 
    #             ans += -1
    #             print(ans)
    #         print('check 0')
    #         await ctx.send("are you sure?")
    #         msg = await bot.wait_for("message",check=check)
    #         if msg.content.lower() == "im sure":
    #             print('check 1')
    #             await ctx.send("are you really sure?")
    #             msg = await bot.wait_for("message",check=check)
    #             if msg.content.lower() == "im really sure":
    #                 print('check 2')
    #                 await ctx.send("are you really really sure?")
    #                 msg = await bot.wait_for("message",check=check)
    #                 if msg.content.lower() == "im really really sure":
    #                     print('check 3')
    #                     if ans > 0:
    #                         await ctx.send("you lose")
    #                     elif ans < 0:
    #                         await ctx.send("you win")
                
    #     except IndexError: 
    #         print("index error")
    #         pass