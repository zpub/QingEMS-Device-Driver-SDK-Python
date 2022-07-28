# -*- encoding: utf-8 -tterySystemCapacity()
import enum
import typing
import iface_class

### 常量定义 ###

class DeviceType(enum.Enum):
    """ 设备类型 """
    UDD = 0             # 未知/用户自定义设备
    BAT_CELL = 1        # 电芯
    BAT_PACK = 2        # 电池包
    BAT_CLUSTER = 3     # 电池簇
    BAT_STACK = 4       # 电堆
    BMS = 5             # BMS系统
    PCS = 6             # PCS
    EM = 7              # 单向电表
    EM2 = 8             # 双向电表
    AC = 9              # 空调
    EMS = 10            # EMS系统
    MNG = 10            # 管理类系统


class ChargeStatus(enum.Enum):
    """ 充放电状态 """
    CHARGE = -1     # 充电
    IDLE = 0        # 静置
    DISCHARGE = 1   # 放电


class InverterWorkMode(enum.Enum):
    """ 逆变器工作模式 """
    UNKNOWN = 0                 # 未知
    DC_CONSTANT_VOLTAGE = 1     # 直流恒压
    DC_CONSTANT_CURRENT = 2     # 直流恒流
    DC_CONSTANT_POWER = 3       # 直流恒功率
    AC_CONSTANT_VOLTAGE = 4     # 交流恒压 (V/F)
    AC_CONSTANT_CURRENT = 5     # 交流恒流
    AC_CONSTANT_POWER_ = 6      # 交流恒功率 (PQ)
    VSG = 7                     # VSG

class BatterySystemStatus(enum.Enum):
    """ 电池系统状态 """
    READY = 0x0000              # 就绪
    FAULT = 0x0001              # 故障
    MAINTAIN = 0x0002           # 维护
    NO_CHARGE = 0x0010          # 禁充
    NO_DISCHARGE = 0x0020       # 禁放
    NO_ACTION = 0x0030          # 禁充放

class EMChargingLevel(enum.Enum):
    """ 电表计费等级 """
    FREE = 0                    # 不计费
    SHARP = 1                   # 尖
    PEAK = 2                    # 峰
    FLAT = 3                    # 平
    VALLEY = 4                  # 谷

### 字段结构定义 ###

class DeviceFieldBase(iface_class.JsonEnabled):
    pass

class DevCmd(DeviceFieldBase):
    """ 设备指令 """
    def __init__(self) -> None:
        self.cmd: str = "noop"
        self.args: typing.List[bytes] = []

class DevRet(DeviceFieldBase):
    """ 设备指令返回结果 """

    def __init__(self, succ: bool, content: bytes) -> None:
        self.succ: bool = succ
        self.cont: bytes = content

class AlarmInfo(DeviceFieldBase):
    """ 告警 """
    
    def __init__(self) -> None:
        # 设备定义的告警ID
        self.alarm_id: int = 0
        # EMS系统标准告警ID
        self.standard_id: str = "AI-NIL-$000"
        # 告警内容
        self.content: str = ""
        # 告警设备信息
        self.device: str = None

class AccIndicator(DeviceFieldBase):
    """ 累计指标 """
    
    def __init__(self) -> None:
        # 总累计量
        self.total: float = 0.0
        # 当日累计量
        self.daily: float = 0.0
        # 当次累计量
        self.round: float = 0.0

class AggIndicator(DeviceFieldBase):
    """ 聚合指标 """

    def __init__(self) -> None:
        # 聚合值
        self.mass: float = 0.0
        # 均值
        self.avg: float = 0.0
        # 最小值
        self.min: float = 0.0
        # 最大值
        self.max: float = 0.0
        # 最小值ID
        self.min_id: int = 0
        # 最大值ID
        self.max_id: int = 0

class ACField3(DeviceFieldBase):
    """ 交流三相三线数据 """

    def __init__(self) -> None:
        self.total: float = 0.0
        self.phase_a: float = 0.0
        self.phase_b: float = 0.0
        self.phase_c: float = 0.0
        self.line_ab: float = 0.0
        self.line_bc: float = 0.0
        self.line_ca: float = 0.0


class ACVoltage(ACField3):
    """ 交流电压 (默认单位: 伏特) """
    pass


class ACCurrent(ACField3):
    """ 交流电流 (默认单位: 安培) """
    pass


class ACPower(ACField3):
    """ 交流功率 (默认单位: 瓦特) """
    def W2kW(w: float) -> float:
        return w / 1000.0

    def kW2W(kw: float) -> float:
        return kw * 1000.0


class ACEnergy(ACField3):
    """ 交流电能 (默认单位: 焦耳) """
    def J2kWh(J: float) -> float:
        return J / (3600.0 * 1000.0)

    def kWh2J(kWh: float) -> float:
        return kWh * (3600.0 * 1000.0)


class ACPowerFactor(ACField3):
    """ 交流功率因数 """
    pass

class ACFrequency(ACField3):
    """ 交流频率 """
    pass
class ACPowerMeasure(DeviceFieldBase):
    """ 直流功率度量 """

    def __init__(self) -> None:
        self.active: ACPower = ACPower()
        self.reactive: ACPower = ACPower()
        self.apparent: ACPower = ACPower()
        self.factor: ACPowerFactor = ACPowerFactor()

class ACRuntime(DeviceFieldBase):
    """ 交流运行时度量 """
    
    def __init__(self) -> None:
        # 电压
        self.voltage: ACVoltage = ACVoltage()
        # 电流
        self.current: ACCurrent = ACCurrent()
        # 功率
        self.power: ACPowerMeasure = ACPowerMeasure()
        # 频率
        self.frequency: ACFrequency = ACFrequency()

class DCRuntime(DeviceFieldBase):
    """ 直流运行时度量 """

    def __init__(self) -> None:
        # 电压
        self.voltage: float = 0
        # 电流
        self.current: float = 0
        # 功率
        self.power: float = 0


class DeviceCommonStatus(DeviceFieldBase):
    """ 通用设备状态 """

    def __init__(self) -> None:
        # 是否在线/通讯正常
        self.online = True
        # 设备工作/停机
        self.run: bool = True
        # 是否告警
        self.alarm: bool = False
        # 是否故障
        self.fault: bool = False

class DCBranch(DeviceFieldBase):
    """ 直流支路 """

    def __init__(self) -> None:
        # 支路编号
        self.id : int = 0
        # 支路名称
        self.name : str = ""
        # 运行状态
        self.runtime: DCRuntime = DCRuntime()
        
class BatteryRuntime(DeviceFieldBase):
    """ 电池运行时度量 """

    def __init__(self) -> None:
        # 电压
        self.voltage: float = 0.0
        # 电流
        self.current: float = 0.0
        # 温度
        self.temperature: float = 0.0
        # SOC
        self.soc: float = 0.0
        # SOH
        self.soh: float = 0.0
        # 电阻/内阻
        self.r: float = 0.0
        # 绝缘电阻-正极
        self.positive_ir: float = 0.0
        # 绝缘电阻-负极
        self.negative_ir: float = 0.0

       
class BatterySystemRuntime(DeviceFieldBase):
    """ 电池系统运行时度量 """
    
    def __init__(self) -> None:
        # 电压
        self.voltage: AggIndicator = AggIndicator()
        # 电流
        self.current: AggIndicator = AggIndicator()
        # 温度
        self.temperature: AggIndicator = AggIndicator()
        # SOC
        self.soc: AggIndicator = AggIndicator()
        # SOH
        self.soh: AggIndicator = AggIndicator()
        # 电阻/内阻
        self.r: AggIndicator = AggIndicator()
        # 绝缘电阻-正极
        self.positive_ir: AggIndicator = AggIndicator()
        # 绝缘电阻-负极
        self.negative_ir: AggIndicator = AggIndicator()

class BatterySystemCapacity(DeviceFieldBase):
    """ 电池系统容量度量 """

    def __init__(self) -> None:
        # 充电量
        self.charge: AccIndicator = AccIndicator()
        # 剩余容量
        self.charge_capacity: float = 0.0
        # 放电量
        self.discharge: AccIndicator = AccIndicator()
        # 剩余电量
        self.discharge_capacity: float = 0.0


class EMChargingTR(DeviceFieldBase):
    """ 电表计费时段 """

    def __init__(self) -> None:
        # 时区: 默认 UTC+8 (东8区)
        self.tz: int = 8
        # 起始时刻 (距离0点的秒数)
        self.begin: int = 0
        # 结束时刻 (距离0点的秒数)
        self.end: int = 0
        # 计费等级
        self.level: EMChargingLevel = EMChargingLevel.FREE

class EnergyMeasure(DeviceFieldBase):
    """ 电量/能量度量 """

    def __init__(self) -> None:
        self.total: ACEnergy = ACEnergy()
        self.sharp: ACEnergy = ACEnergy()
        self.peak: ACEnergy = ACEnergy()
        self.flat: ACEnergy = ACEnergy()
        self.valley: ACEnergy = ACEnergy()

class AirConditionerRuntime(DeviceFieldBase):
    """ 空调运行时度量 """

    def __init__(self) -> None:
        # 当前温度
        self.temperature: float = 0.0
        # 制冷低点
        self.refrigeration_low: float = 0.0
        # 制冷高点
        self.refrigeration_high: float = 0.0
        # 制热低点
        self.heating_low: float = 0.0
        # 制热高点
        self.heating_high: float = 0.0
