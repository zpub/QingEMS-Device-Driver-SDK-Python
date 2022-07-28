# -*- encoding: utf-8 -*-

import abc
import typing

from addr import AddrRange, AddrType
from addrspace import AddressSpace
from devdata import DD, DDOfInverter, DDofMngDevice
from devfield import DevCmd, DeviceType
from devfield import DevRet
from driver import DriverBase

class UDD_Skiffenergy_EMU(DriverBase):
    # 设备类型
    DEVICE_TYPE: DeviceType = DeviceType.UDD
    # 生产商
    PRODUCER: str = "skiffenergy"
    # 型号
    MODEL: str = "emu"

    def defineAddrRange(self) -> typing.List[AddrRange]:
        r = [
            AddrRange(
                AddrType.MODBUS_INPUT_REGS,
                0,
                20),
            AddrRange(
                AddrType.MODBUS_REGS,
                1000,
                1050),
        ]
        return r
    
    def parseDeviceData(self, addr_space: AddressSpace) -> DD:
        """ 解析设备数据 """
        ems = DDofMngDevice()
        
        pcs = DDOfInverter()
        pass

    def execCommand(self, cmd: DevCmd) -> DevRet:
        """ 执行指令 """
        pass
