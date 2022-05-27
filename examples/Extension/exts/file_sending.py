import interactions
import io


# We create an Extension object.
class File_Sending(interactions.Extension):
    def __init__(self, client):
        self.client = client

    # After that, we just create the command, like the example below.
    @interactions.extension_command(
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
    async def _write(self, ctx: interactions.CommandContext, content: str):
        file = io.StringIO(content) # We use StringIO from the io module to utilize a file object. 
        files = interactions.File(
            filename="message.txt", # We name the file "message.txt"
            fp=file # This is the io file object we created above.
        )
        await ctx.send(
            content="Read the message in a test file below.", # This is the content of the message.
            files=files # The param in ``send`` to send File object is ``files``.
        )



# Set up the extension.
def setup(client):
    client.load('exts.file_sending')
