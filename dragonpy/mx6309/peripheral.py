from typing import ClassVar

from dragonpy.mx6309.callback import BaseCallback


class BaseMX6309Peripheral:
    callbacks: ClassVar[list[BaseCallback]]

    def __init__(self, periphery):
        self.periphery = periphery
        self.cfg = self.periphery.cfg
        self.cpu = self.periphery.cpu
        self.memory = self.periphery.memory

        for callback in self.callbacks:
            callback.peripheral = self
            callback.periphery = self.periphery

            memory_map_method = getattr(self.memory, callback.memory_map_method)
            if memory_map_method:
                memory_map_method(
                    callback_func=callback.func,
                    start_addr=callback.start_addr,
                    end_addr=callback.end_addr
                )
