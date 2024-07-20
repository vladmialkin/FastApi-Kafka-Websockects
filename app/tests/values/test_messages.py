from datetime import datetime
import pytest
from faker import Faker

from app.domain.entities.messages import Message, Chat
from app.domain.events.messages import NewMessageReceivedEvent
from app.domain.exceptions.messages import TitleTooLongException
from app.domain.values.messages import Text, Title

faker = Faker()
def test_create_message_success_short_text():
    text = Text(faker.text(max_nb_chars=20))
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_message_success_long_text():
    text = Text(faker.text())
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title(faker.text())
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        Title(faker.text()*10)


def test_add_chat_to_message():
    text = Text(faker.text())
    message = Message(text=text)

    title = Title(faker.text())
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages

def test_new_message_events():
    text = Text(faker.text())
    message = Message(text=text)

    title = Title(faker.text())
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == chat.oid



