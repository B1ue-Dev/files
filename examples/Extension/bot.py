"""
Again, pylint.
"""

import interactions


client = interactions.Client(
    token="YOUR_TOKEN_HERE", intents=interactions.Intents.DEFAULT
)

# These are just normal parts of the bot.

# To use files in CommandContext send, you need to load it as an extension.
client.load("interactions-ext-files")
# We load the Extension.
client.load("exts._files")

client.start()
