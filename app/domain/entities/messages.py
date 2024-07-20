from dataclasses import dataclass, field
from datetime import datetime

from app.domain.values.messages import Text, Title
from app.domain.entities.base import BaseEntity
from app.domain.events.messages import NewMessageReceivedEvent


@dataclass(eq=False)
class Message(BaseEntity):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    text: Text

    def pull_events(self):
        registered_events = copy(self._events)
        self._events.clear()

        return registered_events


@dataclass(eq=False)
class Chat(BaseEntity):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(NewMessageReceivedEvent(
            message_text=message.text.as_generic_type(),
            chat_oid=self.oid,
            message_oid=message.oid,
        ))
