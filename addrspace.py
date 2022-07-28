# -*- encoding: utf-8 -*-

import abc
import typing
import segment

class AddressSpace(abc.ABC):
    @abc.abstractmethod
    def default_space(self, space: int) -> typing.NoReturn:
        pass
    
    @abc.abstractmethod
    def bit(self, addr: int, space: int = 0) -> int:
        return 0

    @abc.abstractmethod
    def u16(self, addr: int, space: int = 0) -> int:
        return 0

    @abc.abstractmethod
    def i16(self, addr: int, space: int = 0) -> int:
        return 0

    @abc.abstractmethod
    def u32(self, addr: int, space: int = 0) -> int:
        return 0

    @abc.abstractmethod
    def i32(self, addr: int, space: int = 0) -> int:
        return 0

    @abc.abstractmethod
    def f32(self, addr: int, space: int = 0) -> float:
        return 0.0

class ModbusAddressSpace(AddressSpace):
    def __init__(self, segset: segment.SegmentSet, defspace: int = 1) -> None:
        super().__init__()
        self.segset = segset
        self.defspace = defspace

    def default_space(self, space: int) -> typing.NoReturn:
        self.defspace = space

    def bit(self, addr: int, space: int = 0) -> int:
        return self.ref(addr, space).bit(addr)
        
    def u16(self, addr: int, space: int = 0) -> int:
        return self.ref(addr, space).u16le(addr)
    
    def i16(self, addr: int, space: int = 0) -> int:
        return self.ref(addr, space).i16le(addr)

    def u32(self, addr: int, space: int = 0) -> int:
        return self.ref(addr, space).u32be(addr)
    
    def i32(self, addr: int, space: int = 0) -> int:
        return self.ref(addr, space).i32be(addr)

    def f32(self, addr: int, space: int = 0) -> float:
        return self.ref(addr, space).f32(addr)

    def ref(self, addr: int, space: int) -> segment.Segment:
        s: int = space if space != 0 else self.defspace
        return self.segset.ref(addr, s)