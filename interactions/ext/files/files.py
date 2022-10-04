from logging import Logger
from typing import List, Optional, Union

from aiohttp import MultipartWriter
from interactions.api.http.route import Route
from interactions.api.http.request import _Request
from interactions.base import get_logger
from interactions.client.context import (
    CommandContext,
    ComponentContext,
    _Context,
)
from interactions.client.models.component import _build_components

from interactions import (
    MISSING,
    ActionRow,
    Button,
    Embed,
    Attachment,
    File,
    InteractionCallbackType,
    Message,
    MessageInteraction,
    MessageReference,
    SelectMenu,
    Extension,
    Client,
    LibraryException,
)


log: Logger = get_logger("context")


class Inter_Request:
    """A custom version of InteractionRequest that add file sending."""
    _req = _Request

    def __init__(self) -> None:
        pass

    async def create_interaction_response(
        self, token: str, application_id: int, data: dict, files: Optional[List[File]] = MISSING
    ) -> None:

        file_data = None
        if files is not MISSING and len(files) > 0:

            file_data = MultipartWriter("form-data")
            part = file_data.append_json(data)
            part.set_content_disposition("form-data", name="payload_json")
            data = None

            for id, file in enumerate(files):
                part = file_data.append(
                    file._fp,
                )
                part.set_content_disposition(
                    "form-data", name=f"files[{str(id)}]", filename=file._filename
                )

        return await self._req.request(
            Route("POST", f"/interactions/{application_id}/{token}/callback"),
            json=data,
            data=file_data,
        )

    async def edit_interaction_response(
        self, data: dict, files: Optional[List[File]], token: str, application_id: str, message_id: str = "@original",
    ) -> dict:

        file_data = None
        if files is not MISSING and files is not None:

            file_data = MultipartWriter("form-data")
            part = file_data.append_json(data)
            part.set_content_disposition("form-data", name="payload_json")
            data = None

            for id, file in enumerate(files):
                part = file_data.append(
                    file._fp,
                )
                part.set_content_disposition(
                    "form-data", name=f"files[{str(id)}]", filename=file._filename
                )

        return await self._req.request(
            Route("PATCH", f"/webhooks/{application_id}/{token}/messages/{message_id}"),
            json=data,
            data=file_data,
        )

    async def _post_followup(
        self, data: dict, files: Optional[List[File]], token: str, application_id: str,
    ) -> dict:

        file_data = None
        if files is not MISSING and files is not None:
            file_data = MultipartWriter("form-data")
            part = file_data.append_json(data)
            part.set_content_disposition("form-data", name="payload_json")
            data = None

            for id, file in enumerate(files):
                part = file_data.append(
                    file._fp,
                )
                part.set_content_disposition(
                    "form-data", name=f"files[{str(id)}]", filename=file._filename
                )

        return await self._req.request(
            Route("POST", f"/webhooks/{application_id}/{token}"),
            json=data,
            data=file_data,
        )


class Context(_Context):
    """A custom version of _Context that add file sending."""

    def __init__(self):
        pass

    async def _send(
        self: _Context,
        content: Optional[str] = MISSING,
        *,
        tts: Optional[bool] = MISSING,
        attachments: Optional[List[Attachment]] = MISSING,
        files: Optional[Union[File, List[File]]] = MISSING,
        embeds: Optional[Union[Embed, List[Embed]]] = MISSING,
        allowed_mentions: Optional[MessageInteraction] = MISSING,
        components: Optional[
            Union[
                ActionRow,
                Button,
                SelectMenu,
                List[ActionRow],
                List[Button],
                List[SelectMenu],
            ]
        ] = MISSING,
        ephemeral: Optional[bool] = False,
    ) -> dict:

        if (
            content is MISSING
            and self.message
            and self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
        ):
            _content = self.message.content
        else:
            _content: str = "" if content is MISSING else content
        _tts: bool = False if tts is MISSING else tts

        if (
            embeds is MISSING
            and self.message
            and self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
        ):
            embeds = self.message.embeds
        _embeds: list = (
            []
            if not embeds or embeds is MISSING
            else ([embed._json for embed in embeds] if isinstance(embeds, list) else [embeds._json])
        )

        _allowed_mentions: dict = {} if allowed_mentions is MISSING else allowed_mentions

        if components is not MISSING and components:
            _components = _build_components(components=components)
        elif (
            components is MISSING
            and self.message
            and self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
        ):
            if isinstance(self.message.components, list):
                _components = self.message.components
            else:
                _components = [self.message.components]
        else:
            _components = []

        _attachments = [] if attachments is MISSING else [a._json for a in attachments]

        if not files or files is MISSING:
            _files = []
        elif isinstance(files, list):
            _files = [file._json_payload(id) for id, file in enumerate(files)]
        else:
            _files = [files._json_payload(0)]
            files = [files]

        _ephemeral: int = (1 << 6) if ephemeral else 0

        _files.extend(_attachments)

        payload: dict = dict(
            content=_content,
            tts=_tts,
            attachments=_files,
            embeds=_embeds,
            allowed_mentions=_allowed_mentions,
            components=_components,
            flags=_ephemeral,
        )

        return payload, files

    async def _edit(
        self: _Context,
        content: Optional[str] = MISSING,
        *,
        tts: Optional[bool] = MISSING,
        attachments: Optional[List[Attachment]] = MISSING,
        files: Optional[Union[File, List[File]]] = MISSING,
        embeds: Optional[Union[Embed, List[Embed]]] = MISSING,
        allowed_mentions: Optional[MessageInteraction] = MISSING,
        message_reference: Optional[MessageReference] = MISSING,
        components: Optional[
            Union[ActionRow, Button, SelectMenu, List[ActionRow], List[Button], List[SelectMenu]]
        ] = MISSING,
    ) -> dict:

        payload = {}

        if self.message.content is not None or content is not MISSING:
            _content: str = self.message.content if content is MISSING else content
            payload["content"] = _content

        _tts: bool = False if tts is MISSING else tts
        payload["tts"] = _tts

        if self.message.embeds is not None or embeds is not MISSING:
            if embeds is MISSING:
                embeds = self.message.embeds
            _embeds: list = (
                ([embed._json for embed in embeds] if isinstance(embeds, list) else [embeds._json])
                if embeds
                else []
            )
            payload["embeds"] = _embeds

        _allowed_mentions: dict = {} if allowed_mentions is MISSING else allowed_mentions
        _message_reference: dict = {} if message_reference is MISSING else message_reference._json

        payload["allowed_mentions"] = _allowed_mentions
        payload["message_reference"] = _message_reference

        if self.message.components is not None or components is not MISSING:
            if components is MISSING:
                _components = _build_components(components=self.message.components)
            elif not components:
                _components = []
            else:
                _components = _build_components(components=components)

            payload["components"] = _components

        if self.message.attachments is not None or attachments is not MISSING:
            if attachments is MISSING:
                attachments = self.message.attachments
            _attachments: list = (
                (
                    [attachment._json for attachment in attachments]
                    if isinstance(attachments, list)
                    else [attachments._json]
                )
                if attachments
                else []
            )

        if not files or files is MISSING:
            _files = []
        elif isinstance(files, list):
            _files = [file._json_payload(id) for id, file in enumerate(files)]
        else:
            _files = [files._json_payload(0)]
            files = [files]

        _files.extend(_attachments)

        payload["attachments"] = _files

        return payload, files


class Files(Extension):
    """I don't know what this does, but it is required to load the extension."""
    def __init__(self, client: Client):
        self.client: Client = client

    def command_send(self, content: Optional[str] = MISSING, **kwargs) -> Message:
        return command_send(self, content=content, **kwargs)

    def command_edit(self, content: Optional[str] = MISSING, **kwargs) -> Message:
        return command_edit(self, content=content, **kwargs)

    def component_send(self, content: Optional[str] = MISSING, **kwargs) -> Message:
        return component_send(self, content=content, **kwargs)

    def component_edit(self, content: Optional[str] = MISSING, **kwargs) -> Message:
        return component_send(self, content=content, **kwargs)


async def command_send(
    ctx: CommandContext, content: Optional[str] = MISSING, **kwargs
) -> Message:
    """
    This allows the invocation state described in the "context" to send an interaction response.

    :param content?: The contents of the message as a string or string-converted value.
    :type content?: Optional[str]
    :param tts?: Whether the message utilizes the text-to-speech Discord programme or not.
    :type tts?: Optional[bool]
    :param attachments?: The attachments to attach to the message. Needs to be uploaded to the CDN first
    :type attachments?: Optional[List[Attachment]]
    :param files?: The files to attach to the message.
    :type files?: Optional[Union[File, List[File]]]
    :param embeds?: An embed, or list of embeds for the message.
    :type embeds?: Optional[Union[Embed, List[Embed]]]
    :param allowed_mentions?: The message interactions/mention limits that the message can refer to.
    :type allowed_mentions?: Optional[MessageInteraction]
    :param components?: A component, or list of components for the message.
    :type components?: Optional[Union[ActionRow, Button, SelectMenu, List[Union[ActionRow, Button, SelectMenu]]]]
    :param ephemeral?: Whether the response is hidden or not.
    :type ephemeral?: Optional[bool]
    :return: The sent message as an object.
    :rtype: Message
    """

    if not isinstance(ctx, CommandContext):
        return log.warning(f"You can only use command_send for CommandContext, not {type(ctx).__name__}")

    payload, files = await Context._send(ctx, content, **kwargs)

    if not ctx.deferred:
        ctx.callback = InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE

    _payload: dict = {"type": ctx.callback.value, "data": payload}

    msg = None
    if ctx.responded:
        res = await Inter_Request._post_followup(
            ctx._client,
            data=payload,
            files=files,
            token=ctx.token,
            application_id=str(ctx.application_id),
        )
        ctx.message = msg = Message(**res, _client=ctx._client)
    else:
        await Inter_Request.create_interaction_response(
            ctx._client,
            token=ctx.token,
            application_id=int(ctx.id),
            data=_payload,
            files=files,
        )

        try:
            _msg = await ctx._client.get_original_interaction_response(
                ctx.token, str(ctx.application_id)
            )
        except LibraryException:
            pass
        else:
            ctx.message = msg = Message(**_msg, _client=ctx._client)

        ctx.responded = True

    if msg is not None:
        return msg

    return Message(
        **payload,
        _client=ctx._client,
        author={"_client": ctx._client, "id": None, "username": None, "discriminator": None},
    )


async def command_edit(
    ctx: CommandContext, content: Optional[str] = MISSING, **kwargs
) -> Message:
    """
    This allows the invocation state described in the "context" to edit an interaction response.

    :param content?: The contents of the message as a string or string-converted value.
    :type content?: Optional[str]
    :param tts?: Whether the message utilizes the text-to-speech Discord programme or not.
    :type tts?: Optional[bool]
    :param attachments?: The attachments to attach to the message. Needs to be uploaded to the CDN first
    :type attachments?: Optional[List[Attachment]]
    :param files?: The files to attach to the message.
    :type files?: Optional[Union[File, List[File]]]
    :param embeds?: An embed, or list of embeds for the message.
    :type embeds?: Optional[Union[Embed, List[Embed]]]
    :param allowed_mentions?: The message interactions/mention limits that the message can refer to.
    :type allowed_mentions?: Optional[MessageInteraction]
    :param components?: A component, or list of components for the message.
    :type components?: Optional[Union[ActionRow, Button, SelectMenu, List[Union[ActionRow, Button, SelectMenu]]]]
    :param ephemeral?: Whether the response is hidden or not.
    :type ephemeral?: Optional[bool]
    :return: The sent message as an object.
    :rtype: Message
    """

    if not isinstance(ctx, CommandContext):
        return log.warning(f"You can only use command_edit for CommandContext, not {type(ctx).__name__}")

    payload, files = await Context._edit(ctx, content, **kwargs)
    msg = None

    if ctx.deferred:
        if (
            hasattr(ctx.message, "id")
            and ctx.message.id is not None
            and ctx.message.flags != 64
        ):
            try:
                res = await ctx._client.edit_message(
                    int(ctx.channel_id), int(ctx.message.id), payload=payload, files=files
                )
            except LibraryException as e:
                if e.code in {10015, 10018}:
                    log.warning(f"You can't edit hidden messages." f"({e.message}).")
                else:
                    raise e from e
            else:
                ctx.message = msg = Message(**res, _client=ctx._client)
        else:
            try:
                res = await Inter_Request.edit_interaction_response(
                    ctx._client,
                    data=payload,
                    files=files,
                    token=ctx.token,
                    application_id=str(ctx.id),
                    message_id=ctx.message.id
                    if ctx.message and ctx.message.flags != 64
                    else "@original",
                )
            except LibraryException as e:
                if e.code in {10015, 10018}:
                    log.warning(f"You can't edit hidden messages." f"({e.message}).")
                else:
                    raise e from e
            else:
                ctx.message = msg = Message(**res, _client=ctx._client)
    else:
        try:
            res = await Inter_Request.edit_interaction_response(
                ctx._client, token=ctx.token, application_id=str(ctx.application_id), data=payload, files=files
            )
        except LibraryException as e:
            if e.code in {10015, 10018}:
                log.warning(f"You can't edit hidden messages." f"({e.message}).")
            else:
                raise e from e
        else:
            ctx.message = msg = Message(**res, _client=ctx._client)

    if msg is not None:
        return msg
    return Message(**payload, _client=ctx._client)


async def component_send(
    ctx: ComponentContext, content: Optional[str] = MISSING, **kwargs
) -> Message:
    """
    This allows the invocation state described in the "context" to send an interaction response.

    :param content?: The contents of the message as a string or string-converted value.
    :type content?: Optional[str]
    :param tts?: Whether the message utilizes the text-to-speech Discord programme or not.
    :type tts?: Optional[bool]
    :param attachments?: The attachments to attach to the message. Needs to be uploaded to the CDN first
    :type attachments?: Optional[List[Attachment]]
    :param files?: The files to attach to the message.
    :type files?: Optional[Union[File, List[File]]]
    :param embeds?: An embed, or list of embeds for the message.
    :type embeds?: Optional[Union[Embed, List[Embed]]]
    :param allowed_mentions?: The message interactions/mention limits that the message can refer to.
    :type allowed_mentions?: Optional[MessageInteraction]
    :param components?: A component, or list of components for the message.
    :type components?: Optional[Union[ActionRow, Button, SelectMenu, List[Union[ActionRow, Button, SelectMenu]]]]
    :param ephemeral?: Whether the response is hidden or not.
    :type ephemeral?: Optional[bool]
    :return: The sent message as an object.
    :rtype: Message
    """

    if not isinstance(ctx, ComponentContext):
        return log.warning(f"You can only use component_send for ComponentContext, not {type(ctx).__name__}")

    payload, files = await Context._send(ctx, content, **kwargs)

    if not ctx.deferred:
        ctx.callback = InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE

    _payload: dict = {"type": ctx.callback.value, "data": payload}

    msg = None
    if ctx.responded:
        res = await Inter_Request._post_followup(
            ctx._client,
            data=payload,
            token=ctx.token,
            application_id=str(ctx.application_id),
            files=files,
        )
        ctx.message = msg = Message(**res, _client=ctx._client)
    else:
        await Inter_Request.create_interaction_response(
            ctx._client,
            token=ctx.token,
            application_id=int(ctx.id),
            data=_payload,
            files=files,
        )

        try:
            _msg = await ctx._client.get_original_interaction_response(
                ctx.token, str(ctx.application_id)
            )
        except LibraryException:
            pass
        else:
            ctx.message = msg = Message(**_msg, _client=ctx._client)

        ctx.responded = True

    if msg is not None:
        return msg
    return Message(**payload, _client=ctx._client)


async def component_edit(
    ctx: ComponentContext, content: Optional[str] = MISSING, **kwargs
) -> Message:
    """
    This allows the invocation state described in the "context" to edit an interaction response.

    :param content?: The contents of the message as a string or string-converted value.
    :type content?: Optional[str]
    :param tts?: Whether the message utilizes the text-to-speech Discord programme or not.
    :type tts?: Optional[bool]
    :param attachments?: The attachments to attach to the message. Needs to be uploaded to the CDN first
    :type attachments?: Optional[List[Attachment]]
    :param files?: The files to attach to the message.
    :type files?: Optional[Union[File, List[File]]]
    :param embeds?: An embed, or list of embeds for the message.
    :type embeds?: Optional[Union[Embed, List[Embed]]]
    :param allowed_mentions?: The message interactions/mention limits that the message can refer to.
    :type allowed_mentions?: Optional[MessageInteraction]
    :param components?: A component, or list of components for the message.
    :type components?: Optional[Union[ActionRow, Button, SelectMenu, List[Union[ActionRow, Button, SelectMenu]]]]
    :param ephemeral?: Whether the response is hidden or not.
    :type ephemeral?: Optional[bool]
    :return: The sent message as an object.
    :rtype: Message
    """

    if not isinstance(ctx, ComponentContext):
        return log.warning(f"You can only use component_edit for ComponentContext, not {type(ctx).__name__}")

    payload, files = await Context._edit(ctx, content, **kwargs)

    msg = None

    if not ctx.deferred:
        ctx.callback = InteractionCallbackType.UPDATE_MESSAGE
        await Inter_Request.create_interaction_response(
            ctx._client,
            token=ctx.token,
            application_id=int(ctx.id),
            data={"type": ctx.callback.value, "data": payload},
            files=files,
        )

        try:
            _msg = await ctx._client.get_original_interaction_response(
                ctx.token, str(ctx.application_id)
            )
        except LibraryException:
            pass
        else:
            ctx.message = msg = Message(**_msg, _client=ctx._client)

        ctx.responded = True

    elif ctx.callback != InteractionCallbackType.DEFERRED_UPDATE_MESSAGE:
        await Inter_Request._post_followup(
            ctx._client,
            data=payload,
            files=files,
            token=ctx.token,
            application_id=str(ctx.application_id),
        )
    else:
        res = await Inter_Request.edit_interaction_response(
            ctx._client,
            data=payload,
            files=files,
            token=ctx.token,
            application_id=str(ctx.application_id),
        )
        ctx.responded = True
        ctx.message = msg = Message(**res, _client=ctx._client)

    if msg is not None:
        return msg

    return Message(**payload, _client=ctx._client)


def setup(client: Client) -> Files:
    """Setup the extension."""

    _Context.send = Context._send
    _Context.edit = Context._edit
    CommandContext.send = command_send
    CommandContext.edit = command_edit
    ComponentContext.send = component_send
    ComponentContext.edit = component_edit
    return Files(client)
