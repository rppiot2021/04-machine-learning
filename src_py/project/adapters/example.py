import hat.aio
import hat.event.common
import hat.gui.common
import hat.util


json_schema_id = None
json_schema_repo = None


async def create_subscription(conf):
    return hat.event.common.Subscription([('counter', )])


async def create_adapter(conf, event_client):
    adapter = Adapter()

    adapter._async_group = hat.aio.Group()
    adapter._event_client = event_client
    adapter._sessions = set()
    adapter._state = {}

    adapter._async_group.spawn(adapter._main_loop)

    return adapter


class Adapter(hat.gui.common.Adapter):

    @property
    def async_group(self):
        return self._async_group

    async def create_session(self, juggler_client):
        session = Session(
            juggler_client,
            self._async_group.create_subgroup())
        self._sessions.add(session)
        return session

    async def _main_loop(self):
        while True:
            events = await self._event_client.receive()
            for event in events:
                self._state = {'counter': event.payload.data}
            for session in self._sessions:
                if session.is_open:
                    session.notify_state_change(self._state)


class Session(hat.gui.common.AdapterSession):

    def __init__(self, juggler_client, group):
        self._juggler_client = juggler_client
        self._async_group = group

    @property
    def async_group(self):
        return self._async_group

    def notify_state_change(self, state):
        self._juggler_client.set_local_data(state)
