import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id, speaker_id, toilet_id = await asyncio.gather(
        service.register_device(device=hue_light),
        service.register_device(device=speaker),
        service.register_device(device=toilet)
    )

    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function

    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)


    # create a few programs
    await run_parallel(
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_ON)
            ]
        ),
        run_sequence(
            service.run_program(
                [
                    Message(speaker_id, MessageType.SWITCH_ON),
                    Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
                ]
            )
        )
    )
    # [
    #     Message(hue_light_id, MessageType.SWITCH_ON),
    #     Message(speaker_id, MessageType.SWITCH_ON),
    #     Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up"),
    # ]

    await run_parallel(
        service.run_program(
            [
                Message(hue_light_id, MessageType.SWITCH_OFF),
                Message(speaker_id, MessageType.SWITCH_OFF)
            ]
        ),
        run_sequence(
            service.run_program(
                [
                    Message(toilet_id, MessageType.FLUSH),
                    Message(toilet_id, MessageType.CLEAN),
                ]
            )
        )
    )

    # sleep_program = [
    #     Message(hue_light_id, MessageType.SWITCH_OFF),
    #     Message(speaker_id, MessageType.SWITCH_OFF),
    #     Message(toilet_id, MessageType.FLUSH),
    #     Message(toilet_id, MessageType.CLEAN),
    # ]

    # run the programs
    # await run_sequence(
    #     wake_up_program,
    #     service.run_program(sleep_program)
    # )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)

"""Connecting Hue Light.
Hue Light connected.
Connecting to Smart Speaker.
Smart Speaker connected.
Connecting to Smart Toilet.
Smart Toilet connected.
=====RUNNING PROGRAM======
Hue Light handling message of type SWITCH_ON with data [].
Hue Light received message.
Smart Speaker handling message of type SWITCH_ON with data [].
Smart Speaker received message.
Smart Speaker handling message of type PLAY_SONG with data [Rick Astley - Never Gonna Give You Up].
Smart Speaker received message.
=====END OF PROGRAM======
=====RUNNING PROGRAM======
Hue Light handling message of type SWITCH_OFF with data [].
Hue Light received message.
Smart Speaker handling message of type SWITCH_OFF with data [].
Smart Speaker received message.
Smart Toilet handling message of type FLUSH with data [].
Smart Toilet received message.
Smart Toilet handling message of type CLEAN with data [].
Smart Toilet received message.
=====END OF PROGRAM======
Elapsed: 5.005261988997518"""

#
"""Connecting Hue Light.
Connecting to Smart Speaker.
Connecting to Smart Toilet.
Hue Light connected.
Smart Speaker connected.
Smart Toilet connected.
=====RUNNING PROGRAM======
Hue Light handling message of type SWITCH_ON with data [].
=====RUNNING PROGRAM======
Hue Light handling message of type SWITCH_OFF with data [].
Hue Light received message.
Smart Speaker handling message of type SWITCH_ON with data [].
Hue Light received message.
Smart Speaker handling message of type SWITCH_OFF with data [].
Smart Speaker received message.
Smart Speaker handling message of type PLAY_SONG with data [Rick Astley - Never Gonna Give You Up].
Smart Speaker received message.
Smart Toilet handling message of type FLUSH with data [].
Smart Speaker received message.
=====END OF PROGRAM======
Smart Toilet received message.
Smart Toilet handling message of type CLEAN with data [].
Smart Toilet received message.
=====END OF PROGRAM======
Elapsed: 2.5067292430030648"""

#
"""Connecting Hue Light.
Connecting to Smart Speaker.
Connecting to Smart Toilet.
Hue Light connected.
Smart Speaker connected.
Smart Toilet connected.
=====RUNNING PROGRAM======
Hue Light handling message of type SWITCH_ON with data [].
=====RUNNING PROGRAM======
Smart Speaker handling message of type SWITCH_ON with data [].
Hue Light received message.
=====END OF PROGRAM======
Smart Speaker received message.
Smart Speaker handling message of type PLAY_SONG with data [Rick Astley - Never Gonna Give You Up].
Smart Speaker received message.
=====END OF PROGRAM======
=====RUNNING PROGRAM======
Hue Light handling message of type SWITCH_OFF with data [].
=====RUNNING PROGRAM======
Smart Toilet handling message of type FLUSH with data [].
Hue Light received message.
Smart Speaker handling message of type SWITCH_OFF with data [].
Smart Toilet received message.
Smart Toilet handling message of type CLEAN with data [].
Smart Speaker received message.
=====END OF PROGRAM======
Smart Toilet received message.
=====END OF PROGRAM======
Elapsed: 2.5055530669997097"""

# 2
"""Connecting Hue Light.
Connecting to Smart Speaker.
Connecting to Smart Toilet.
Hue Light connected.
Smart Speaker connected.
Smart Toilet connected.
Hue Light handling message of type SWITCH_ON with data [].
=====RUNNING PROGRAM======
Smart Speaker handling message of type SWITCH_ON with data [].
Hue Light received message.
Smart Speaker received message.
Smart Speaker handling message of type PLAY_SONG with data [Rick Astley - Never Gonna Give You Up].
Smart Speaker received message.
=====END OF PROGRAM======
=====RUNNING PROGRAM======
Hue Light handling message of type SWITCH_OFF with data [].
=====RUNNING PROGRAM======
Smart Toilet handling message of type FLUSH with data [].
Hue Light received message.
Smart Speaker handling message of type SWITCH_OFF with data [].
Smart Toilet received message.
Smart Toilet handling message of type CLEAN with data [].
Smart Speaker received message.
=====END OF PROGRAM======
Smart Toilet received message.
=====END OF PROGRAM======
Elapsed: 2.5044225780002307"""