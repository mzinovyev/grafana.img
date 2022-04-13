# -*- coding: UTF-8 -*-
import datetime
import urllib3
import re
import os
import sys
import argparse
from configparser import RawConfigParser
import json

myurl = 'http://osa-web-v001t4.test.local:3000/render/d-solo/4Uw1Zrc7k/mssql_dashboard?from=1647449485228&to=1647453085228&orgId=1&panelId=9&width=1000&height=500&tz=Europe%2FMoscow'
#


def create_parser():
    '''Params for help and parsing args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--section', help="название секции ini, например KBD, содержащей списки панелей grafana", required=True)
    parser.add_argument('-f', '--from_date', help="начало временного интервала в формате YYYY, с английсокй 'T' середине, например 2022-03-16T11:05:00", required=True)
    parser.add_argument('-t', '--to_date', help="окончание временного интервала в формате YYYY, с английсокй 'T' середине, например 2022-03-16T11:05:00", required=True)
    return parser

def parameterize_url(url, from_date_str, to_date_str, section_key):
    '''Add to url resolution of image & datetime interval'''
    from_date = datetime.datetime.fromisoformat(from_date_str)
    to_date = datetime.datetime.fromisoformat(to_date_str)
    from_unix = datetime.datetime.timestamp(from_date)*1000
    to_unix = datetime.datetime.timestamp(to_date)*1000
    range = "?from=%s&to=%s" % (str(from_unix)[:-2], str(to_unix)[:-2])
    width = re.search('.*_(.+?)_\d+$', section_key).group(1)
    height = re.search('.*_\d+_(.+?)$', section_key).group(1)
    resolution = "width=%s&height=%s" % (width, height)
    newstring = re.sub(r'\?from=\d+\&to=\d+', range, url)
    newstring = re.sub(r'width=\d+\&height=\d+', resolution, newstring)
    return newstring

def get_file_path(section, section_key, from_str, to_str):
    '''Create filepath from section & section_key. Ex: KBD\\mysql_mem_2022-03-16T11:05:00__2022-03-16T11:05:00.PNG'''
    file_name = re.search('(.+?)_\d+_\d+', section_key).group(1) #
    filepath = "%s\\%s_%s__%s.png" % (section, file_name, from_str.replace(':','.'), to_str.replace(':','.'))
    return filepath

def create_start_img_url(json_data, system):
    '''Creating first part of url 2 download image'''
    start_img_url = json_data.get("meta").get("base_url")
    return start_img_url

if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    section = namespace.section # название системы и каталога

    # read json file
    json_data = {}
    with open("settings.json", "r") as jsf:
        json_data = json.load(jsf)

    # get list of presets of dushboardsv(oracle, weblogic etc)
    preset_list = json_data.get("dashboard").keys()

    #cycle for preset_list
    preset_found_flag = False
    for preset in preset_list:
        if preset == section:
            preset_found_flag = True
        if not preset_found_flag:
            print ("Cant find system $s at settings.json" % (section))
            break
        #make folder for preset 2 save images
    #ini = RawConfigParser()
    #ini.read('get.images.ini')

    # Prepare request
    http = urllib3.PoolManager()
    headers = urllib3.util.make_headers(basic_auth='zinovev.mn:Il_NarDep456')

    # save all urls for section


    url = "https://grafana.test.local/api/search?folderIds=202&query=&starred=false"
    url_1 = "https://grafana.test.local/api/dashboards/uid/ATh0RNL7k"


    # curl - s - H
    # "Authorization: Bearer ${KEY}" \
    # "${YOUR-GRAFANA-URL}/api/dashboards/uid/${DASH-UID}" | \
    # jq
    # '.dashboard.panels[].id'

    resp = http.request('GET', url_1, headers=headers)
    with open('some_url1.json', 'wb') as f:
        f.write(resp.data)
   # for key in ini[section]:
   #      if not os.path.isdir(section):
   #          os.makedirs(section)
   #
   #      url = ini[section].get(key)
   #      url = parameterize_url(url, namespace.from_date, namespace.to_date, key)
   #      resp = http.request('GET', url, headers=headers)
   #
   #      file_name = get_file_path(section, key, namespace.from_date, namespace.to_date)
   #      with open(file_name, "wb") as f:
   #          f.write(resp.data)

   #make search for PL folder