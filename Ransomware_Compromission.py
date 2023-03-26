import pandas as pd
import datetime
from googlesearch import search
import re
import os
from tld import get_tld
import argparse
import zipfile


def creation_Dataframe_Ransom(url):
    df = pd.read_json(url)
    now = datetime.datetime.now()
    yesterday_date= datetime.datetime.now() - datetime.timedelta(days=1)
    df = df.loc[df["discovered"].between(str(yesterday_date), str(now))]
    df = df.reset_index(drop=True)
    return df

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help = "the number of days difference")
    args=parser.parse_args()
    return args

def url_Creation(dataframe_Ransom,list_Url):
    Url_Pattern_No_HTTP = re.compile('^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$')
    Url_Pattern_With_HTTP = re.compile('^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$')
    for Victim in dataframe_Ransom['post_title']:
        if Url_Pattern_No_HTTP.match(str(Victim)):
            list_Url.append(Victim)
        elif Url_Pattern_With_HTTP.match(str(Victim)):
            list_Url.append(Victim)        
        else:
            for j in search(Victim, num=1, stop=1, pause=2):
                list_Url.append(j)
    dataframe_Ransom["url_of_website"] = list_Url

def country_Creation(dataframe_Ransom, list_Country):
    tld_df = pd.read_json("tld.json")
    list_tld=[]
    list_Country=[]
    list_sld=['gov.',"edu.","ac.","in.","co.","com.","im."]
    url_Pattern_No_HTTP = re.compile('^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$')
    url_Pattern_With_HTTP = re.compile('^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$')
    for url_Victim in dataframe_Ransom['url_of_website']:
        if url_Pattern_No_HTTP.match(str(url_Victim)):
            list_tld.append(get_tld(url_Victim, fix_protocol=True))
        elif url_Pattern_With_HTTP.match(str(url_Victim)):
            list_tld.append(get_tld(url_Victim))

    dataframe_Ransom["TLD"] = pd.Series(list_tld)
    for tld in dataframe_Ransom['TLD']:
        for i in list_sld:
            if i in tld:
                tld=tld.replace(i,"")
        for i in range(len(tld_df)):
            if tld == tld_df['tlds'][i]:
                list_Country.append(tld_df['country'][i])
    dataframe_Ransom["Country"] = pd.Series(list_Country)

def output_Creation(dataframe_Ransom):
    var1="Ransomware_"
    date= datetime.datetime.now()
    date_formatted=date.strftime("%d_%m_%Y")
    dataframe_Ransom.to_csv(f'{var1}{date_formatted}.csv')
    dataframe_Ransom.to_excel(f'{var1}{date_formatted}.xlsx')
    zfile = zipfile.ZipFile(f'{var1}{date_formatted}.zip', 'w')
    zfile.write(f'{var1}{date_formatted}.csv')
    zfile.write(f'{var1}{date_formatted}.xlsx')
    zfile.close()
    os.remove(f'{var1}{date_formatted}.xlsx')
    os.remove(f'{var1}{date_formatted}.csv')

def misc():
    os.remove(".google-cookie")

def main():
    url = "https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json"
    url_List = []
    Dataframe_Ransom=creation_Dataframe_Ransom(url)
    url_Creation(Dataframe_Ransom,url_List)
    output_Creation(Dataframe_Ransom)
    misc()

if __name__ == "__main__":
    main()
