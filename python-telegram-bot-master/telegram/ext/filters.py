#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2020
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
# pylint: disable=C0112, C0103, W0221
"""This module contains the Filters for use with the MessageHandler class."""

import re
import warnings

from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, FrozenSet, List, Match, Optional, Pattern, Set, Union, cast

from telegram import Chat, Message, MessageEntity, Update

__all__ = [
    'Filters',
    'BaseFilter',
    'MessageFilter',
    'UpdateFilter',
    'InvertedFilter',
    'MergedFilter',
]

from telegram.utils.deprecate import TelegramDeprecationWarning


class BaseFilter(ABC):
    """Base class for all Filters.

    Filters subclassing from this class can combined using bitwise operators:

    And:

        >>> (Filters.text & Filters.entity(MENTION))

    Or:

        >>> (Filters.audio | Filters.video)

    Not:

        >>> ~ Filters.command

    Also works with more than two filters:

        >>> (Filters.text & (Filters.entity(URL) | Filters.entity(TEXT_LINK)))
        >>> Filters.text & (~ Filters.forwarded)

    Note:
        Filters use the same short circuiting logic as python's `and`, `or` and `not`.
        This means that for example:

            >>> Filters.regex(r'(a?x)') | Filters.regex(r'(b?x)')

        With ``message.text == x``, will only ever return the matches for the first filter,
        since the second one is never evaluated.


    If you want to create your own filters create a class inheriting from either
    :class:`MessageFilter` or :class:`UpdateFilter` and implement a :meth:``filter`` method that
    returns a boolean: :obj:`True` if the message should be
    handled, :obj:`False` otherwise.
    Note that the filters work only as class instances, not
    actual class objects (so remember to
    initialize your filter classes).

    By default the filters name (what will get printed when converted to a string for display)
    will be the class name. If you want to overwrite this assign a better name to the :attr:`name`
    class variable.

    Attributes:
        name (:obj:`str`): Name for this filter. Defaults to the type of filter.
        data_filter (:obj:`bool`): Whether this filter is a data filter. A data filter should
            return a dict with lists. The dict will be merged with
            :class:`telegram.ext.CallbackContext`'s internal dict in most cases
            (depends on the handler).
    """

    name = None
    data_filter = False

    @abstractmethod
    def __call__(self, update: Update) -> Optional[Union[bool, Dict]]:
        pass

    def __and__(self, other: 'BaseFilter') -> 'BaseFilter':
        return MergedFilter(self, and_filter=other)

    def __or__(self, other: 'BaseFilter') -> 'BaseFilter':
        return MergedFilter(self, or_filter=other)

    def __invert__(self) -> 'BaseFilter':
        return InvertedFilter(self)

    def __repr__(self) -> str:
        # We do this here instead of in a __init__ so filter don't have to call __init__ or super()
        if self.name is None:
            self.name = self.__class__.__name__
        return self.name


class MessageFilter(BaseFilter, ABC):
    """Base class for all Message Filters. In contrast to :class:`UpdateFilter`, the object passed
    to :meth:`filter` is ``update.effective_message``.

    Please see :class:`telegram.ext.BaseFilter` for details on how to create custom filters.

    Attributes:
        name (:obj:`str`): Name for this filter. Defaults to the type of filter.
        data_filter (:obj:`bool`): Whether this filter is a data filter. A data filter should
            return a dict with lists. The dict will be merged with
            :class:`telegram.ext.CallbackContext`'s internal dict in most cases
            (depends on the handler).

    """

    def __call__(self, update: Update) -> Optional[Union[bool, Dict]]:
        return self.filter(update.effective_message)

    @abstractmethod
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        """This method must be overwritten.

        Args:
            message (:class:`telegram.Message`): The message that is tested.

        Returns:
            :obj:`dict` or :obj:`bool`

        """


class UpdateFilter(BaseFilter, ABC):
    """Base class for all Update Filters. In contrast to :class:`UpdateFilter`, the object
    passed to :meth:`filter` is ``update``, which allows to create filters like
    :attr:`Filters.update.edited_message`.

    Please see :class:`telegram.ext.BaseFilter` for details on how to create custom filters.

    Attributes:
        name (:obj:`str`): Name for this filter. Defaults to the type of filter.
        data_filter (:obj:`bool`): Whether this filter is a data filter. A data filter should
            return a dict with lists. The dict will be merged with
            :class:`telegram.ext.CallbackContext`'s internal dict in most cases
            (depends on the handler).

    """

    def __call__(self, update: Update) -> Optional[Union[bool, Dict]]:
        return self.filter(update)

    @abstractmethod
    def filter(self, update: Update) -> Optional[Union[bool, Dict]]:
        """This method must be overwritten.

        Args:
            update (:class:`telegram.Update`): The update that is tested.

        Returns:
            :obj:`dict` or :obj:`bool`.

        """


class InvertedFilter(UpdateFilter):
    """Represents a filter that has been inverted.

    Args:
        f: The filter to invert.

    """

    def __init__(self, f: BaseFilter):
        self.f = f

    def filter(self, update: Update) -> bool:
        return not bool(self.f(update))

    def __repr__(self) -> str:
        return "<inverted {}>".format(self.f)


class MergedFilter(UpdateFilter):
    """Represents a filter consisting of two other filters.

    Args:
        base_filter: Filter 1 of the merged filter.
        and_filter: Optional filter to "and" with base_filter. Mutually exclusive with or_filter.
        or_filter: Optional filter to "or" with base_filter. Mutually exclusive with and_filter.

    """

    def __init__(
        self, base_filter: BaseFilter, and_filter: BaseFilter = None, or_filter: BaseFilter = None
    ):
        self.base_filter = base_filter
        if self.base_filter.data_filter:
            self.data_filter = True
        self.and_filter = and_filter
        if (
            self.and_filter
            and not isinstance(self.and_filter, bool)
            and self.and_filter.data_filter
        ):
            self.data_filter = True
        self.or_filter = or_filter
        if self.or_filter and not isinstance(self.and_filter, bool) and self.or_filter.data_filter:
            self.data_filter = True

    @staticmethod
    def _merge(base_output: Union[bool, Dict], comp_output: Union[bool, Dict]) -> Dict:
        base = base_output if isinstance(base_output, dict) else {}
        comp = comp_output if isinstance(comp_output, dict) else {}
        for k in comp.keys():
            # Make sure comp values are lists
            comp_value = comp[k] if isinstance(comp[k], list) else []
            try:
                # If base is a list then merge
                if isinstance(base[k], list):
                    base[k] += comp_value
                else:
                    base[k] = [base[k]] + comp_value
            except KeyError:
                base[k] = comp_value
        return base

    def filter(self, update: Update) -> Union[bool, Dict]:  # pylint: disable=R0911
        base_output = self.base_filter(update)
        # We need to check if the filters are data filters and if so return the merged data.
        # If it's not a data filter or an or_filter but no matches return bool
        if self.and_filter:
            # And filter needs to short circuit if base is falsey
            if base_output:
                comp_output = self.and_filter(update)
                if comp_output:
                    if self.data_filter:
                        merged = self._merge(base_output, comp_output)
                        if merged:
                            return merged
                    return True
        elif self.or_filter:
            # Or filter needs to short circuit if base is truthey
            if base_output:
                if self.data_filter:
                    return base_output
                return True

            comp_output = self.or_filter(update)
            if comp_output:
                if self.data_filter:
                    return comp_output
                return True
        return False

    def __repr__(self) -> str:
        return "<{} {} {}>".format(
            self.base_filter, "and" if self.and_filter else "or", self.and_filter or self.or_filter
        )


class _DiceEmoji(MessageFilter):
    def __init__(self, emoji: str = None, name: str = None):
        self.name = 'Filters.dice.{}'.format(name) if name else 'Filters.dice'
        self.emoji = emoji

    class _DiceValues(MessageFilter):
        def __init__(self, values: Union[int, List[int]], name: str, emoji: str = None):
            self.values = [values] if isinstance(values, int) else values
            self.emoji = emoji
            self.name = '{}({})'.format(name, values)

        def filter(self, message: Message) -> bool:
            if message.dice and message.dice.value in self.values:
                if self.emoji:
                    return message.dice.emoji == self.emoji
                return True
            return False

    def __call__(  # type: ignore[override]
        self, update: Union[Update, List[int]]
    ) -> Union[bool, '_DiceValues']:
        if isinstance(update, Update):
            return self.filter(update.effective_message)
        return self._DiceValues(update, self.name, emoji=self.emoji)

    def filter(self, message: Message) -> bool:
        if bool(message.dice):
            if self.emoji:
                return message.dice.emoji == self.emoji
            return True
        return False


class Filters:
    """Predefined filters for use as the ``filter`` argument of
    :class:`telegram.ext.MessageHandler`.

    Examples:
        Use ``MessageHandler(Filters.video, callback_method)`` to filter all video
        messages. Use ``MessageHandler(Filters.contact, callback_method)`` for all contacts. etc.

    """

    class _All(MessageFilter):
        name = 'Filters.all'

        def filter(self, message: Message) -> bool:
            return True

    all = _All()
    """All Messages."""

    class _Text(MessageFilter):
        name = 'Filters.text'

        class _TextStrings(MessageFilter):
            def __init__(self, strings: List[str]):
                self.strings = strings
                self.name = 'Filters.text({})'.format(strings)

            def filter(self, message: Message) -> bool:
                if message.text:
                    return message.text in self.strings
                return False

        def __call__(  # type: ignore[override]
            self, update: Union[Update, List[str]]
        ) -> Union[bool, '_TextStrings']:
            if isinstance(update, Update):
                return self.filter(update.effective_message)
            return self._TextStrings(update)

        def filter(self, message: Message) -> bool:
            return bool(message.text)

    text = _Text()
    """Text Messages. If a list of strings is passed, it filters messages to only allow those
    whose text is appearing in the given list.

    Examples:
        To allow any text message, simply use
        ``MessageHandler(Filters.text, callback_method)``.

        A simple use case for passing a list is to allow only messages that were sent by a
        custom :class:`telegram.ReplyKeyboardMarkup`::

            buttons = ['Start', 'Settings', 'Back']
            markup = ReplyKeyboardMarkup.from_column(buttons)
            ...
            MessageHandler(Filters.text(buttons), callback_method)

    Note:
        * Dice messages don't have text. If you want to filter either text or dice messages, use
          ``Filters.text | Filters.dice``.
        * Messages containing a command are accepted by this filter. Use
          ``Filters.text & (~Filters.command)``, if you want to filter only text messages without
          commands.

    Args:
        update (List[:obj:`str`] | Tuple[:obj:`str`], optional): Which messages to allow. Only
            exact matches are allowed. If not specified, will allow any text message.
    """

    class _Caption(MessageFilter):
        name = 'Filters.caption'

        class _CaptionStrings(MessageFilter):
            def __init__(self, strings: List[str]):
                self.strings = strings
                self.name = 'Filters.caption({})'.format(strings)

            def filter(self, message: Message) -> bool:
                if message.caption:
                    return message.caption in self.strings
                return False

        def __call__(  # type: ignore[override]
            self, update: Union[Update, List[str]]
        ) -> Union[bool, '_CaptionStrings']:
            if isinstance(update, Update):
                return self.filter(update.effective_message)
            return self._CaptionStrings(update)

        def filter(self, message: Message) -> bool:
            return bool(message.caption)

    caption = _Caption()
    """Messages with a caption. If a list of strings is passed, it filters messages to only
    allow those whose caption is appearing in the given list.

    Examples:
        ``MessageHandler(Filters.caption, callback_method)``

    Args:
        update (List[:obj:`str`] | Tuple[:obj:`str`], optional): Which captions to allow. Only
            exact matches are allowed. If not specified, will allow any message with a caption.
    """

    class _Command(MessageFilter):
        name = 'Filters.command'

        class _CommandOnlyStart(MessageFilter):
            def __init__(self, only_start: bool):
                self.only_start = only_start
                self.name = 'Filters.command({})'.format(only_start)

            def filter(self, message: Message) -> bool:
                return bool(
                    message.entities
                    and any([e.type == MessageEntity.BOT_COMMAND for e in message.entities])
                )

        def __call__(  # type: ignore[override]
            self, update: Union[bool, Update]
        ) -> Union[bool, '_CommandOnlyStart']:
            if isinstance(update, Update):
                return self.filter(update.effective_message)
            return self._CommandOnlyStart(update)

        def filter(self, message: Message) -> bool:
            return bool(
                message.entities
                and message.entities[0].type == MessageEntity.BOT_COMMAND
                and message.entities[0].offset == 0
            )

    command = _Command()
    """
    Messages with a :attr:`telegram.MessageEntity.BOT_COMMAND`. By default only allows
    messages `starting` with a bot command. Pass :obj:`False` to also allow messages that contain a
    bot command `anywhere` in the text.

    Examples::

        MessageHandler(Filters.command, command_at_start_callback)
        MessageHandler(Filters.command(False), command_anywhere_callback)

    Note:
        ``Filters.text`` also accepts messages containing a command.

    Args:
        update (:obj:`bool`, optional): Whether to only allow messages that `start` with a bot
            command. Defaults to :obj:`True`.
    """

    class regex(MessageFilter):
        """
        Filters updates by searching for an occurrence of ``pattern`` in the message text.
        The ``re.search()`` function is used to determine whether an update should be filtered.

        Refer to the documentation of the ``re`` module for more information.

        To get the groups and groupdict matched, see :attr:`telegram.ext.CallbackContext.matches`.

        Examples:
            Use ``MessageHandler(Filters.regex(r'help'), callback)`` to capture all messages that
            contain the word 'help'. You can also use
            ``MessageHandler(Filters.regex(re.compile(r'help', re.IGNORECASE)), callback)`` if
            you want your pattern to be case insensitive. This approach is recommended
            if you need to specify flags on your pattern.

        Note:
            Filters use the same short circuiting logic as python's `and`, `or` and `not`.
            This means that for example:

                >>> Filters.regex(r'(a?x)') | Filters.regex(r'(b?x)')

            With a message.text of `x`, will only ever return the matches for the first filter,
            since the second one is never evaluated.

        Args:
            pattern (:obj:`str` | :obj:`Pattern`): The regex pattern.
        """

        data_filter = True

        def __init__(self, pattern: Union[str, Pattern]):
            if isinstance(pattern, str):
                pattern = re.compile(pattern)
            pattern = cast(Pattern, pattern)
            self.pattern: Pattern = pattern
            self.name = 'Filters.regex({})'.format(self.pattern)

        def filter(self, message: Message) -> Optional[Dict[str, List[Match]]]:
            """"""  # remove method from docs
            if message.text:
                match = self.pattern.search(message.text)
                if match:
                    return {'matches': [match]}
            return {}

    class _Reply(MessageFilter):
        name = 'Filters.reply'

        def filter(self, message: Message) -> bool:
            return bool(message.reply_to_message)

    reply = _Reply()
    """Messages that are a reply to another message."""

    class _Audio(MessageFilter):
        name = 'Filters.audio'

        def filter(self, message: Message) -> bool:
            return bool(message.audio)

    audio = _Audio()
    """Messages that contain :class:`telegram.Audio`."""

    class _Document(MessageFilter):
        name = 'Filters.document'

        class category(MessageFilter):
            """Filters documents by their category in the mime-type attribute.

            Note:
                This Filter only filters by the mime_type of the document,
                    it doesn't check the validity of the document.
                The user can manipulate the mime-type of a message and
                    send media with wrong types that don't fit to this handler.

            Example:
                Filters.documents.category('audio/') returns :obj:`True` for all types
                of audio sent as file, for example 'audio/mpeg' or 'audio/x-wav'.
            """

            def __init__(self, category: Optional[str]):
                """Initialize the category you want to filter

                Args:
                    category (str, optional): category of the media you want to filter"""
                self.category = category
                self.name = "Filters.document.category('{}')".format(self.category)

            def filter(self, message: Message) -> bool:
                """"""  # remove method from docs
                if message.document:
                    return message.document.mime_type.startswith(self.category)
                return False

        application = category('application/')
        audio = category('audio/')
        image = category('image/')
        video = category('video/')
        text = category('text/')

        class mime_type(MessageFilter):
            """This Filter filters documents by their mime-type attribute

            Note:
                This Filter only filters by the mime_type of the document,
                    it doesn't check the validity of document.
                The user can manipulate the mime-type of a message and
                    send media with wrong types that don't fit to this handler.

            Example:
                ``Filters.documents.mime_type('audio/mpeg')`` filters all audio in mp3 format.
            """

            def __init__(self, mimetype: Optional[str]):
                """Initialize the category you want to filter

                Args:
                    mimetype (str, optional): mime_type of the media you want to filter"""
                self.mimetype = mimetype
                self.name = "Filters.document.mime_type('{}')".format(self.mimetype)

            def filter(self, message: Message) -> bool:
                """"""  # remove method from docs
                if message.document:
                    return message.document.mime_type == self.mimetype
                return False

        apk = mime_type('application/vnd.android.package-archive')
        doc = mime_type('application/msword')
        docx = mime_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        exe = mime_type('application/x-ms-dos-executable')
        gif = mime_type('video/mp4')
        jpg = mime_type('image/jpeg')
        mp3 = mime_type('audio/mpeg')
        pdf = mime_type('application/pdf')
        py = mime_type('text/x-python')
        svg = mime_type('image/svg+xml')
        txt = mime_type('text/plain')
        targz = mime_type('application/x-compressed-tar')
        wav = mime_type('audio/x-wav')
        xml = mime_type('application/xml')
        zip = mime_type('application/zip')

        def filter(self, message: Message) -> bool:
            return bool(message.document)

    document = _Document()
    """
    Subset for messages containing a document/file.

    Examples:
        Use these filters like: ``Filters.document.mp3``,
        ``Filters.document.mime_type("text/plain")`` etc. Or use just
        ``Filters.document`` for all document messages.

    Attributes:
        category: Filters documents by their category in the mime-type attribute

            Note:
                This Filter only filters by the mime_type of the document,
                it doesn't check the validity of the document.
                The user can manipulate the mime-type of a message and
                send media with wrong types that don't fit to this handler.

            Example:
                ``Filters.documents.category('audio/')`` filters all types
                of audio sent as file, for example 'audio/mpeg' or 'audio/x-wav'.
        application: Same as ``Filters.document.category("application")``.
        audio: Same as ``Filters.document.category("audio")``.
        image: Same as ``Filters.document.category("image")``.
        video: Same as ``Filters.document.category("video")``.
        text: Same as ``Filters.document.category("text")``.
        mime_type: Filters documents by their mime-type attribute

            Note:
                This Filter only filters by the mime_type of the document,
                it doesn't check the validity of document.

                The user can manipulate the mime-type of a message and
                send media with wrong types that don't fit to this handler.

            Example:
                ``Filters.documents.mime_type('audio/mpeg')`` filters all audio in mp3 format.
        apk: Same as ``Filters.document.mime_type("application/vnd.android.package-archive")``-
        doc: Same as ``Filters.document.mime_type("application/msword")``-
        docx: Same as ``Filters.document.mime_type("application/vnd.openxmlformats-\
officedocument.wordprocessingml.document")``-
        exe: Same as ``Filters.document.mime_type("application/x-ms-dos-executable")``-
        gif: Same as ``Filters.document.mime_type("video/mp4")``-
        jpg: Same as ``Filters.document.mime_type("image/jpeg")``-
        mp3: Same as ``Filters.document.mime_type("audio/mpeg")``-
        pdf: Same as ``Filters.document.mime_type("application/pdf")``-
        py: Same as ``Filters.document.mime_type("text/x-python")``-
        svg: Same as ``Filters.document.mime_type("image/svg+xml")``-
        txt: Same as ``Filters.document.mime_type("text/plain")``-
        targz: Same as ``Filters.document.mime_type("application/x-compressed-tar")``-
        wav: Same as ``Filters.document.mime_type("audio/x-wav")``-
        xml: Same as ``Filters.document.mime_type("application/xml")``-
        zip: Same as ``Filters.document.mime_type("application/zip")``-
    """

    class _Animation(MessageFilter):
        name = 'Filters.animation'

        def filter(self, message: Message) -> bool:
            return bool(message.animation)

    animation = _Animation()
    """Messages that contain :class:`telegram.Animation`."""

    class _Photo(MessageFilter):
        name = 'Filters.photo'

        def filter(self, message: Message) -> bool:
            return bool(message.photo)

    photo = _Photo()
    """Messages that contain :class:`telegram.PhotoSize`."""

    class _Sticker(MessageFilter):
        name = 'Filters.sticker'

        def filter(self, message: Message) -> bool:
            return bool(message.sticker)

    sticker = _Sticker()
    """Messages that contain :class:`telegram.Sticker`."""

    class _Video(MessageFilter):
        name = 'Filters.video'

        def filter(self, message: Message) -> bool:
            return bool(message.video)

    video = _Video()
    """Messages that contain :class:`telegram.Video`."""

    class _Voice(MessageFilter):
        name = 'Filters.voice'

        def filter(self, message: Message) -> bool:
            return bool(message.voice)

    voice = _Voice()
    """Messages that contain :class:`telegram.Voice`."""

    class _VideoNote(MessageFilter):
        name = 'Filters.video_note'

        def filter(self, message: Message) -> bool:
            return bool(message.video_note)

    video_note = _VideoNote()
    """Messages that contain :class:`telegram.VideoNote`."""

    class _Contact(MessageFilter):
        name = 'Filters.contact'

        def filter(self, message: Message) -> bool:
            return bool(message.contact)

    contact = _Contact()
    """Messages that contain :class:`telegram.Contact`."""

    class _Location(MessageFilter):
        name = 'Filters.location'

        def filter(self, message: Message) -> bool:
            return bool(message.location)

    location = _Location()
    """Messages that contain :class:`telegram.Location`."""

    class _Venue(MessageFilter):
        name = 'Filters.venue'

        def filter(self, message: Message) -> bool:
            return bool(message.venue)

    venue = _Venue()
    """Messages that contain :class:`telegram.Venue`."""

    class _StatusUpdate(UpdateFilter):
        """Subset for messages containing a status update.

        Examples:
            Use these filters like: ``Filters.status_update.new_chat_members`` etc. Or use just
            ``Filters.status_update`` for all status update messages.

        """

        class _NewChatMembers(MessageFilter):
            name = 'Filters.status_update.new_chat_members'

            def filter(self, message: Message) -> bool:
                return bool(message.new_chat_members)

        new_chat_members = _NewChatMembers()
        """Messages that contain :attr:`telegram.Message.new_chat_members`."""

        class _LeftChatMember(MessageFilter):
            name = 'Filters.status_update.left_chat_member'

            def filter(self, message: Message) -> bool:
                return bool(message.left_chat_member)

        left_chat_member = _LeftChatMember()
        """Messages that contain :attr:`telegram.Message.left_chat_member`."""

        class _NewChatTitle(MessageFilter):
            name = 'Filters.status_update.new_chat_title'

            def filter(self, message: Message) -> bool:
                return bool(message.new_chat_title)

        new_chat_title = _NewChatTitle()
        """Messages that contain :attr:`telegram.Message.new_chat_title`."""

        class _NewChatPhoto(MessageFilter):
            name = 'Filters.status_update.new_chat_photo'

            def filter(self, message: Message) -> bool:
                return bool(message.new_chat_photo)

        new_chat_photo = _NewChatPhoto()
        """Messages that contain :attr:`telegram.Message.new_chat_photo`."""

        class _DeleteChatPhoto(MessageFilter):
            name = 'Filters.status_update.delete_chat_photo'

            def filter(self, message: Message) -> bool:
                return bool(message.delete_chat_photo)

        delete_chat_photo = _DeleteChatPhoto()
        """Messages that contain :attr:`telegram.Message.delete_chat_photo`."""

        class _ChatCreated(MessageFilter):
            name = 'Filters.status_update.chat_created'

            def filter(self, message: Message) -> bool:
                return bool(
                    message.group_chat_created
                    or message.supergroup_chat_created
                    or message.channel_chat_created
                )

        chat_created = _ChatCreated()
        """Messages that contain :attr:`telegram.Message.group_chat_created`,
            :attr: `telegram.Message.supergroup_chat_created` or
            :attr: `telegram.Message.channel_chat_created`."""

        class _Migrate(MessageFilter):
            name = 'Filters.status_update.migrate'

            def filter(self, message: Message) -> bool:
                return bool(message.migrate_from_chat_id or message.migrate_to_chat_id)

        migrate = _Migrate()
        """Messages that contain :attr:`telegram.Message.migrate_from_chat_id` or
            :attr:`telegram.Message.migrate_to_chat_id`."""

        class _PinnedMessage(MessageFilter):
            name = 'Filters.status_update.pinned_message'

            def filter(self, message: Message) -> bool:
                return bool(message.pinned_message)

        pinned_message = _PinnedMessage()
        """Messages that contain :attr:`telegram.Message.pinned_message`."""

        class _ConnectedWebsite(MessageFilter):
            name = 'Filters.status_update.connected_website'

            def filter(self, message: Message) -> bool:
                return bool(message.connected_website)

        connected_website = _ConnectedWebsite()
        """Messages that contain :attr:`telegram.Message.connected_website`."""

        name = 'Filters.status_update'

        def filter(self, message: Update) -> bool:
            return bool(
                self.new_chat_members(message)
                or self.left_chat_member(message)
                or self.new_chat_title(message)
                or self.new_chat_photo(message)
                or self.delete_chat_photo(message)
                or self.chat_created(message)
                or self.migrate(message)
                or self.pinned_message(message)
                or self.connected_website(message)
            )

    status_update = _StatusUpdate()
    """Subset for messages containing a status update.

    Examples:
        Use these filters like: ``Filters.status_update.new_chat_members`` etc. Or use just
        ``Filters.status_update`` for all status update messages.

    Attributes:
        chat_created: Messages that contain
            :attr:`telegram.Message.group_chat_created`,
            :attr:`telegram.Message.supergroup_chat_created` or
            :attr:`telegram.Message.channel_chat_created`.
        delete_chat_photo: Messages that contain
            :attr:`telegram.Message.delete_chat_photo`.
        left_chat_member: Messages that contain
            :attr:`telegram.Message.left_chat_member`.
        migrate: Messages that contain
            :attr:`telegram.Message.migrate_from_chat_id` or
            :attr: `telegram.Message.migrate_from_chat_id`.
        new_chat_members: Messages that contain
            :attr:`telegram.Message.new_chat_members`.
        new_chat_photo: Messages that contain
            :attr:`telegram.Message.new_chat_photo`.
        new_chat_title: Messages that contain
            :attr:`telegram.Message.new_chat_title`.
        pinned_message: Messages that contain
            :attr:`telegram.Message.pinned_message`.
    """

    class _Forwarded(MessageFilter):
        name = 'Filters.forwarded'

        def filter(self, message: Message) -> bool:
            return bool(message.forward_date)

    forwarded = _Forwarded()
    """Messages that are forwarded."""

    class _Game(MessageFilter):
        name = 'Filters.game'

        def filter(self, message: Message) -> bool:
            return bool(message.game)

    game = _Game()
    """Messages that contain :class:`telegram.Game`."""

    class entity(MessageFilter):
        """
        Filters messages to only allow those which have a :class:`telegram.MessageEntity`
        where their `type` matches `entity_type`.

        Examples:
            Example ``MessageHandler(Filters.entity("hashtag"), callback_method)``

        Args:
            entity_type: Entity type to check for. All types can be found as constants
                in :class:`telegram.MessageEntity`.

        """

        def __init__(self, entity_type: str):
            self.entity_type = entity_type
            self.name = 'Filters.entity({})'.format(self.entity_type)

        def filter(self, message: Message) -> bool:
            """"""  # remove method from docs
            return any(entity.type == self.entity_type for entity in message.entities)

    class caption_entity(MessageFilter):
        """
        Filters media messages to only allow those which have a :class:`telegram.MessageEntity`
        where their `type` matches `entity_type`.

        Examples:
            Example ``MessageHandler(Filters.caption_entity("hashtag"), callback_method)``

        Args:
            entity_type: Caption Entity type to check for. All types can be found as constants
                in :class:`telegram.MessageEntity`.

        """

        def __init__(self, entity_type: str):
            self.entity_type = entity_type
            self.name = 'Filters.caption_entity({})'.format(self.entity_type)

        def filter(self, message: Message) -> bool:
            """"""  # remove method from docs
            return any(entity.type == self.entity_type for entity in message.caption_entities)

    class _Private(MessageFilter):
        name = 'Filters.private'

        def filter(self, message: Message) -> bool:
            warnings.warn(
                'Filters.private is deprecated. Use Filters.chat_type.private instead.',
                TelegramDeprecationWarning,
                stacklevel=2,
            )
            return message.chat.type == Chat.PRIVATE

    private = _Private()
    """
    Messages sent in a private chat.

    Note:
        DEPRECATED. Use
        :attr:`telegram.ext.Filters.chat_type.private` instead.
    """

    class _Group(MessageFilter):
        name = 'Filters.group'

        def filter(self, message: Message) -> bool:
            warnings.warn(
                'Filters.group is deprecated. Use Filters.chat_type.groups instead.',
                TelegramDeprecationWarning,
                stacklevel=2,
            )
            return message.chat.type in [Chat.GROUP, Chat.SUPERGROUP]

    group = _Group()
    """
    Messages sent in a group or a supergroup chat.

    Note:
        DEPRECATED. Use
        :attr:`telegram.ext.Filters.chat_type.groups` instead.
    """

    class _ChatType(MessageFilter):
        name = 'Filters.chat_type'

        class _Channel(MessageFilter):
            name = 'Filters.chat_type.channel'

            def filter(self, message: Message) -> bool:
                return message.chat.type == Chat.CHANNEL

        channel = _Channel()

        class _Group(MessageFilter):
            name = 'Filters.chat_type.group'

            def filter(self, message: Message) -> bool:
                return message.chat.type == Chat.GROUP

        group = _Group()

        class _SuperGroup(MessageFilter):
            name = 'Filters.chat_type.supergroup'

            def filter(self, message: Message) -> bool:
                return message.chat.type == Chat.SUPERGROUP

        supergroup = _SuperGroup()

        class _Groups(MessageFilter):
            name = 'Filters.chat_type.groups'

            def filter(self, message: Message) -> bool:
                return message.chat.type in [Chat.GROUP, Chat.SUPERGROUP]

        groups = _Groups()

        class _Private(MessageFilter):
            name = 'Filters.chat_type.private'

            def filter(self, message: Message) -> bool:
                return message.chat.type == Chat.PRIVATE

        private = _Private()

        def filter(self, message: Message) -> bool:
            return bool(message.chat.type)

    chat_type = _ChatType()
    """Subset for filtering the type of chat.

    Examples:
        Use these filters like: ``Filters.chat_type.channel`` or
        ``Filters.chat_type.supergroup`` etc. Or use just ``Filters.chat_type`` for all
        chat types.

    Attributes:
        channel: Updates from channel
        group: Updates from group
        supergroup: Updates from supergroup
        groups: Updates from group *or* supergroup
        private: Updates sent in private chat
    """

    class user(MessageFilter):
        """Filters messages to allow only those which are from specified user ID(s) or
        username(s).

        Examples:
            ``MessageHandler(Filters.user(1234), callback_method)``

        Warning:
            :attr:`user_ids` will give a *copy* of the saved user ids as :class:`frozenset`. This
            is to ensure thread safety. To add/remove a user, you should use :meth:`add_usernames`,
            :meth:`add_user_ids`, :meth:`remove_usernames` and :meth:`remove_user_ids`. Only update
            the entire set by ``filter.user_ids/usernames = new_set``, if you are entirely sure
            that it is not causing race conditions, as this will complete replace the current set
            of allowed users.

        Attributes:
            user_ids(set(:obj:`int`), optional): Which user ID(s) to allow through.
            usernames(set(:obj:`str`), optional): Which username(s) (without leading '@') to allow
                through.
            allow_empty(:obj:`bool`, optional): Whether updates should be processed, if no user
                is specified in :attr:`user_ids` and :attr:`usernames`.

        Args:
            user_id(:obj:`int` | List[:obj:`int`], optional): Which user ID(s) to allow
                through.
            username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to allow
                through. Leading '@'s in usernames will be discarded.
            allow_empty(:obj:`bool`, optional): Whether updates should be processed, if no user
                is specified in :attr:`user_ids` and :attr:`usernames`. Defaults to :obj:`False`

        Raises:
            RuntimeError: If user_id and username are both present.

        """

        def __init__(
            self,
            user_id: Union[int, List[int]] = None,
            username: Union[str, List[str]] = None,
            allow_empty: bool = False,
        ):
            self.allow_empty = allow_empty
            self.__lock = Lock()

            self._user_ids: Set[int] = set()
            self._usernames: Set[str] = set()

            self._set_user_ids(user_id)
            self._set_usernames(username)

        @staticmethod
        def _parse_user_id(user_id: Union[int, List[int]]) -> Set[int]:
            if user_id is None:
                return set()
            if isinstance(user_id, int):
                return {user_id}
            return set(user_id)

        @staticmethod
        def _parse_username(username: Union[str, List[str]]) -> Set[str]:
            if username is None:
                return set()
            if isinstance(username, str):
                return {username[1:] if username.startswith('@') else username}
            return {user[1:] if user.startswith('@') else user for user in username}

        def _set_user_ids(self, user_id: Union[int, List[int]]) -> None:
            with self.__lock:
                if user_id and self._usernames:
                    raise RuntimeError(
                        "Can't set user_id in conjunction with (already set) " "usernames."
                    )
                self._user_ids = self._parse_user_id(user_id)

        def _set_usernames(self, username: Union[str, List[str]]) -> None:
            with self.__lock:
                if username and self._user_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "user_ids."
                    )
                self._usernames = self._parse_username(username)

        @property
        def user_ids(self) -> FrozenSet[int]:
            with self.__lock:
                return frozenset(self._user_ids)

        @user_ids.setter
        def user_ids(self, user_id: Union[int, List[int]]) -> None:
            self._set_user_ids(user_id)

        @property
        def usernames(self) -> FrozenSet[str]:
            with self.__lock:
                return frozenset(self._usernames)

        @usernames.setter
        def usernames(self, username: Union[str, List[str]]) -> None:
            self._set_usernames(username)

        def add_usernames(self, username: Union[str, List[str]]) -> None:
            """
            Add one or more users to the allowed usernames.

            Args:
                username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to allow
                    through. Leading '@'s in usernames will be discarded.
            """
            with self.__lock:
                if self._user_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "user_ids."
                    )

                parsed_username = self._parse_username(username)
                self._usernames |= parsed_username

        def add_user_ids(self, user_id: Union[int, List[int]]) -> None:
            """
            Add one or more users to the allowed user ids.

            Args:
                user_id(:obj:`int` | List[:obj:`int`], optional): Which user ID(s) to allow
                    through.
            """
            with self.__lock:
                if self._usernames:
                    raise RuntimeError(
                        "Can't set user_id in conjunction with (already set) " "usernames."
                    )

                parsed_user_id = self._parse_user_id(user_id)

                self._user_ids |= parsed_user_id

        def remove_usernames(self, username: Union[str, List[str]]) -> None:
            """
            Remove one or more users from allowed usernames.

            Args:
                username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to disallow
                    through. Leading '@'s in usernames will be discarded.
            """
            with self.__lock:
                if self._user_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "user_ids."
                    )

                parsed_username = self._parse_username(username)
                self._usernames -= parsed_username

        def remove_user_ids(self, user_id: Union[int, List[int]]) -> None:
            """
            Remove one or more users from allowed user ids.

            Args:
                user_id(:obj:`int` | List[:obj:`int`], optional): Which user ID(s) to disallow
                    through.
            """
            with self.__lock:
                if self._usernames:
                    raise RuntimeError(
                        "Can't set user_id in conjunction with (already set) " "usernames."
                    )
                parsed_user_id = self._parse_user_id(user_id)
                self._user_ids -= parsed_user_id

        def filter(self, message: Message) -> bool:
            """"""  # remove method from docs
            if message.from_user:
                if self.user_ids:
                    return message.from_user.id in self.user_ids
                if self.usernames:
                    return bool(
                        message.from_user.username and message.from_user.username in self.usernames
                    )
                return self.allow_empty
            return False

    class via_bot(MessageFilter):
        """Filters messages to allow only those which are from specified via_bot ID(s) or
        username(s).

        Examples:
            ``MessageHandler(Filters.via_bot(1234), callback_method)``

        Warning:
            :attr:`bot_ids` will give a *copy* of the saved bot ids as :class:`frozenset`. This
            is to ensure thread safety. To add/remove a bot, you should use :meth:`add_usernames`,
            :meth:`add_bot_ids`, :meth:`remove_usernames` and :meth:`remove_bot_ids`. Only update
            the entire set by ``filter.bot_ids/usernames = new_set``, if you are entirely sure
            that it is not causing race conditions, as this will complete replace the current set
            of allowed bots.

        Attributes:
            bot_ids(set(:obj:`int`), optional): Which bot ID(s) to allow through.
            usernames(set(:obj:`str`), optional): Which username(s) (without leading '@') to allow
                through.
            allow_empty(:obj:`bool`, optional): Whether updates should be processed, if no bot
                is specified in :attr:`bot_ids` and :attr:`usernames`.

        Args:
            bot_id(:obj:`int` | List[:obj:`int`], optional): Which bot ID(s) to allow
                through.
            username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to allow
                through. Leading '@'s in usernames will be discarded.
            allow_empty(:obj:`bool`, optional): Whether updates should be processed, if no user
                is specified in :attr:`bot_ids` and :attr:`usernames`. Defaults to :obj:`False`

        Raises:
            RuntimeError: If bot_id and username are both present.
        """

        def __init__(
            self,
            bot_id: Union[int, List[int]] = None,
            username: Union[str, List[str]] = None,
            allow_empty: bool = False,
        ):
            self.allow_empty = allow_empty
            self.__lock = Lock()

            self._bot_ids: Set[int] = set()
            self._usernames: Set[str] = set()

            self._set_bot_ids(bot_id)
            self._set_usernames(username)

        @staticmethod
        def _parse_bot_id(bot_id: Union[int, List[int]]) -> Set[int]:
            if bot_id is None:
                return set()
            if isinstance(bot_id, int):
                return {bot_id}
            return set(bot_id)

        @staticmethod
        def _parse_username(username: Union[str, List[str]]) -> Set[str]:
            if username is None:
                return set()
            if isinstance(username, str):
                return {username[1:] if username.startswith('@') else username}
            return {bot[1:] if bot.startswith('@') else bot for bot in username}

        def _set_bot_ids(self, bot_id: Union[int, List[int]]) -> None:
            with self.__lock:
                if bot_id and self._usernames:
                    raise RuntimeError(
                        "Can't set bot_id in conjunction with (already set) " "usernames."
                    )
                self._bot_ids = self._parse_bot_id(bot_id)

        def _set_usernames(self, username: Union[str, List[str]]) -> None:
            with self.__lock:
                if username and self._bot_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "bot_ids."
                    )
                self._usernames = self._parse_username(username)

        @property
        def bot_ids(self) -> FrozenSet[int]:
            with self.__lock:
                return frozenset(self._bot_ids)

        @bot_ids.setter
        def bot_ids(self, bot_id: Union[int, List[int]]) -> None:
            self._set_bot_ids(bot_id)

        @property
        def usernames(self) -> FrozenSet[str]:
            with self.__lock:
                return frozenset(self._usernames)

        @usernames.setter
        def usernames(self, username: Union[str, List[str]]) -> None:
            self._set_usernames(username)

        def add_usernames(self, username: Union[str, List[str]]) -> None:
            """
            Add one or more users to the allowed usernames.

            Args:
                username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to allow
                    through. Leading '@'s in usernames will be discarded.
            """
            with self.__lock:
                if self._bot_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "bot_ids."
                    )

                parsed_username = self._parse_username(username)
                self._usernames |= parsed_username

        def add_bot_ids(self, bot_id: Union[int, List[int]]) -> None:
            """

            Add one or more users to the allowed user ids.

            Args:
                bot_id(:obj:`int` | List[:obj:`int`], optional): Which bot ID(s) to allow
                    through.
            """
            with self.__lock:
                if self._usernames:
                    raise RuntimeError(
                        "Can't set bot_id in conjunction with (already set) " "usernames."
                    )

                parsed_bot_id = self._parse_bot_id(bot_id)

                self._bot_ids |= parsed_bot_id

        def remove_usernames(self, username: Union[str, List[str]]) -> None:
            """
            Remove one or more users from allowed usernames.

            Args:
                username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to disallow
                    through. Leading '@'s in usernames will be discarded.
            """
            with self.__lock:
                if self._bot_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "bot_ids."
                    )

                parsed_username = self._parse_username(username)
                self._usernames -= parsed_username

        def remove_bot_ids(self, bot_id: Union[int, List[int]]) -> None:
            """
            Remove one or more users from allowed user ids.

            Args:
                bot_id(:obj:`int` | List[:obj:`int`], optional): Which bot ID(s) to disallow
                    through.
            """
            with self.__lock:
                if self._usernames:
                    raise RuntimeError(
                        "Can't set bot_id in conjunction with (already set) " "usernames."
                    )
                parsed_bot_id = self._parse_bot_id(bot_id)
                self._bot_ids -= parsed_bot_id

        def filter(self, message: Message) -> bool:
            """"""  # remove method from docs
            if message.via_bot:
                if self.bot_ids:
                    return message.via_bot.id in self.bot_ids
                if self.usernames:
                    return bool(
                        message.via_bot.username and message.via_bot.username in self.usernames
                    )
                return self.allow_empty
            return False

    class chat(MessageFilter):
        """Filters messages to allow only those which are from a specified chat ID or username.

        Examples:
            ``MessageHandler(Filters.chat(-1234), callback_method)``

        Warning:
            :attr:`chat_ids` will give a *copy* of the saved chat ids as :class:`frozenset`. This
            is to ensure thread safety. To add/remove a chat, you should use :meth:`add_usernames`,
            :meth:`add_chat_ids`, :meth:`remove_usernames` and :meth:`remove_chat_ids`. Only update
            the entire set by ``filter.chat_ids/usernames = new_set``, if you are entirely sure
            that it is not causing race conditions, as this will complete replace the current set
            of allowed chats.

        Attributes:
            chat_ids(set(:obj:`int`), optional): Which chat ID(s) to allow through.
            usernames(set(:obj:`str`), optional): Which username(s) (without leading '@') to allow
                through.
            allow_empty(:obj:`bool`, optional): Whether updates should be processed, if no chat
                is specified in :attr:`chat_ids` and :attr:`usernames`.

        Args:
            chat_id(:obj:`int` | List[:obj:`int`], optional): Which chat ID(s) to allow
                through.
            username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to allow
                through. Leading `'@'` s in usernames will be discarded.
            allow_empty(:obj:`bool`, optional): Whether updates should be processed, if no chat
                is specified in :attr:`chat_ids` and :attr:`usernames`. Defaults to :obj:`False`

        Raises:
            RuntimeError: If chat_id and username are both present.

        """

        def __init__(
            self,
            chat_id: Union[int, List[int]] = None,
            username: Union[str, List[str]] = None,
            allow_empty: bool = False,
        ):
            self.allow_empty = allow_empty
            self.__lock = Lock()

            self._chat_ids: Set[int] = set()
            self._usernames: Set[str] = set()

            self._set_chat_ids(chat_id)
            self._set_usernames(username)

        @staticmethod
        def _parse_chat_id(chat_id: Union[int, List[int]]) -> Set[int]:
            if chat_id is None:
                return set()
            if isinstance(chat_id, int):
                return {chat_id}
            return set(chat_id)

        @staticmethod
        def _parse_username(username: Union[str, List[str]]) -> Set[str]:
            if username is None:
                return set()
            if isinstance(username, str):
                return {username[1:] if username.startswith('@') else username}
            return {chat[1:] if chat.startswith('@') else chat for chat in username}

        def _set_chat_ids(self, chat_id: Union[int, List[int]]) -> None:
            with self.__lock:
                if chat_id and self._usernames:
                    raise RuntimeError(
                        "Can't set chat_id in conjunction with (already set) " "usernames."
                    )
                self._chat_ids = self._parse_chat_id(chat_id)

        def _set_usernames(self, username: Union[str, List[str]]) -> None:
            with self.__lock:
                if username and self._chat_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "chat_ids."
                    )
                self._usernames = self._parse_username(username)

        @property
        def chat_ids(self) -> FrozenSet[int]:
            with self.__lock:
                return frozenset(self._chat_ids)

        @chat_ids.setter
        def chat_ids(self, chat_id: Union[int, List[int]]) -> None:
            self._set_chat_ids(chat_id)

        @property
        def usernames(self) -> FrozenSet[str]:
            with self.__lock:
                return frozenset(self._usernames)

        @usernames.setter
        def usernames(self, username: Union[str, List[str]]) -> None:
            self._set_usernames(username)

        def add_usernames(self, username: Union[str, List[str]]) -> None:
            """
            Add one or more chats to the allowed usernames.

            Args:
                username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to allow
                    through. Leading `'@'` s in usernames will be discarded.
            """
            with self.__lock:
                if self._chat_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "chat_ids."
                    )

                parsed_username = self._parse_username(username)
                self._usernames |= parsed_username

        def add_chat_ids(self, chat_id: Union[int, List[int]]) -> None:
            """
            Add one or more chats to the allowed chat ids.

            Args:
                chat_id(:obj:`int` | List[:obj:`int`], optional): Which chat ID(s) to allow
                    through.
            """
            with self.__lock:
                if self._usernames:
                    raise RuntimeError(
                        "Can't set chat_id in conjunction with (already set) " "usernames."
                    )

                parsed_chat_id = self._parse_chat_id(chat_id)

                self._chat_ids |= parsed_chat_id

        def remove_usernames(self, username: Union[str, List[str]]) -> None:
            """
            Remove one or more chats from allowed usernames.

            Args:
                username(:obj:`str` | List[:obj:`str`], optional): Which username(s) to disallow
                    through. Leading '@'s in usernames will be discarded.
            """
            with self.__lock:
                if self._chat_ids:
                    raise RuntimeError(
                        "Can't set username in conjunction with (already set) " "chat_ids."
                    )

                parsed_username = self._parse_username(username)
                self._usernames -= parsed_username

        def remove_chat_ids(self, chat_id: Union[int, List[int]]) -> None:
            """
            Remove one or more chats from allowed chat ids.

            Args:
                chat_id(:obj:`int` | List[:obj:`int`], optional): Which chat ID(s) to disallow
                    through.
            """
            with self.__lock:
                if self._usernames:
                    raise RuntimeError(
                        "Can't set chat_id in conjunction with (already set) " "usernames."
                    )
                parsed_chat_id = self._parse_chat_id(chat_id)
                self._chat_ids -= parsed_chat_id

        def filter(self, message: Message) -> bool:
            """"""  # remove method from docs
            if message.chat:
                if self.chat_ids:
                    return message.chat.id in self.chat_ids
                if self.usernames:
                    return bool(message.chat.username and message.chat.username in self.usernames)
                return self.allow_empty
            return False

    class _Invoice(MessageFilter):
        name = 'Filters.invoice'

        def filter(self, message: Message) -> bool:
            return bool(message.invoice)

    invoice = _Invoice()
    """Messages that contain :class:`telegram.Invoice`."""

    class _SuccessfulPayment(MessageFilter):
        name = 'Filters.successful_payment'

        def filter(self, message: Message) -> bool:
            return bool(message.successful_payment)

    successful_payment = _SuccessfulPayment()
    """Messages that confirm a :class:`telegram.SuccessfulPayment`."""

    class _PassportData(MessageFilter):
        name = 'Filters.passport_data'

        def filter(self, message: Message) -> bool:
            return bool(message.passport_data)

    passport_data = _PassportData()
    """Messages that contain a :class:`telegram.PassportData`"""

    class _Poll(MessageFilter):
        name = 'Filters.poll'

        def filter(self, message: Message) -> bool:
            return bool(message.poll)

    poll = _Poll()
    """Messages that contain a :class:`telegram.Poll`."""

    class _Dice(_DiceEmoji):
        dice = _DiceEmoji('????', 'dice')
        darts = _DiceEmoji('????', 'darts')
        basketball = _DiceEmoji('????', 'basketball')

    dice = _Dice()
    """Dice Messages. If an integer or a list of integers is passed, it filters messages to only
    allow those whose dice value is appearing in the given list.

    Examples:
        To allow any dice message, simply use
        ``MessageHandler(Filters.dice, callback_method)``.
        To allow only dice with value 6, use
        ``MessageHandler(Filters.dice(6), callback_method)``.
        To allow only dice with value 5 `or` 6, use
        ``MessageHandler(Filters.dice([5, 6]), callback_method)``.

    Args:
        update (:obj:`int` | List[:obj:`int`], optional): Which values to allow. If not
            specified, will allow any dice message.

    Note:
        Dice messages don't have text. If you want to filter either text or dice messages, use
        ``Filters.text | Filters.dice``.

    Attributes:
        dice: Dice messages with the emoji ????. Passing a list of integers is supported just as for
            :attr:`Filters.dice`.
        darts: Dice messages with the emoji ????. Passing a list of integers is supported just as for
            :attr:`Filters.dice`.
        basketball: Dice messages with the emoji ????. Passing a list of integers is supported just
            as for :attr:`Filters.dice`.
    """

    class language(MessageFilter):
        """Filters messages to only allow those which are from users with a certain language code.

        Note:
            According to official Telegram API documentation, not every single user has the
            `language_code` attribute. Do not count on this filter working on all users.

        Examples:
            ``MessageHandler(Filters.language("en"), callback_method)``

        Args:
            lang (:obj:`str` | List[:obj:`str`]): Which language code(s) to allow through. This
                will be matched using ``.startswith`` meaning that 'en' will match both 'en_US'
                and 'en_GB'.

        """

        def __init__(self, lang: Union[str, List[str]]):
            if isinstance(lang, str):
                lang = cast(str, lang)
                self.lang = [lang]
            else:
                lang = cast(List[str], lang)
                self.lang = lang
            self.name = 'Filters.language({})'.format(self.lang)

        def filter(self, message: Message) -> bool:
            """"""  # remove method from docs
            return bool(
                message.from_user.language_code
                and any([message.from_user.language_code.startswith(x) for x in self.lang])
            )

    class _UpdateType(UpdateFilter):
        name = 'Filters.update'

        class _Message(UpdateFilter):
            name = 'Filters.update.message'

            def filter(self, update: Update) -> bool:
                return update.message is not None

        message = _Message()

        class _EditedMessage(UpdateFilter):
            name = 'Filters.update.edited_message'

            def filter(self, update: Update) -> bool:
                return update.edited_message is not None

        edited_message = _EditedMessage()

        class _Messages(UpdateFilter):
            name = 'Filters.update.messages'

            def filter(self, update: Update) -> bool:
                return update.message is not None or update.edited_message is not None

        messages = _Messages()

        class _ChannelPost(UpdateFilter):
            name = 'Filters.update.channel_post'

            def filter(self, update: Update) -> bool:
                return update.channel_post is not None

        channel_post = _ChannelPost()

        class _EditedChannelPost(UpdateFilter):
            name = 'Filters.update.edited_channel_post'

            def filter(self, update: Update) -> bool:
                return update.edited_channel_post is not None

        edited_channel_post = _EditedChannelPost()

        class _ChannelPosts(UpdateFilter):
            name = 'Filters.update.channel_posts'

            def filter(self, update: Update) -> bool:
                return update.channel_post is not None or update.edited_channel_post is not None

        channel_posts = _ChannelPosts()

        def filter(self, update: Update) -> bool:
            return bool(self.messages(update) or self.channel_posts(update))

    update = _UpdateType()
    """Subset for filtering the type of update.

    Examples:
        Use these filters like: ``Filters.update.message`` or
        ``Filters.update.channel_posts`` etc. Or use just ``Filters.update`` for all
        types.

    Attributes:
        message: Updates with :attr:`telegram.Update.message`
        edited_message: Updates with :attr:`telegram.Update.edited_message`
        messages: Updates with either :attr:`telegram.Update.message` or
            :attr:`telegram.Update.edited_message`
        channel_post: Updates with :attr:`telegram.Update.channel_post`
        edited_channel_post: Updates with
            :attr:`telegram.Update.edited_channel_post`
        channel_posts: Updates with either :attr:`telegram.Update.channel_post` or
            :attr:`telegram.Update.edited_channel_post`
    """
