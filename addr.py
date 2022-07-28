# -*- encoding: utf-8 -*-

import enum
import iface_class

class AddrType(enum.Enum):
    """ 地址类型 """
    MODBUS_INPUT_BITS = 0       # modbus 只读遥信
    MODBUS_BITS = 1             # modbus 线圈/读写位
    MODBUS_COIL = 1             # modbus 线圈/读写位
    MODBUS_INPUT_REGS = 2       # modbus 只读寄存器
    MODBUS_REGS = 3             # modbus 读写寄存器

class AddrRange(iface_class.JsonEnabled):
    """ 地址区间 前闭后开 [begin, end) """

    def __init__(self, addr_type: AddrType, begin: int, end: int, space = 0, ts_presleep = 0) -> None:
        # 地址类型
        self.addr_type: AddrType = addr_type
        # 起始地址 (含)
        self.addr_begin: int = begin
        # 终止地址 (不含)
        self.addr_end: int = end
        # 地址空间号/modbus设备地址
        self.space: int = space
        # 采集时前置sleep毫秒数
        self.ts_presleep: int = ts_presleep
