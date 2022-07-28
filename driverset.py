# -*- encoding: utf-8 -*-

from math import prod
import typing
from driver import DriverBase
from devfield import DeviceType
import driver_udd_skiffenergy_emu

class DriverSet:
    def __init__(self) -> None:
        self.driver: typing.Dict[str, DriverBase] = {}
    
    def register(self, type: DeviceType, producer: str, model: str, driver: DriverBase):
        key = DriverSet.gen_driver_index_key(type, producer, model)
        self.driver[key] = driver
        
    def ref(self, type: DeviceType, producer: str, model: str) -> DriverBase:
        key = DriverSet.gen_driver_index_key(type, producer, model)
        return None if key not in self.driver else self.driver[key]

    def gen_driver_index_key(type: DeviceType, producer: str, model: str) -> str:
        return "%s|%s|%s" % (type, producer, model)

DRIVERS = DriverSet()

def LoadLocalDriverFor(cls):
    DRIVERS.register(cls.DEVICE_TYPE, cls.PRODUCER, cls.MODEL, cls())
    
LoadLocalDriverFor(driver_udd_skiffenergy_emu.UDD_Skiffenergy_EMU)
