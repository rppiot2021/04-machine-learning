import asyncio
import hat.aio
import hat.event.common
import hat.gateway.common


json_schema_id = None
json_schema_repo = None
device_type = 'example'


async def create(conf, event_client, event_type_prefix):
    device = Device()

    device._async_group = hat.aio.Group()
    device._event_client = event_client
    device._event_type_prefix = event_type_prefix
    device._async_group.spawn(device._main_loop)

    return device


class Device(hat.gateway.common.Device):

    @property
    def async_group(self):
        return self._async_group

    async def _main_loop(self):
        counter = 0
        while True:
            await asyncio.sleep(3)
            self._event_client.register([
                hat.event.common.RegisterEvent(
                    event_type=(*self._event_type_prefix,
                                'gateway', 'counter'),
                    source_timestamp=None,
                    payload=hat.event.common.EventPayload(
                        type=hat.event.common.EventPayloadType.JSON,
                        data=counter))])
            counter += 1
