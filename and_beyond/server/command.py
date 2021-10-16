import abc
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from and_beyond.server.client import Client
    from and_beyond.server.main import AsyncServer


class AbstractCommandSender(abc.ABC):
    name: str
    server: 'AsyncServer'
    operator: int

    @abc.abstractmethod
    async def reply(self, message: str) -> None:
        pass

    async def no_permissions(self, min_level: int) -> None:
        await self.reply('You do not have the permissions for that command.')
        await self.reply(f'It requires a minimum permission level of {min_level},')
        await self.reply(f'but you only have a permission level of {self.operator}.')

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<CommandSender name={self.name!r}>'


class ConsoleCommandSender(AbstractCommandSender):
    name = 'CONSOLE'
    operator = 3

    def __init__(self, server: 'AsyncServer') -> None:
        self.server = server

    async def reply(self, message: str) -> None:
        print(message) # Wow so complicated


class ClientCommandSender(AbstractCommandSender):
    client: 'Client'
    operator = 0

    def __init__(self, client: 'Client') -> None:
        self.server = client.server
        self.client = client

    @property
    def name(self) -> str:
        if self.client.nickname is None:
            # Use client's IP address instead
            return self.client._writer.get_extra_info('peername')[0]
        return self.client.nickname

    async def reply(self, message: str) -> None:
        return await self.client.send_chat(message)


def evaluate_client(arg: str, server: 'AsyncServer') -> Optional['Client']:
    if arg in server.clients_by_name:
        return server.clients_by_name[arg]
    try:
        uuid = UUID(arg)
    except ValueError:
        return None
    if uuid in server.clients_by_uuid:
        return server.clients_by_uuid[uuid]
    return None
