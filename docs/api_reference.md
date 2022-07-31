# API Reference

## *func* `command_send`

Send an interaction response, specifically for `CommandContext`.

```py
from interactions.ext.files import command_send

async def test(ctx: interactions.CommandContext):

    await command_send(ctx, ...)
```

Parameters:
* `?content: str`: The contents of the message as a string or string-converted value.
* `?tts: bool`: Whether the message utilizes the text-to-speech Discord programme or not. Default to `False`.
* `?attachments: Attachment | list[Attachment]`: An attachment, or list of attachments to attach to the message. Needs to be uploaded to the CDN first.
* `?files: File | list[File]` A file, or list of files to attach to the message.
* `?embeds: Embed | list[Embed]`: An embed, or list of embeds for the message.
* `?allowed_mentions: MessageInteraction`: The message interactions/mention limits that the message can refer to.
* `?components: ActionRow | Button | SelectMenu | list[ActionRow, Button, SelectMenu]`: A component, or list of components for the message.
* `?ephemeral: bool`: Whether the response is hidden or not. Default to `False`.

## *func* `command_edit`

Edit an interaction response, specifically for `CommandContext`.

```py
from interactions.ext.files import command_edit

async def test(ctx: interactions.CommandContext):

    await ctx.send(...)

    await command_edit(ctx, ...)
```

Parameters:
* `?content: str`: The contents of the message as a string or string-converted value.
* `?tts: bool`: Whether the message utilizes the text-to-speech Discord programme or not. Default to `False`.
* `?attachments: Attachment | list[Attachment]`: An attachment, or list of attachments to attach to the message. Needs to be uploaded to the CDN first.
* `?files: File | list[File]` A file, or list of files to attach to the message.
* `?embeds: Embed | list[Embed]`: An embed, or list of embeds for the message.
* `?allowed_mentions: MessageInteraction`: The message interactions/mention limits that the message can refer to.
* `?components: ActionRow | Button | SelectMenu | list[ActionRow, Button, SelectMenu]`: A component, or list of components for the message.
* `?ephemeral: bool`: Whether the response is hidden or not. Default to `False`.

**Note:**

By default, when editing an interaction response, any previous sent `files` is counted in the `attachments` field, as how Discord payload works. To remove previous file that is sent using `files`, do `attachments=[]` and send new files in `files` if you wish to.

## *func* `component_send`

Send an interaction response, specifically for `ComponentContext`.

```py
from interactions.ext.files import component_send

async def test(ctx: interactions.ComponentContext):

    await component_send(ctx, ...)
```

Parameters:
* `?content: str`: The contents of the message as a string or string-converted value.
* `?tts: bool`: Whether the message utilizes the text-to-speech Discord programme or not. Default to `False`.
* `?attachments: Attachment | list[Attachment]`: An attachment, or list of attachments to attach to the message. Needs to be uploaded to the CDN first.
* `?files: File | list[File]` A file, or list of files to attach to the message.
* `?embeds: Embed | list[Embed]`: An embed, or list of embeds for the message.
* `?allowed_mentions: MessageInteraction`: The message interactions/mention limits that the message can refer to.
* `?components: ActionRow | Button | SelectMenu | list[ActionRow, Button, SelectMenu]`: A component, or list of components for the message.
* `?ephemeral: bool`: Whether the response is hidden or not. Default to `False`.

## *func* `component_edit`

Edit an interaction response, specifically for `ComponentContext`.


```py
from interactions.ext.files import component_edit

async def test(ctx: interactions.ComponentContext):

    await ctx.send(...)

    await component_edit(ctx, ...)
```

Parameters:
* `?content: str`: The contents of the message as a string or string-converted value.
* `?tts: bool`: Whether the message utilizes the text-to-speech Discord programme or not. Default to `False`.
* `?attachments: Attachment | list[Attachment]`: An attachment, or list of attachments to attach to the message. Needs to be uploaded to the CDN first.
* `?files: File | list[File]` A file, or list of files to attach to the message.
* `?embeds: Embed | list[Embed]`: An embed, or list of embeds for the message.
* `?allowed_mentions: MessageInteraction`: The message interactions/mention limits that the message can refer to.
* `?components: ActionRow | Button | SelectMenu | list[ActionRow, Button, SelectMenu]`: A component, or list of components for the message.
* `?ephemeral: bool`: Whether the response is hidden or not. Default to `False`.

**Note:**

By default, when editing an interaction response, any previous sent `files` is counted in the `attachments` field, as how Discord payload works. To remove previous file that is sent using `files`, do `attachments=[]` and send new files in `files` if you wish to.
