import array
from dragonpy.mx6309.callback import read_bytes_callback, write_bytes_callback, add_read_word_callback
from dragonpy.mx6309.peripheral import BaseMX6309Peripheral


@write_bytes_callback(0xF200)
def write_to_console(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    uart = kwargs.get('peripheral')


@read_bytes_callback(0xF200)
def read_from_console(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    uart = kwargs.get('peripheral')


@add_read_word_callback(0xF200)
def read_from_keyboard(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    """ Reads byte from the USB keyboard UART """
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    uart = kwargs.get('peripheral')


class SCC2691AC1(BaseMX6309Peripheral):
    """
    This card is actually 2 SCC2691AC1s, but making it one class makes sense as they both handle input
    """
    callbacks = [write_to_console, read_from_console, read_from_keyboard]

    def __init__(self, periphery):
        super().__init__(periphery)
