# -*- encoding: utf-8 -*-

import struct
import typing

class Segment:
    def __init__(self, addr_begin: int, addr_end: int, width: int, space: int, data: bytes):
        self.addr_begin = addr_begin
        self.addr_end = addr_end
        self.width = width
        self.space = space
        self.data = data
        self.size = len(data)
        
        if addr_end < addr_begin:
            raise RuntimeError("Segment Address Error: %s < %s" % (addr_end, addr_begin))
        if (addr_end - addr_begin) * width < self.size:
            raise RuntimeError("Segment Size Error: %s < %s" % ((addr_end - addr_begin) * width, self.size))
        
    def bit(self, addr: int) -> int:
        if addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        b = struct.unpack_from("B", self.data, addr / 8)
        return (b >> (addr % 8)) & 0x01
    
    def u16le(self, addr: int) -> int:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from("<H", self.data, addr * self.width / 8)

    def u16be(self, addr: int) -> int:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from(">H", self.data, addr * self.width / 8)

    def i16le(self, addr: int) -> int:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from("<h", self.data, addr * self.width / 8)

    def i16be(self, addr: int) -> int:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from(">h", self.data, addr * self.width / 8)

    def u32le(self, addr: int) -> int:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from("<I", self.data, addr * self.width / 8)

    def u32be(self, addr: int) -> int:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from(">I", self.data, addr * self.width / 8)

    def i32le(self, addr: int) -> int:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from("<i", self.data, addr * self.width / 8)

    def i32be(self, addr: int) -> int:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from(">i", self.data, addr * self.width / 8)

    def f32(self, addr: int) -> float:
        if self.width < 8 or addr < self.addr_begin or addr >= self.addr_end:
            return 0
        addr = addr - self.addr_begin
        return struct.unpack_from("f", self.data, addr * self.width / 8)

class SegmentSet:
    def __init__(self):
        self.segment: typing.List[Segment] = []
        self.null_segment: Segment = Segment(0, 0, 0, 0)
        
    def add(self, segment: Segment) -> typing.NoReturn:
        self.segment.append(segment)

    def ref(self, addr: int, space: int) -> Segment:
        for segment in self.segment:
            if segment.space == space and segment.addr_begin <= addr and segment.addr_end > addr:
                return segment
        return self.null_segment
