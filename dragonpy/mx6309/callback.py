from typing import Callable, Union, Literal, ClassVar

# Takes cpu_cycles, op_address, address, value. Returns either an int, or nothing
WriteFunc = Callable[[int, int, int, int], Union[int, None]]
# Takes cpu_cycles, op_address, address. Returns an int
ReadFunc = Callable[[int, int, int], int]

# todo: Type aliases for the other memory map method arguments in
#  dragonpy.components.memory.Memory

#

# Corresponds to those methods of 'dragonpy.components.memory.Memory' that map memory to callbacks/middleware
MemoryMapMethods = ClassVar[
    Literal[
        'None',
        'add_read_byte_callback', 'add_write_byte_callback',
        'add_read_word_callback', 'add_write_word_callback',
        'add_read_byte_middleware', 'add_write_byte_middleware',
        'add_read_word_middleware', 'add_write_word_middleware'
    ]
]


class BaseCallback:
    """
    peripheral: To expose access to peripheral-specific attributes.
    periphery: To expose access to config, cpu, memory, and periphery-specific attributes.
    memory_map_method: To decide which of the memory object's methods to use when mapping addresses to function calls
    func: The function that gets called when the mapped address is read/written
    start_addr: The lower bound (or only bound) of address space that the function call is mapped to
    end_addr: The upper bound of address space that the function call is mapped to
    """
    peripheral = None
    periphery = None
    memory_map_method: MemoryMapMethods = 'None'
    func: Callable
    start_addr: int
    end_addr: Union[int, None]

    def __init__(self, func: Callable, start_addr: int, end_addr: int = None):
        self.start_addr = start_addr
        self.end_addr = end_addr
        self.func = func

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs, peripheral=self.peripheral, periphery=self.periphery)


class WriteByteCallback(BaseCallback):
    memory_map_method = "add_write_byte_callback"
    func: WriteFunc

    def __call__(self, cpu_cycles: int, op_address: int, address: int, value: int):
        super().__call__(cpu_cycles, op_address, address, value)


def write_bytes_callback(start_addr: int, end_addr=None):
    def wrapper(func: WriteFunc):
        return WriteByteCallback(func=func, start_addr=start_addr, end_addr=end_addr)

    return wrapper


class ReadByteCallback(BaseCallback):
    memory_map_method = "add_read_byte_callback"
    func: ReadFunc

    def __call__(self, cpu_cycles: int, op_address: int, address: int):
        super().__call__(cpu_cycles, op_address, address)


def read_bytes_callback(start_addr: int, end_addr=None):
    def wrapper(func: ReadFunc):
        return ReadByteCallback(func=func, start_addr=start_addr, end_addr=end_addr)

    return wrapper

# todo: more classes
class ReadWordCallback(BaseCallback):
    memory_map_method = "add_read_word_callback"
    func: ReadFunc

    def __call__(self, cpu_cycles: int, op_address: int, address: int):
        super().__call__(cpu_cycles, op_address, address)



# Placeholders
def add_read_word_callback(start_addr: int, end_addr=None):
    

def add_write_word_callback(start_addr: int, end_addr=None):
    ...

def add_read_byte_middleware(start_addr: int, end_addr=None):
    ...

def add_write_byte_middleware(start_addr: int, end_addr=None):
    ...

def add_read_word_middleware(start_addr: int, end_addr=None):
    ...

def add_write_word_middleware(start_addr: int, end_addr=None):
    ...

