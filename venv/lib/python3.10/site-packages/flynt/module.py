import dataclasses


@dataclasses.dataclass
class Foo:
    bar: int


class FooChild(Foo):
    pass
