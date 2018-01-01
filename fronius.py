###
# fronius.py
# v1.1
# Api for fetching data from Fronius Symo
#
# Still very much a work in Progress, still working on the function parameters
# Todo:
# 1.  Fix functions with Mandatory option and option combinations.
#     eg. if Scope="Device"  DeviceId is required
# 2.  Option to return csv or raw json/dict data
# 3.  Wrap into a module when bugs ironed out
#
###

# print("*************************************************")
# print("THIS IS NOT RUNNING YET - Check the CODE First :)")
# print("*************************************************")
# exit()

import requests
import json
import pprint
import time

# You might want to add  ip.ip.ip.ip  fronius to your hosts file

hostname = "fronius"



def getData(hostname,dataRequest):
    """
    All Request's come via this function.  It builds the url from args
    hostname and dataRequest.  It is advised to have a fronius hostname
    entry in /etc/hosts.  There is no authentication required, it is assumed
    you are on a local, private network.
    """
    try:
        url = "http://" + hostname + dataRequest
        r = requests.get(url,timeout=60)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        print("Request: {} failed ".format(url))
    except requests.exceptions.RequestException as e:
        print("Request failed with {}".format(e))

    exit()

def GetInverterRealtimeData(DeviceId="0",Scope='System',DataCollection='CumulationInverterData'):
    """
    :param Scope:
        String ("Device" || "System"
        System implies whole system and uses CumulationInverterData
    :param DeviceId:
        Mandatory - needs DeviceId
        String ("Solar Net: 0 ...99")
    :param DataCollection:
        String:
            "CumulationInverterData"
            "CommonInverterData"
            "3PInverterData"
            "MinMaxInverterData"

    :return:
        json (dict)
    """

    dataRq = '/solar_api/v1/GetInverterRealtimeData.cgi?'+'scope='+Scope+'&DataCollection='+DataCollection+'&DeviceId=' +DeviceId
    return getData(hostname,dataRq)

def GetSensorRealtimeData(Scope='System',DeviceId='0',DataCollection='NowStringControlData',TimePeriod='Day'):
    """
    This request provides data for all channels of a single Fronius Sensor Card.
    Inactive channels and channels with damaged sensors are not included in the response.
    :param Scope:
        String "Device" or "System"

    :param DeviceId:
        String "0" .. "99"

    :param DataCollection:
        String.
        "NowStringControlData" -> The presently measured currents of every channel.
        "LastErrorStringControlData" -> Information about the last error which triggered a service message
        "CurrentSumStringControlData" -> Current Sums of all channels for a selected time period

    :param TimePeriod:
        String.
        "Day"
        "Year"
        "Total"
    :return:
        json (dict)
    """
    dataRq = '/solar_api/v1/GetSensorRealtimeData.cgi?Scope='+Scope+'&DeviceId='+DeviceId+'&DataCollection='+DataCollection+'&TimePeriod='+TimePeriod
    return getData(hostname,dataRq)

def GetStringRealtimeData(Scope='System',DeviceId='0',DataCollection='NowStringControlData',TimePeriod='Day'):
    """
    :param Scope:
        String "Device" or "System"

    :param DeviceId:
        String "0" .. "99"

    :param DataCollection:
        String.
        "NowStringControlData" -> The presently measured currents of every channel.
        "LastErrorStringControlData" -> Information about the last error which triggered a service message
        "CurrentSumStringControlData" -> Current Sums of all channels for a selected time period

    :param TimePeriod:
        String.
        "Day"
        "Year"
        "Total"
    :return:
        json (dict)
    """

    dataRq = '/solar_api/v1/GetStringRealtimeData.cgi?Scope='+Scope+'&DeviceId='+DeviceId+'&DataCollection='+DataCollection+'&TimePeriod='+TimePeriod
    return getData(hostname, dataRq)

def GetLoggerInfo():
    """
       This request provides information about the logging device which provides this API
    """
    dataRq = '/solar_api/v1/GetLoggerInfo.cgi'
    return getData(hostname, dataRq)

def GetLoggerLEDInfo():
    """
        This request provides information about the LED states and colors on the
        device which provides this API
    """
    dataRq = '/solar_api/v1/GetLoggerLEDInfo.cgi'
    return getData(hostname, dataRq)

def InverterInfoStatusCode(code):
    if code > 10:
        return "Invalid Status"
    if code < 7:
        return "Startup"
    elif code == 7:
        return "Running"
    elif code == 8:
        return "Standby"
    elif code == 9:
        return "Bootloading"
    elif code == 10:
        return "Error"


def GetInverterInfo():
    """
    This request provides information about all inverters that are currently
    being monitored by the logging device. So this means that inverters which
    are currently not online are also reported by this request, provided these
    inverters have been seen by the logging device within the last 24 hours.
    If information about devices currently online is needed,
    the GetActiveDeviceInfo request should be used. This request also provides
    information about device classes other than inverters
    Returns:
        StatusCode (Numeric)
        0-6         Startup
        7           Running
        8           Standby
        9           Bootloading
        10          Error
    """
    dataRq = '/solar_api/v1/GetInverterInfo.cgi'
    return getData(hostname, dataRq)

def GetActiveDeviceInfo(DeviceClass='System'):
    """
        This request provides information about which devices are currently online.

        :parameter:  DeviceClass
            String:
            "Inverter"
            "Storage"
            "Ohmpilot"
            "SensorCard"
            "StringControl"
            "Meter"
            "System"
    """
    dataRq = '/solar_api/v1/GetActiveDeviceInfo.cgi?'+ 'DeviceClass=' + DeviceClass
    return getData(hostname, dataRq)


def GetMeterRealtimeData(Scope='System',DeviceId='0',DeviceClass='System'):
    """
    This request provides detailed information about Meter devices.
    Inactive channels are not included in the response and may vary depended
    on used metering device and software version. Take care about permanently
    or temporary missing channels when processing this response.
    Check the Enable,Visible fields if zero data may not be available.

    :param Scope:     String "Device" or "System"

    :param DeviceId:  String "0" .. "65535"

    :parameter:  DeviceClass  String:
    "Inverter"
    "Storage"
    "Ohmpilot"
    "SensorCard"
    "StringControl"
    "Meter"
    "System"

    :return:
       json (dict)
    """

    dataRq = '/solar_api/v1/GetMeterRealtimeData.cgi?Scope='+Scope+'&DeviceId='+DeviceId+'&DeviceClass='+DeviceClass
    return getData(hostname, dataRq)


def GetStorageRealtimeData(Scope='System',DeviceId='0'):
    """
    This request provides detailed information about batteries. Inactive channels
    are not included in the response and may vary depended on used battery and
    software version. Take care about permanently or temporary missing channels
    when processing this response.
    ***
       I can't test this -
       Get Request failed with 404 Client Error: Not Found for url:
    ***

    :param Scope:     String "Device" or "System"

    :param DeviceId:  String "0" .. "65535"

    :return:
    """
    dataRq ='/solar_api/v1/GetStorageRealtimeData.cgi?Scope='+Scope+'&DeviceId='+DeviceId
    return getData(hostname, dataRq)


def GetOhmPilotRealtimeData(Scope='Device',DeviceId='0'):
    """
    This request provides detailed information about OhmPilot. Inactive channels
    are not included in the response and may vary depended on used hardware and
    software version. Take care about permanently or temporary missing channels
    when processing this response.

    :param Scope:     String "Device" or "System"

    :param DeviceId:  String "0" .. "65535"

    """
    dataRq = '/solar_api/v1/GetOhmPilotRealtimeData.cgi?Scope=' + Scope + '&DeviceId=' + DeviceId
    return getData(hostname, dataRq)



def GetArchiveData(startDate,endDate):
    """
    Archive requests shall be provided whenever access to historic device-data
    is possible and it makes sense to provide such a request.

    Of course, the Datalogger Web can only provide what is stored in its internal
    memory and has not been overwritten by newer data yet. It can loose data,
    due to capacity reason. The number of days stored dependence on the
    number of connected units to log. This limitation of is not present
    for Solar.web, provided that the Datalogger has reliably uploaded the data.
    The Request is populated with All Possible parameters by default.
    """

    dataRq = "/solar_api/v1/GetArchiveData.cgi?Scope=System&SeriesType=Detail&HumanReadable=True&StartDate=1.9.2017&EndDate=3.9.2017&Channel=TimeSpanInSec&Channel=Digital_PowerManagementRelay_Out_1&Channel=EnergyReal_WAC_Sum_Produced&Channel=InverterEvents&Channel=InverterErrors&Channel=Current_DC_String_1&Channel=Current_DC_String_2&Channel=Voltage_DC_String_1&Channel=Voltage_DC_String_2&Channel=Temperature_Powerstage&Channel=Voltage_AC_Phase_1&Channel=Voltage_AC_Phase_2&Channel=Voltage_AC_Phase_3&Channel=Current_AC_Phase_1&Channel=Current_AC_Phase_2&Channel=Current_AC_Phase_3&Channel=PowerReal_PAC_Sum&Channel=EnergyReal_WAC_Minus_Absolute&Channel=EnergyReal_WAC_Plus_Absolute&Channel=Meter_Location_Current&Channel=Temperature_Channel_1&Channel=Temperature_Channel_2&Channel=Digital_Channel_1&Channel=Digital_Channel_2&Channel=Radiation&Channel=Digital_PowerManagementRelay_Out_1&"
    return getData(hostname,dataRq)

def GetPowerFlowRealtimeData():
    """
    This request provides detailed information about the local energy grid.
    The values replied represent the current state. Because of data has multiple
    asynchrone origins it is a matter of facts that the sum of all
    powers (grid, load and generate) will differ from zero.
    """
    dataRq = '/solar_api/v1/GetPowerFlowRealtimeData.fcgi'
    return getData(hostname,dataRq)

def PowerFlowRealtimeData(jPFRD):
# Collect the Inverter Data
# Does not include Optional Fields at this time
    Inverters = dict()
    Site = dict()
# There could be more than 1 inverter here -  Bitcoin Miners :)
    for i in jPFRD['Body']['Data']['Inverters']:
        for i in jPFRD['Body']['Data']['Inverters']:
            Inverters['DeviceId'] = i
            Inverters['Version'] = jPFRD['Body']['Data']['Version']
            Inverters['Timestamp'] = jPFRD['Head']['Timestamp']
            Inverters['DT'] = jPFRD['Body']['Data']['Inverters'][i]['DT']
            Inverters['E_Day'] = jPFRD['Body']['Data']['Inverters'][i]['E_Day']
            Inverters['E_Total'] = jPFRD['Body']['Data']['Inverters'][i]['E_Total']
            Inverters['E_Year'] = jPFRD['Body']['Data']['Inverters'][i]['E_Year']
            Inverters['P'] = jPFRD['Body']['Data']['Inverters'][i]['P']

# Collect Site data (single row)
        Site['Timestamp'] = jPFRD['Head']['Timestamp']
        Site['Version'] = jPFRD['Body']['Data']['Version']
        Site['E_Day'] = jPFRD['Body']['Data']['Site']['E_Day']
        Site['E_Total'] = jPFRD['Body']['Data']['Site']['E_Total']
        Site['E_Year'] = jPFRD['Body']['Data']['Site']['E_Year']
        Site['Meter_Location'] = jPFRD['Body']['Data']['Site']['Meter_Location']
        Site['Mode'] = jPFRD['Body']['Data']['Site']['Mode']
        Site['P_Akku'] = jPFRD['Body']['Data']['Site']['P_Akku']
        Site['P_Grid'] = jPFRD['Body']['Data']['Site']['P_Grid']
        Site['P_Load'] = jPFRD['Body']['Data']['Site']['P_Load']
        Site['P_PV'] = jPFRD['Body']['Data']['Site']['P_PV']
        Site['rel_Autonomy'] = jPFRD['Body']['Data']['Site']['rel_Autonomy']
        Site['rel_SelfConsumption'] = jPFRD['Body']['Data']['Site']['rel_SelfConsumption']
    return [Site, Inverters]

### Just Initial Testing Code
def testPowerFlowRealtimeData():
    pp = pprint.PrettyPrinter(indent=4)
    cnt = 0
    while cnt < 10:
        cnt = cnt + 1
        Site, Inverters = PowerFlowRealtimeData(GetPowerFlowRealtimeData())
        pp.pprint(Site)
        pp.pprint(Inverters)
        time.sleep(10)



#testPowerFlowRealtimeData()

#jArchiveData = getArchiveData('1.9.2017','30.12.2017')
#jPowerFLowRealtimeData = GetPowerFlowRealtimeData()
#Site, Inverters = PowerFlowRealtimeData(jPowerFLowRealtimeData)
#jDeviceInfo = GetActiveDeviceInfo('Inverter')
#jInverterRealtimeData = GetInverterRealtimeData()
#jSensorRealtimeData = GetSensorRealtimeData()
#jStringRealtimeData = GetStringRealtimeData(DataCollection='LastErrorStringControlData')
#jStringRealtimeData = GetStringRealtimeData(DataCollection='CurrentSumStringControlData')
jLoggerInfo = GetLoggerInfo()
#jLoggerLEDInfo = GetLoggerLEDInfo()
#jInverterInfo = GetInverterInfo()

#for i in range(1,20):
#    print(InverterInfoStatusCode(i))

#jMeterRealtimeData = GetMeterRealtimeData(Scope='System')
#jStorageRealtimeData = GetStorageRealtimeData(Scope='System')
#jOhmPilotRealtimeData = GetOhmPilotRealtimeData(Scope='System')
#jPowerFlowRealtimeData = GetPowerFlowRealtimeData()
print('Done')

