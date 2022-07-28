# -*- encoding: utf-8 -*-

from os import device_encoding
import typing
import devfield
import iface_class

class DD(iface_class.JsonEnabled):
    """ 设备数据 Device Data """
    def __init__(self) -> None:
        # 设备类型
        self.devtype: devfield.DeviceType = devfield.DeviceType.UDD
        # 设备运行状态
        self.devstatus: devfield.DeviceCommonStatus = devfield.DeviceCommonStatus()
        # 发生中的告警信息
        self.alarm: typing.List[devfield.AlarmInfo] = []

        ### 以下通用字段, EMS系统不识别其含义 ###
        # 通用 数值 字段
        self.number: typing.Dict[str, float] = {}
        # 通用 布尔/状态 字段
        self.status: typing.Dict[str, bool] = {}
        # 通用 字符串/二进制 字段
        self.raw: typing.Dict[str, bytes] = {}

        
    def checkAlarm(self, alarm: bool, alarm_id: int, standard_id: str, content: str, device: str = None) -> None:
        """ 检测和记录告警测点状态 """
        if not alarm:
            return None
        ainfo = devfield.AlarmInfo()
        ainfo.alarm_id = alarm_id
        ainfo.standard_id = standard_id
        ainfo.content = content
        ainfo.device = device
        self.alarm.append(ainfo)
        
class DDOfUserDefined(DD):
    """ 用户自定义设备: 只使用通用字段 """
    def __init__(self) -> None:
        self.devtype: devfield.DeviceType = devfield.DeviceType.UDD

class DDofMngDevice(DD):
    """ 管理设备, 一个管理设备可导出其管理的多个设备的数据
    例如: EMS可导出站内多个设备数据. BMS, 可导出其管理的所有堆和簇数据
    """

    def __init__(self) -> None:
        self.devtype: devfield.DeviceType = devfield.DeviceType.MNG
        # 次级设备数据
        self.sub_dd: typing.List[DD] = []

class DDOfInverter(DD):
    """ 逆变器数据 (PCS/光伏逆变器) """
    def __init__(self) -> None:
        self.devtype: devfield.DeviceType = devfield.DeviceType.PCS

        # *** 工作参数 ***

        # 是否支持EMS端控制
        self.remote_control = False
        # 是否并网
        self.grid_interconnection = False
        # 充放电状态
        self.charge_status: devfield.ChargeStatus = devfield.ChargeStatus.IDLE
        # 工作模式
        self.work_mode: devfield.InverterWorkMode = devfield.InverterWorkMode.UNKNOWN
        # 逆变器温度
        self.temperature: float = None
        # 逆变器环境温度
        self.environ_temperature: float = None

        # *** 交流测 ***

        # 运行状态
        self.ac_runtime: devfield.ACRuntime = devfield.ACRuntime()
        # 充电量
        self.ac_charge: devfield.AccIndicator = devfield.AccIndicator()
        # 放电量
        self.ac_discharge: devfield.AccIndicator = devfield.AccIndicator()

        # *** 直流测 ***

        # 直流支路
        self.branch: typing.List[devfield.DCBranch] = []
       
class DDOfCluster(DD):
    """ 电池簇 """
    def __init__(self) -> None:
        self.devtype: devfield.DeviceType = devfield.DeviceType.BAT_CLUSTER

        # 堆运行状态
        self.cluster_status: devfield.BatterySystemStatus = devfield.BatterySystemStatus()
        # 堆充放电状态
        self.charge_status: devfield.ChargeStatus = devfield.ChargeStatus()
        # 堆运行时参数
        self.runtime: devfield.BatterySystemRuntime = devfield.BatterySystemRuntime()
        # 累计充放电量和容量
        self.capacity: devfield.BatterySystemCapacity = devfield.BatterySystemCapacity()
        # 电芯数据
        self.battery: typing.List[devfield.BatteryRuntime] = []
 
class DDOfStack(DD):
    """ 电池堆 """
    def __init__(self) -> None:
        self.devtype: devfield.DeviceType = devfield.DeviceType.BAT_STACK

        # 堆运行状态
        self.stack_status: devfield.BatterySystemStatus = devfield.BatterySystemStatus()
        # 堆充放电状态
        self.charge_status: devfield.ChargeStatus = devfield.ChargeStatus()
        # 堆运行时参数
        self.runtime: devfield.BatterySystemRuntime = devfield.BatterySystemRuntime()
        # 累计充放电量和容量
        self.capacity: devfield.BatterySystemCapacity = devfield.BatterySystemCapacity()
        # 电池簇
        self.cluster: typing.List[DDOfCluster] = []
        
class DDOfEM2(DD):
    """ 双向电表 """

    def __init__(self) -> None:
        self.devtype: devfield.DeviceType = devfield.DeviceType.EM2

        # 计费时段
        self.tr: typing.List[devfield.EMChargingTR] = []

        # 运行时度量-电压 电流 功率 (正向)
        self.forward_runtime: devfield.ACRuntime = devfield.ACRuntime()
        # 运行时度量-电压 电流 功率 (反向)
        self.reverse_runtime: devfield.ACRuntime = devfield.ACRuntime()

        # 电量度量 (正向)
        self.forward_energy: devfield.EnergyMeasure = devfield.EnergyMeasure()
        # 电量度量 (反向)
        self.reverse_energy: devfield.EnergyMeasure = devfield.EnergyMeasure()

class DDOfAirConditioner(DD):
    """ 空调 """

    def __init__(self) -> None:
        self.devtype: devfield.DeviceType = devfield.DeviceType.AC

        # 运行时度量
        self.runtime: devfield.AirConditionerRuntime = devfield.AirConditionerRuntime()

        # 关键遥调参数: 高温告警点
        self.temperature_high_point: float = 0.0
        # 关键遥调参数: 低温告警点
        self.temperature_low_point: float = 0.0

        # 关键告警: 温度
        self.alarm_temperature: bool = False
        # 关键告警: 电压
        self.alarm_voltage: bool = False
        # 关键告警: 气压
        self.alarm_pressure: bool = False
        # 关键告警: 压缩机
        self.alarm_compressor: bool = False
        # 关键告警: 传感器
        self.alarm_sensor: bool = False
        
