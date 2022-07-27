"""
pylint.
"""

import io
import interactions


class _Files(interactions.Extension):
    """Extension to demonstrate the use of `files`."""
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    # After that, we just create the command, like the example below.
    @interactions.extension_command(
        name="write",
        description="Write the message content to a file",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="content",
                description="The content to write to the file",
                required=True
            )
        ]
    )
    async def write(self, ctx: interactions.CommandContext, content: str):
        """Write the message content to a file."""
        # We use StringIO from the io module to utilize a file object.
        file = io.StringIO(content)
        files = interactions.File(
            filename="message.txt",  # We name the file "message.txt"
            fp=file  # This is the io file object we created above.
        )
        await ctx.send(
            content="Read the message in a test file below.",
            files=files  # The param in `send` to send File object is `files`.
        )


# Set up the extension.
def setup(client) -> None:
    """Setup the Extension."""
    _Files(client)
