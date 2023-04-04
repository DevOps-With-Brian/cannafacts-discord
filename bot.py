import discord
import os
import requests
import json
import re


discord_token = os.getenv("DISCORD_TOKEN")
api_url = os.getenv("API_URL")


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    def lookup_strain(self, strain_name):
        # Make api call to get strain information
        url = api_url + "/strains/" + strain_name
        response = requests.get(url)
        data = response.json()
        return data
    
    def sanitize_message(self, message):
        # Define a regular expression that matches any non-printable characters or escape sequences
        non_printable_regex = r"[\x00-\x1f\x7f-\xff\u2028\u2029]"

        # Remove any non-printable characters or escape sequences from the input string
        sanitized_message = re.sub(non_printable_regex, "", message.content)

        return sanitized_message

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith('!cf'):
            if message.content == '!cf help':
                await message.channel.send('Available commands:\n !cf flavors - Gives back the flavor info for a strain.\n !cf helps_with - Gives back the things the strain has been known to help with.\n !cf strain - Get information about a specific strain.\n !cf strain_type - Get the type of strain based on the name, ie hybrid, sativa, indica.\n !cf thc - Get the thc percentage for a given strain name.')
                return
            if message.content.__contains__('!cf strain '):
                await message.channel.send('Sure give me a sec to look that up...')
                sanitized_message = self.sanitize_message(message)

                # Make api call to get strain information
                strain_name = sanitized_message.split("!cf strain ")[1]

                print("Currently being asked about strain: {}".format(strain_name))
                
                data = self.lookup_strain(strain_name)
                print(data)

                if "detail" in data:
                    # Respond to the cannafacts strain command
                    await message.channel.send(data["detail"])
                elif data['name']:
                    strain_name = data["name"]
                    thc_level = data["thc_level"]
                    strain_type = data["strain_type"]
                    flavors = data["flavors"]
                    feelings = data["feelings"]
                    helps_with = data["helps_with"]

                    # Write up our own response from the data
                    result = "{0} is a {1} strain with a thc level of {2}. It has the following flavors: {3}.  Some known feelings are: {4}.  It has been known to help with: {5}".format(
                        strain_name, strain_type, thc_level, flavors, feelings, helps_with
                    )

                    await message.channel.send(result)
                return
            

            if message.content.__contains__('!cf thc'):
                # Remove any non-printable characters or escape sequences from the input string
                sanitized_message = self.sanitize_message(message)
                strain_name = sanitized_message.split("!cf thc ")[1]
                await message.channel.send('Sure give me a sec to look that up...')
                
                # Make api call to get strain information
                data = self.lookup_strain(strain_name)

                if "detail" in data:
                    # Respond to the cannafacts thc command
                    await message.channel.send(data["detail"])
                elif "thc_level" in data:
                    # Respond to the cannafacts thc command
                    await message.channel.send(
                        "Strain: {0} has a thc level of {1}".format(
                            strain_name, data["thc_level"]
                        )
                    )
                else:
                    print("Not sure what hits here...")
                return
            

            if message.content.__contains__('!cf flavors'):
                await message.channel.send('Sure give me a sec to look that up...')
                sanitized_message = self.sanitize_message(message)
                strain_name = sanitized_message.split("!cf flavors ")[1]
                data = self.lookup_strain(strain_name)

                if "detail" in data:
                    # Respond to the cannafacts thc command
                    await message.channel.send(data["detail"])
                elif "flavors" in data:
                    # Respond to the cannafacts thc command
                    await message.channel.send(
                        "Strain: {0} has a flavor profile of {1}".format(
                            strain_name, data["flavors"]
                        )
                    )
                else:
                    print("Not sure what hits here...")

            
            if message.content.__contains__('!cf helps_with'):
                await message.channel.send('Sure give me a sec to look that up...')
                sanitized_message = self.sanitize_message(message)
                strain_name = sanitized_message.split("!cf helps_with ")[1]
                data = self.lookup_strain(strain_name)

                if "detail" in data:
                    # Respond to the cannafacts thc command
                    await message.channel.send(data["detail"])
                elif "helps_with" in data:
                    # Respond to the cannafacts thc command
                    await message.channel.send(
                        "Strain: {0} has been known to help with the following things: {1}".format(
                            strain_name, data["helps_with"]
                        )
                    )
                else:
                    print("Not sure what hits here...")

            
            if message.content.__contains__('!cf strain_type'):
                await message.channel.send('Sure give me a sec to look that up...')
                sanitized_message = self.sanitize_message(message)
                strain_name = sanitized_message.split("!cf strain_type ")[1]
                data = self.lookup_strain(strain_name)

                if "detail" in data:
                    # Respond to the cannafacts thc command
                    await message.channel.send(data["detail"])
                elif "strain_type" in data:
                    # Respond to the cannafacts thc command
                    await message.channel.send(
                        "Strain: {0}'s strain type is: {1}".format(
                            strain_name, data["strain_type"]
                        )
                    )
                else:
                    print("Not sure what hits here...")

        print(message.channel)
        print(message.channel.id)
        print(message.content)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)
