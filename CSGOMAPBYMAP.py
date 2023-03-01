from __future__ import print_function
from google.auth.transport.requests import Request
from lxml import html
import requests
import csv
from datetime import date
from dateutil.relativedelta import relativedelta
import time
import random

endDate = date.today()
startDate = endDate - relativedelta(months=+3)
startDate1M = endDate - relativedelta(months=+1)

filename = "CSGOMAPBYMAPdata.csv"

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)


### COPY COLUMN C FROM SHEET: "SCRIPT COPY" ###
    players = [
'14495/droid',
'19709/shane',
'19710/dare',
'19711/snav',
'20213/intra',
'11163/trk',
'11617/malbsmd',
'2529/maluk3',
'17553/pesadelo',
'10818/idk',
'22069/grizz',
'21665/jba',
'20233/scar',
'20572/kmrn',
'19887/makzwell',
'19128/slight',
'14799/brett',
'15176/cryptic',
'18090/micro',
'18706/freshie',
'14494/junior',
'8507/stanislaw',
'7805/rush',
'17929/walco',
'20333/jeorge',
'16546/cynic',
'16647/bwills',
'10892/marke',
'17918/nosrac',
'9571/cj',
'17353/cxzi',
'20630/silas',
'19705/chop',
'19177/consti',
'20934/tender',
'16893/stamina',
'17510/j0lz',
'13229/snakes',
'14619/infinite',
'16470/aris',]

    for player in players:

        headshotContent = requests.get("https://www.hltv.org/stats/players/"+player+"?startDate="+str(startDate)+"&endDate="+str(endDate))
        tree2 = html.fromstring(headshotContent.content)

        #player_hs = "/html/body/div[2]/div[5]/div[2]/div[1]/div/div[8]/div/div[1]/div[2]/span[2]/text()" 
        player_hs = "/html/body/div[2]/div[5]/div[2]/div[1]/div[2]/div[9]/div/div[1]/div[2]/span[2]/text()"
        #player_hs = /html/body/div[2]/div[5]/div[2]/div[1]/div[2]/div[9]/div/div[1]/div[2]/span[2]
                    
        player_headshots_temp = tree2.xpath(player_hs)[0].strip()
        player_headshots_2 = player_headshots_temp.split("%")[0]
        player_headshots = float(player_headshots_2)/100

        pageContent=requests.get("https://www.hltv.org/stats/players/matches/"+player+"?startDate="+str(startDate)+"&endDate="+str(endDate))
        tree = html.fromstring(pageContent.content)

        ### Get player name ###
        #player_name = "/html/body/div[2]/div[5]/div[2]/div[2]/div[1]/div[1]/div[2]/div/div/span/text()"
        player_name = "/html/body/div[2]/div[5]/div[2]/div[2]/div[1]/div[1]/div[2]/div/div/span/text()"
        #player_name = /html/body/div[2]/div[5]/div[2]/div[2]/div/div[1]/div[2]/div/div/span
                    
        player_name_pulled = tree.xpath(player_name)[0]
        #.split(" ")[3]
        print("player: ", player_name_pulled)
        player_name_fixed = player_name_pulled.replace("ś","s")

        rounds_won_array = []
        rounds_lost_array = []
        kills_array = []
        match_date_array = []
        team_array = []

        i = 1
        while i < 500:
            try:
                team = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[2]/div[1]/a/span/text()"
		#team = /html/body/div[2]/div[5]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/div[1]/a/span

                       
                team_pulled = tree.xpath(team)[0].strip()
                team_array.append(team_pulled)

                #rounds_won = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[2]/div[1]/span/text()"
                rounds_won = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[2]/div[1]/span/text()"
                #rounds_won = /html/body/div[2]/div[5]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/div[1]/span
                             
                rounds_won_pulled = tree.xpath(rounds_won)[0].strip(" (").strip(")").strip()
                rounds_won_array.append(rounds_won_pulled)

                #rounds_lost = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[3]/div[1]/span/text()"
                rounds_lost = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[3]/div[1]/span/text()"
                #rounds_lost = /html/body/div[2]/div[1]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[3]/div[1]/span
                              
                rounds_lost_pulled = tree.xpath(rounds_lost)[0].strip(" (").strip(")").strip()
                rounds_lost_array.append(rounds_lost_pulled)

                #kills = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[5]/text()"
                kills = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[5]/text()"
                #kills = /html/body/div[2]/div[1]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[5]
                        
                kills_pulled = tree.xpath(kills)[0].strip(" (").strip(")").strip()
                kills_final = kills_pulled.split("-")[0].strip()
                kills_array.append(kills_final)

                #match_date = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[1]/a/div/text()"
                match_date = "/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tbody/tr["+str(i)+"]/td[1]/a/div/text()"
                #match_date = /html/body/div[2]/div[1]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]
                             
                match_date_pulled = tree.xpath(match_date)[0].strip(" (").strip(")").strip()
                match_date_array.append(match_date_pulled)

                i += 1
                j = i-1
            except Exception:
                break

        y = random.randint(4,7)
        time.sleep(y)
        print ('Sleep for: ', y, ' seconds. ')

        x = 0
        while x < j:
            try:
                temp = [player_name_fixed,kills_array[x],rounds_won_array[x],rounds_lost_array[x],match_date_array[x],team_array[x],player_headshots]
                csvwriter.writerow(temp)
                x += 1
            except Exception:
                break
