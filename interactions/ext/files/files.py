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
        self.client: Client = client

        async def create_interaction_response(
            self, token: str, application_id: int, data: dict, files: List[File]
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
            self, data: dict, files: List[File], token: str, application_id: str, message_id: str = "@original",
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
                Route(
                    "PATCH", f"/webhooks/{application_id}/{token}/messages/{message_id}"
                ),
                json=data,
                data=file_data,
            )

        async def post_followup(
            self, data: dict, files: List[File], token: str, application_id: str,
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

            if not files or files is MISSING:
                _files = []
            elif isinstance(files, list):
                _files = [file._json_payload(id) for id, file in enumerate(files)]
            else:
                _files = [files._json_payload(0)]
                files = [files]

            _ephemeral: int = (1 << 6) if ephemeral else 0

            payload: dict = dict(
                content=_content,
                tts=_tts,
                # files=file,
                attachments=_files,
                embeds=_embeds,
                allowed_mentions=_allowed_mentions,
                components=_components,
                flags=_ephemeral,
            )

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
                    []
                    if not embeds
                    else (
                        [embed._json for embed in embeds]
                        if isinstance(embeds, list)
                        else [embeds._json]
                    )
                )
                payload["embeds"] = _embeds

            _allowed_mentions: dict = {} if allowed_mentions is MISSING else allowed_mentions
            _message_reference: dict = {} if message_reference is MISSING else message_reference._json

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

            return payload, files



        async def command_send(
            self, content: Optional[str] = MISSING, **kwargs
        ) -> Message:
            payload, files = await base_send(self, content, **kwargs)

            if not self.deferred:
                self.callback = InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE

            _payload: dict = {"type": self.callback.value, "data": payload}

            msg = None
            if self.responded or self.deferred:
                if self.deferred:
                    res = await edit_interaction_response(
                        self.client,
                        data=payload,
                        files=files,
                        token=self.token,
                        application_id=str(self.application_id),
                    )
                    # self.deferred = False
                    # self.responded = True
                else:
                    res = await post_followup(
                        self.client,
                        data=payload,
                        files=files,
                        token=self.token,
                        application_id=str(self.application_id),
                    )
                self.message = msg = Message(**res, _client=self.client)
            else:
                await create_interaction_response(
                    self.client,
                    token=self.token,
                    application_id=int(self.id),
                    data=_payload,
                    files=files,
                )
                __newdata = await self._client.edit_interaction_response(
                    data={},
                    token=self.token,
                    application_id=str(self.application_id),
                )
                if not __newdata.get("code"):
                    # if sending message fails somehow
                    msg = Message(**__newdata, _client=self._client)
                    self.message = msg
                self.responded = True
            if msg is not None:
                return msg

            return Message(
                **payload,
                _client=self._client,
                author={"_client": self._client, "id": None, "username": None, "discriminator": None},
            )


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
                        payload=payload,
                        files=files,
                    )
                    self.message = msg = Message(**res, _client=self.client)
                else:
                    res = await edit_interaction_response(
                        self.client,
                        token=self.token,
                        application_id=str(self.id),
                        data={"type": self.callback.value, "data": payload},
                        files=files,
                        message_id=self.message.id if self.message else "@original",
                    )
                    if res["flags"] == 64:
                        print("You cannot edit hidden messages.")
                    else:
                        await self.client.edit_message(
                            int(self.channel_id),
                            res["id"],
                            payload=payload,
                            files=files,
                        )
                        self.message = msg = Message(**res, _client=self.client)
            else:
                res = await edit_interaction_response(
                    self.client,
                    data={"type": self.callback.value, "data": payload},
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
                        payload=payload,
                        files=files,
                    )
                    await self._client.edit_message(int(self.channel_id), res["id"], payload=payload, files=files)
                    self.message = msg = Message(**res, _client=self.client)

            if msg is not None:
                return msg
            return Message(**payload, _client=self._client)


        async def component_send(
            self, content: Optional[str] = MISSING, **kwargs
        ) -> Message:
            payload, files = await base_send(self, content, **kwargs)

            if not self.deferred:
                self.callback = InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE

            _payload: dict = {"type": self.callback.value, "data": payload}

            msg = None
            if (
                self.responded
                or self.deferred
                or self.callback == InteractionCallbackType.DEFERRED_UPDATE_MESSAGE
            ):
                if self.deferred:
                    res = await edit_interaction_response(
                        self.client,
                        data=payload,
                        files=files,
                        token=self.token,
                        application_id=str(self.application_id),
                    )
                    # self.deferred = False
                    self.responded = True
                else:
                    res = await post_followup(
                        self.client,
                        data=payload,
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
            return Message(**payload)


        async def component_edit(
            self, content: Optional[str] = MISSING, **kwargs
        ) -> Message:
            payload, files = await base_edit(self, content, **kwargs)
            
            if not self.deferred:
                self.callback = InteractionCallbackType.UPDATE_MESSAGE
                await create_interaction_response(
                    self.client,
                    token=self.token,
                    application_id=int(self.id),
                    data={"type": self.callback.value, "data": payload},
                    files=files,
                )
                # self.message = payload
                self.responded = True

            elif self.callback != InteractionCallbackType.DEFERRED_UPDATE_MESSAGE:
                res = await post_followup(
                    self.client,
                    data=payload,
                    files=files,
                    token=self.token,
                    application_id=str(self.application_id),
                )
                self.message = Message(**res, _client=self._client)
            else:
                res = await edit_interaction_response(
                    self.client,
                    data=payload,
                    files=files,
                    token=self.token,
                    application_id=str(self.application_id),
                )
                self.responded = True
                self.message = Message(**res, _client=self._client)

            if self.message is None:
                self.message = Message(**payload, _client=self._client)

            return self.message


        _Context.send = base_send
        _Context.edit = base_edit
        CommandContext.send = command_send
        CommandContext.edit = command_edit
        ComponentContext.send = component_send
        ComponentContext.edit = component_edit


def setup(client: Client):
    return Files(client)
