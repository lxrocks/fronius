import requests
import pprint
import time
import pandas as pd
import sqlite3

# collector.py
# This will connect to the Fronius Symo and log data to a sqlite
# database
# Make sure you add ip.ip.ip.ip fronius to your /etc/hosts file or
# Set the variable hostname to your Symo's ip address or hostname
#
# This will create a sqlite db called fronius.sqlite and add
# two tables called Site & Inverters
# It will then start logging data every 5 seconds
# Todo:
# 1. Error Handling
# 2. CLean up exit - use a signal handler or something


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
def TestPowerFlowRealtimeData():
    pp = pprint.PrettyPrinter(indent=4)
    cnt = 0
    while cnt < 3:
        cnt = cnt + 1
        Site, Inverters = PowerFlowRealtimeData(GetPowerFlowRealtimeData())
        pp.pprint(Site)
        pp.pprint(Inverters)
        time.sleep(3)




def initSQL():
    cn = sqlite3.connect("Fronius.sqlite")
    return cn




def InitPowerFlowRealtimeData(cn):

    # Setup
    # Initialise the DataFrames use pandas to setUp the tables initially
    # This is being lazy, build a proper CREATE

    Site, Inverters = PowerFlowRealtimeData(GetPowerFlowRealtimeData())
    dSite = pd.DataFrame(data=Site,index=[0])
    dSite.reset_index()
    dInverters = pd.DataFrame(data=Inverters,index=[0])
    dInverters.reset_index()
    
    dSite.to_sql("Site",cn,if_exists="append")
    dInverters.to_sql("Inverters",cn,if_exists="append")
    return [dSite, dInverters]




def writeSQL(cn,cur,table,row):
    columns = ', '.join(row.keys())
    placeholders = ':'+', :'.join(row.keys())
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (table,columns, placeholders)
    cur.execute(query, row)
    cn.commit()




def main():
    cn = initSQL()
    cur = cn.cursor()
    dSite, dInverters = InitPowerFlowRealtimeData(cn)
    while True:
        try:
            Site, Inverters = PowerFlowRealtimeData(GetPowerFlowRealtimeData())
            writeSQL(cn,cur,table="Site",row=Site)
            writeSQL(cn,cur,table="Inverters",row=Inverters)
            # Loop every 5 seconds
            time.sleep(5)
        except:
            time.sleep(60)
            print("sleeping")
    cn.close()
        




if __name__ == "__main__":
    main()



#pd.read_sql_query("SELECT * from Inverters", cn)
#pd.read_sql_query("SELECT * from Site", cn)

