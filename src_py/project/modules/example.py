import hat.aio
import hat.event.server.common


json_schema_id = None
json_schema_repo = None

_source_id = 0


async def create(conf, engine):
    module = Module()

    global _source_id
    module._source = hat.event.server.common.Source(
        type=hat.event.server.common.SourceType.MODULE,
        name=__name__,
        id=_source_id)
    _source_id += 1

    module._subscription = hat.event.server.common.Subscription([
        ('gateway', '?', 'example', '?', 'gateway', 'counter')])
    module._async_group = hat.aio.Group()
    module._engine = engine

    return module


class Module(hat.event.server.common.Module):

    @property
    def async_group(self):
        return self._async_group

    @property
    def subscription(self):
        return self._subscription

    async def create_session(self):
        return Session(self._engine, self._source,
                       self._async_group.create_subgroup())


class Session(hat.event.server.common.ModuleSession):

    def __init__(self, engine, source, group):
        self._engine = engine
        self._source = source
        self._async_group = group

    @property
    def async_group(self):
        return self._async_group

    async def process(self, changes):
        return [
            self._engine.create_process_event(
                self._source,
                hat.event.server.common.RegisterEvent(
                    event_type=('counter', ),
                    source_timestamp=None,
                    payload=event.payload))
            for event in changes]
