import interactions
import io


client = interactions.Client(
    token="YOUR_TOKEN_HERE",
    intents=interactions.Intents.DEFAULT
)

# These are just normal parts of the bot.

# To use files in CommandContext send, you need to load it as an extension.
client.load('interactions-ext-files')


# Now we have the necessary parts, let's create a basic command to demonstrate it.

@client.command(
    name="write",
    description="Write the message content to a file",
    options=[
        interactions.Option(
            type=interactions.OptionType.STRING, # We need the message content, so the option will be a STRING type.
            name="content",
            description="The content to write to the file",
            required=True
        )
    ]
)
async def _write(ctx: interactions.CommandContext, content: str):
    file = io.StringIO(content) # We use StringIO from the io module to utilize a file object.
    files = interactions.File(
        filename="message.txt", # We name the file "message.txt"
        fp=file # This is the io file object we created above.
    )
    await ctx.send(
        content="Read the message in a test file below.", # This is the content of the message.
        files=files # The param in ``send`` to send File object is ``files``.
    )


client.start()
