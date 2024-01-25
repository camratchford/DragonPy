import array
from dragonpy.mx6309.callback import add_read_byte_middleware, add_write_byte_middleware
from dragonpy.mx6309.peripheral import BaseMX6309Peripheral


@add_write_byte_middleware(0xFF00)
def write_to_page_register(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    mmu = kwargs.get('peripheral')


@add_read_byte_middleware(0xFF00)
def read_from_page_register(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    mmu = kwargs.get('peripheral')


class MX6309MMU(BaseMX6309Peripheral):
    """
    A custom CPLD-based MMU that expands the 16 bytes of memory up to 19
    """
    callbacks = [
        write_to_page_register,
        read_from_page_register
    ]
    # 64 possible pages
    page_register = array.array("B", [0x00])

    def __init__(self, periphery):
        super().__init__(periphery)
