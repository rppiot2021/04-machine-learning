import hat.aio
import hat.event.common
import hat.gui.common
import hat.util


json_schema_id = None
json_schema_repo = None


async def create_subscription(conf):
    return hat.event.common.Subscription([
        ('gui', 'system', 'timeseries', '*')])


async def create_adapter(conf, event_client):
    adapter = Adapter()

    adapter._async_group = hat.aio.Group()
    adapter._event_client = event_client
    adapter._sessions = set()
    adapter._series = {'reading': [], 'forecast': []}

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
                series_id = event.event_type[-1]
                new_series = self._series[series_id] + [event.payload.data]
                self._series = dict(self._series, **{series_id: new_series})
            if len(self._series['reading']) > 71:
                self._series['reading'] = self._series['reading'][-48:]
            if len(self._series['forecast']) > 24:
                self._series['forecast'] = self._series['forecast'][-24:]
            for session in self._sessions:
                if session.is_open:
                    session.notify_state_change(self._series)


class Session(hat.gui.common.AdapterSession):

    def __init__(self, juggler_client, group):
        self._juggler_client = juggler_client
        self._async_group = hat.aio.Group()

    @property
    def async_group(self):
        return self._async_group

    def notify_state_change(self, state):
        self._juggler_client.set_local_data(state)
