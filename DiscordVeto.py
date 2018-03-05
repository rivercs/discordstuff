import discord
import config


client = discord.Client()
email = config.email
password = config.password


#The bot itself
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        print("message received from bot account")
        return

    if message.content.startswith("!veto"):
        maps = []
        maps.extend (config.maps)
        print("message started with !veto\nthe map pool is loaded: ",maps)
        while len(maps) >= 1:
            if len(maps) == 1:
                await client.send_message(message.channel, "Selected map: " + maps[0])
                maps.clear()
                print("maps are cleared: ", maps)
                return
            else:
                if message.author == client.user:
                    print("caught bot trying to reply to itself")
                    return
                await client.send_message(message.channel, "Maps left: " + ','.join(maps))
                await client.send_message(message.channel, "Enter your veto (for example de_dust2)")
                messageobj = await client.wait_for_message()
                userVeto = messageobj.content
                print(messageobj.author,"vetoed: ",userVeto)
                if any(userVeto in s for s in maps):
                    maps.remove(userVeto)
                    print("removed map, the current pool is: ",maps)
                    await client.send_message(message.channel, "Removed " + userVeto)


#Display account info when logged in
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#Login to account
client.run(email, password)