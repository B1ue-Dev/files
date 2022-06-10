from typing import List, Optional, Union

from aiohttp import MultipartWriter
from interactions.api.http.route import Route
from interactions.client.context import CommandContext, ComponentContext, _Context
from interactions.client.models.component import _build_components

from interactions import (
    MISSING,
    ActionRow,
    Button,
    Embed,
    File,
    InteractionCallbackType,
    Message,
    MessageInteraction,
    MessageReference,
    SelectMenu,
    Extension,
    Client,
)


class Files(Extension):
    def __init__(self, client: Client):
        async def create_interaction_response(
            self, token: str, application_id: int, data: dict, files: List[File]
        ) -> None:
            """
            Posts initial response to an interaction, but you need to add the token.

            :param token: Token.
            :param application_id: Application ID snowflake
            :param data: The data to send.
            """

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
            self,
            data: dict,
            files: List[File],
            token: str,
            application_id: str,
            message_id: str = "@original",
        ) -> dict:
            """
            Edits an existing interaction message, but token needs to be manually called.

            :param data: A dictionary containing the new response.
            :param token: the token of the interaction
            :param application_id: Application ID snowflake.
            :param message_id: Message ID snowflake. Defaults to `@original` which represents the initial response msg.
            :return: Updated message data.
            """

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
                Route(
                    "PATCH", f"/webhooks/{application_id}/{token}/messages/{message_id}"
                ),
                json=data,
                data=file_data,
            )

        async def _post_followup(
            self,
            data: dict,
            files: List[File],
            token: str,
            application_id: str,
        ) -> dict:
            """
            Send a followup to an interaction.

            :param data: the payload to send
            :param application_id: the id of the application
            :param token: the token of the interaction
            """
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

        async def base_send(
            self,
            content: Optional[str] = MISSING,
            *,
            tts: Optional[bool] = MISSING,
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
        ) -> Message:

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
                else (
                    [embed._json for embed in embeds]
                    if isinstance(embeds, list)
                    else [embeds._json]
                )
            )

            _allowed_mentions: dict = (
                {} if allowed_mentions is MISSING else allowed_mentions
            )

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

            if not files or files is MISSING:
                _files = []
            elif isinstance(files, list):
                _files = [file._json_payload(id) for id, file in enumerate(files)]
            else:
                _files = [files._json_payload(0)]
                files = [files]

            _ephemeral: int = (1 << 6) if ephemeral else 0

            payload: Message = Message(
                content=_content,
                tts=_tts,
                # files=file,
                attachments=_files,
                embeds=_embeds,
                allowed_mentions=_allowed_mentions,
                components=_components,
                flags=_ephemeral,
            )
            self.message = payload
            self.message._client = self.client
            return payload, files

        async def base_edit(
            self,
            content: Optional[str] = MISSING,
            *,
            tts: Optional[bool] = MISSING,
            files: Optional[Union[File, List[File]]] = MISSING,
            embeds: Optional[Union[Embed, List[Embed]]] = MISSING,
            allowed_mentions: Optional[MessageInteraction] = MISSING,
            message_reference: Optional[MessageReference] = MISSING,
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
        ) -> Message:

            payload = {}

            if self.message.content is not None or content is not MISSING:
                _content: str = self.message.content if content is MISSING else content
                payload["content"] = _content

            _tts: bool = False if tts is MISSING else tts
            payload["tts"] = _tts

            if self.message.embeds is not None or embeds is not MISSING:
                if embeds is MISSING:
                    embeds = self.message.embeds
                    _embeds = []
                _embeds: list = (
                    []
                    if not embeds
                    else (
                        [embed._json for embed in embeds]
                        if isinstance(embeds, list)
                        else [embeds._json]
                    )
                )
                payload["embeds"] = _embeds

            _allowed_mentions: dict = (
                {} if allowed_mentions is MISSING else allowed_mentions
            )
            _message_reference: dict = (
                {} if message_reference is MISSING else message_reference._json
            )

            payload["allowed_mentions"] = _allowed_mentions
            payload["message_reference"] = _message_reference

            if self.message.components is not None or components is not MISSING:
                if components is MISSING:
                    _components = self.message.components
                elif not components:
                    _components = []
                else:
                    _components = _build_components(components=components)
                payload["components"] = _components

            if files is MISSING:
                pass
            else:
                if not files:
                    _files = []
                elif isinstance(files, list):
                    _files = [file._json_payload(id) for id, file in enumerate(files)]
                else:
                    _files = [files._json_payload(0)]
                    files = [files]
                payload["attachments"] = _files

            payload = Message(**payload)
            self.message._client = self.client

            return payload, files

        async def command_send(
            self, content: Optional[str] = MISSING, **kwargs
        ) -> Message:
            payload, files = await base_send(self, content, **kwargs)

            if not self.deferred:
                self.callback = InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE

            _payload: dict = {"type": self.callback.value, "data": payload._json}

            msg = None
            if self.responded or self.deferred:
                if self.deferred:
                    res = await edit_interaction_response(
                        self.client,
                        data=payload._json,
                        files=files,
                        token=self.token,
                        application_id=str(self.application_id),
                    )
                    self.deferred = False
                    self.responded = True
                else:
                    res = await self.client._post_followup(
                        data=payload._json,
                        token=self.token,
                        application_id=str(self.application_id),
                    )
                self.message = msg = Message(**res, _client=self.client)
            else:
                res = await create_interaction_response(
                    self.client,
                    token=self.token,
                    application_id=int(self.id),
                    data=_payload,
                    files=files,
                )
                if res and not res.get("code"):
                    self.message = msg = Message(**res, _client=self.client)
                self.responded = True
            if msg is not None:
                return msg
            return payload

        async def command_edit(
            self, content: Optional[str] = MISSING, **kwargs
        ) -> Message:
            payload, files = await base_edit(self, content, **kwargs)
            msg = None

            if self.deferred:
                if hasattr(self.message, "id") and self.message.id is not None:
                    res = await self.client.edit_message(
                        int(self.channel_id),
                        int(self.message.id),
                        payload=payload._json,
                        files=files,
                    )
                    self.message = msg = Message(**res, _client=self.client)
                else:
                    res = await edit_interaction_response(
                        self.client,
                        token=self.token,
                        application_id=str(self.id),
                        data={"type": self.callback.value, "data": payload._json},
                        files=files,
                        message_id=self.message.id if self.message else "@original",
                    )
                    if res["flags"] == 64:
                        print("You cannot edit hidden messages.")
                        self.message = payload
                        self.message._client = self.client
                    else:
                        await self.client.edit_message(
                            int(self.channel_id),
                            res["id"],
                            payload=payload._json,
                            files=files,
                        )
                        self.message = msg = Message(**res, _client=self.client)
            else:
                res = await edit_interaction_response(
                    self.client,
                    data={"type": self.callback.value, "data": payload._json},
                    files=files,
                    token=self.token,
                    application_id=str(self.application_id),
                )
                if res["flags"] == 64:
                    print("You cannot edit hidden messages.")
                else:
                    await self.client.edit_message(
                        int(self.channel_id),
                        res["id"],
                        payload=payload._json,
                        files=files,
                    )
                    self.message = msg = Message(**res, _client=self.client)

            if msg is not None:
                return msg
            return payload

        async def component_send(
            self, content: Optional[str] = MISSING, **kwargs
        ) -> Message:
            payload, files = await base_send(self, content, **kwargs)

            if not self.deferred:
                self.callback = InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE

            _payload: dict = {"type": self.callback.value, "data": payload._json}

            msg = None
            if (
                self.responded
                or self.deferred
                or self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
            ):
                if self.deferred:
                    res = await edit_interaction_response(
                        self.client,
                        data=payload._json,
                        files=files,
                        token=self.token,
                        application_id=str(self.application_id),
                    )
                    self.deferred = False
                    self.responded = True
                else:
                    res = await _post_followup(
                        self.client,
                        data=payload._json,
                        files=files,
                        token=self.token,
                        application_id=str(self.application_id),
                    )
                self.message = msg = Message(**res, _client=self.client)
            else:
                res = await create_interaction_response(
                    self.client,
                    token=self.token,
                    application_id=int(self.id),
                    data=_payload,
                    files=files,
                )
                if res and not res.get("code"):
                    # if sending message fails somehow
                    msg = Message(**res, _client=self.client)
                    self.message = msg
                self.responded = True

            if msg is not None:
                return msg
            return payload

        async def component_edit(
            self, content: Optional[str] = MISSING, **kwargs
        ) -> Message:
            payload, files = await base_edit(self, content, **kwargs)

            msg = None

            if not self.deferred:
                self.callback = InteractionCallbackType.UPDATE_MESSAGE
                await create_interaction_response(
                    self.client,
                    token=self.token,
                    application_id=int(self.id),
                    data={"type": self.callback.value, "data": payload._json},
                    files=files,
                )
                self.message = payload
                self.responded = True
            elif self.callback != InteractionCallbackType.DEFERRED_UPDATE_MESSAGE:
                await _post_followup(
                    self.client,
                    data=payload._json,
                    files=files,
                    token=self.token,
                    application_id=str(self.application_id),
                )
            else:
                res = await edit_interaction_response(
                    self.client,
                    data=payload._json,
                    files=files,
                    token=self.token,
                    application_id=str(self.application_id),
                )
                self.responded = True
                self.message = msg = Message(**res, _client=self.client)

            if msg is not None:
                return msg

            return payload

        _Context.send = base_send
        CommandContext.send = command_send
        CommandContext.edit = command_edit
        ComponentContext.send = component_send
        ComponentContext.edit = component_edit


def setup(client: Client):
    return Files(client)
