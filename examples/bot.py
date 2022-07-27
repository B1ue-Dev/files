"""
This is just to please pylint.
"""

import io
import interactions


client = interactions.Client(
    token="YOUR_TOKEN_HERE", intents=interactions.Intents.DEFAULT
)

# These are just normal parts of the bot.

# To use files in CommandContext send, you need to load it as an extension.
client.load("interactions-ext-files")

# We have the necessary parts, let's create a basic command to demonstrate it.


@client.command(
    name="write",
    description="Write the message content to a file",
    options=[
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="content",
            description="The content to write to the file",
            required=True,
        )
    ],
)
async def write(ctx: interactions.CommandContext, content: str):
    """Write the message content to a file."""
    file = io.StringIO(
        content
    )  # We use StringIO from the io module to utilize a file object.
    files = interactions.File(
        filename="message.txt",  # We name the file "message.txt"
        fp=file,  # This is the io file object we created above.
    )
    await ctx.send(
        content="Read the message in a test file below.",
        files=files,  # The param in ``send`` to send File object is ``files``.
    )

client.start()
