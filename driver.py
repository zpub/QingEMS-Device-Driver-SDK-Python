# -*- encoding: utf-8 -*-

import abc
import typing

from addr import AddrRange
from addrspace import AddressSpace
from devdata import DD
from devfield import DevCmd, DeviceType
from devfield import DevRet

class DriverBase(abc.ABC):
    """ 设备驱动基类 """

    # 设备类型
    DEVICE_TYPE: DeviceType = DeviceType.UDD
    # 生产商
    PRODUCER: str = "生产商"
    # 型号
    MODEL: str = "型号"

    @abc.abstractmethod
    def defineAddrRange(self) -> typing.List[AddrRange]:
        """ 定义需要采集的地址区间 """
        pass
    
    @abc.abstractmethod
    def parseDeviceData(self, addr_space: AddressSpace) -> DD:
        """ 解析设备数据 """
        pass

    @abc.abstractmethod
    def execCommand(self, cmd: DevCmd) -> DevRet:
        """ 执行指令 """
        pass
