import array
from dragonpy.mx6309.callback import read_bytes_callback, write_bytes_callback
from dragonpy.mx6309.peripheral import BaseMX6309Peripheral


@write_bytes_callback(0xF100)
def write_to_vram(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    vdp = kwargs.get('peripheral')
    if vdp:
        vram = vdp.vram
    ...


@read_bytes_callback(0xF100)
def read_from_vram(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    vdp = kwargs.get('peripheral')
    if vdp:
        vram = vdp.vram


@write_bytes_callback(0xF102)
def write_to_vdp_register(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    vdp = kwargs.get('peripheral')
    if vdp:
        vram = vdp.vram


@read_bytes_callback(0xF102)
def read_from_vdp_register(cpu_cycles: int, op_address: int, address: int, value: int, **kwargs):
    periphery = kwargs.get('periphery')
    if periphery:
        cfg = periphery.cfg
        cpu = periphery.cpu
        memory = periphery.memory
    vdp = kwargs.get('peripheral')
    if vdp:
        vram = vdp.vram

class V9956(BaseMX6309Peripheral):
    """
    A video card with the venerable V9956 (the VDP from the MSX2).
    This board manages its own set of VRAM, so this class does as well.
    """
    callbacks = [
        write_to_vram,
        read_from_vram,
        write_to_vdp_register,
        read_from_vdp_register,
    ]
    # 16kb
    vram = array.array("B", [0x00] * 2**14)

    def __init__(self, periphery):
        super().__init__(periphery)
