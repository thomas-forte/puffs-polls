from datetime import datetime
import discord


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.setting_up_a_poll = 0
    client.polls = []
    client.pollEmojis = {
      discord.PartialEmoji(name='🇦'): 0,
      discord.PartialEmoji(name='🇧'): 0,
      discord.PartialEmoji(name='🇨'): 0,
      discord.PartialEmoji(name='🇩'): 0,
      discord.PartialEmoji(name='🇪'): 0,
      discord.PartialEmoji(name='🇫'): 0,
    },

@client.event
async def on_message(message):
    if client.user in message.mentions:
      
      if message.content.startswith(f'<@!{client.user.id}> teach me how to drive'):
        print(f'teaching {message.author.name}')
        await message.channel.send(f'Sure thing, just ask me to start a poll include the options A-Z. You can even include who you want to participate. \n `@{client.user.name} start a poll`')
      
      elif message.content.startswith(f'<@!{client.user.id}> start a poll') and not client.setting_up_a_poll:
        print(f'starting a poll {message.author.name}')
        client.setting_up_a_poll = 1
        await message.channel.send('Sure thing, what do you want to call it?')

      elif client.setting_up_a_poll:
        print(f'poll setup in progress continuing {message.author.name}')

        if message.content.startswith(f'<@!{client.user.id}> floor it'):
          client.setting_up_a_poll = 0
          await message.channel.send(f'Attention @everyone please vote on the following:\n{client.poll_name}\n- 🇫\n- 🇫\n- 🇫\n- 🇫\n- 🇫')
          # client.polls.append({
          #   'started': datetime.now(),
          #   'name': client.poll_name,
          #   'options': [

          #   ],
          #   'crowd': []
          # })
        
        elif client.setting_up_a_poll == 1:
          poll_name = message.content[len(f'<@!{client.user.id}> '):]
          print(f'saving poll name {poll_name} from {message.author.name}')
          client.poll_name = poll_name
          await message.channel.send('Noted, so tell me about the first option?')
          client.options = []
          client.setting_up_a_poll = 2
        
        elif client.setting_up_a_poll > 1:
          option = message.content[len(f'<@!{client.user.id}> '):]
          print(f'saving poll option {option} from {message.author.name}')
          client.options.append(option)
          await message.channel.send('Keep it going.')
          client.setting_up_a_poll += 1
        
client.run('token')
