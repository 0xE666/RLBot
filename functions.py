import requests
import json
import re

def searchPlayer(platform, player):
    global playerName
    global profileViews
    global seasonRewards
    global avatar
    global unranked
    global duel
    global doubles
    global standard
    global hoops
    global rumble
    global dropshot
    global snowday

    data = parseData(platform, player)
    try:
        playerName = data['Player Search']['Player']['Player Name']
        profileViews = data['Player Search']['Player']['Profile Views']
        seasonRewards = data['Player Search']['Player']['Season Rewards']
        avatar = data['Player Search']['Player']['Avatar']
        duel = f"{data['Player Search']['Ranks']['Ranked Duel 1v1']}\nMMR: {data['Player Search']['Ranks']['Ranked Duel 1v1 MMR']}\nStreak: {data['Player Search']['Ranks']['Ranked Duel 1v1 Streak']}"
        doubles = f"{data['Player Search']['Ranks']['Ranked Doubles 2v2']}\nMMR: {data['Player Search']['Ranks']['Ranked Doubles 2v2 MMR']}\nStreak: {data['Player Search']['Ranks']['Ranked Doubles 2v2 Streak']}"
        standard = f"{data['Player Search']['Ranks']['Ranked Standard 3v3']}\nMMR: {data['Player Search']['Ranks']['Ranked Standard 3v3 MMR']}\nStreak: {data['Player Search']['Ranks']['Ranked Standard 3v3 Streak']}"
        hoops = f"{data['Player Search']['Ranks']['Hoops']}\nMMR: {data['Player Search']['Ranks']['Hoops MMR']}\nStreak: {data['Player Search']['Ranks']['Hoops Streak']}"
        rumble = f"{data['Player Search']['Ranks']['Rumble']}\nMMR: {data['Player Search']['Ranks']['Rumble MMR']}\nStreak: {data['Player Search']['Ranks']['Rumble Streak']}"
        dropshot = f"{data['Player Search']['Ranks']['Dropshot']}\nMMR: {data['Player Search']['Ranks']['Dropshot MMR']}\nStreak: {data['Player Search']['Ranks']['Dropshot Streak']}"
        snowday = f"{data['Player Search']['Ranks']['Snowday']}\nMMR: {data['Player Search']['Ranks']['Snowday MMR']}\nStreak: {data['Player Search']['Ranks']['Snowday Streak']}"
    except Exception as ex:
        print(ex)

def getData(platform, player):
    url = f"https://api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{player}"
    header = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en",
        "referrer": "https://rocketleague.tracker.network/rocket-league/live",
        "referrerPolicy": "no-referrer-when-downgrade",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    data = requests.get(url, headers=header)
    return data.json()

def parseData(platform, player):
    mainJson = {"Player Search":{}}
    jsonData = {"Ranks":{}}

    data = getData(platform, player)
    playerName = data['data']['platformInfo']['platformUserHandle']
    avatar = data['data']['platformInfo']['avatarUrl']
    seasonReward = data['data']['segments'][0]['stats']['seasonRewardLevel']['metadata']['rankName']
    visits = data['data']['userInfo']['pageviews']
    player = {f"Player":{
        "Player Name": f"{playerName}",
        "Profile Views": f"{visits}",
        "Season Rewards": f"{seasonReward}",
        "Avatar": f"{avatar}"
        }}
    mainJson['Player Search'].update(player)

    try:
        for i in range(len(data['data']['segments'])):
            if i < 1:
                pass
            else:
                if data['data']['segments'][i]['stats']['tier']['metadata']['name'] == 'Unranked':
                    rank = {
                        f"{data['data']['segments'][i]['metadata']['name']}": f"{data['data']['segments'][i]['stats']['tier']['metadata']['name']}",
                        f"{data['data']['segments'][i]['metadata']['name']} MMR": f"{data['data']['segments'][i]['stats']['rating']['value']}",
                        f"{data['data']['segments'][i]['metadata']['name']} Streak": f"{data['data']['segments'][i]['stats']['winStreak']['displayValue']}",
                        f"{data['data']['segments'][i]['metadata']['name']} Icon": f"{data['data']['segments'][i]['stats']['tier']['metadata']['iconUrl']}"
                        }
                    jsonData['Ranks'].update(rank)
                else:
                    rank = {
                        f"{data['data']['segments'][i]['metadata']['name']}": f"{data['data']['segments'][i]['stats']['tier']['metadata']['name']} {data['data']['segments'][i]['stats']['division']['metadata']['name']}",
                        f"{data['data']['segments'][i]['metadata']['name']} MMR": f"{data['data']['segments'][i]['stats']['rating']['value']}",
                        f"{data['data']['segments'][i]['metadata']['name']} Streak": f"{data['data']['segments'][i]['stats']['winStreak']['displayValue']}",
                        f"{data['data']['segments'][i]['metadata']['name']} Icon": f"{data['data']['segments'][i]['stats']['tier']['metadata']['iconUrl']}"
                        }
                    jsonData['Ranks'].update(rank)

        mainJson['Player Search'].update(jsonData)           
        return mainJson

    except Exception as ex:
        print(ex)

def searchItem(item):
    url = 'https://rl.insider.gg/api/itemSearchEngine'

    if '-' in item:
        item = item.split(' -')
        itemName = item[0]
        itemType = item[1]
        data = '{"languageID":0,"query":"' + itemName + '"}'
    else:
        data = '{"languageID":0,"query":"' + item + '"}'
        
    headers = {
        'cookie': '__cfduid=d5ee8d22f941171fd6104ee218383efee1616945745; lang=en; ts=1616945745; theme=aquadome; platform=pc; _ga=GA1.2.1828776129.1616945737; _ym_d=1616945739; _ym_uid=161694573923064821; _pbjs_userid_consent_data=3524755945110770; pbjs-unifiedid=%7B%22TDID%22%3A%22c3db6e0e-0206-4833-b185-1762b850fbf5%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-02-28T15%3A35%3A51%22%7D; __gads=ID=0bd22448b2bd3995:T=1616945756:S=ALNI_MZFKF_9SKxklLsGaODwq4ey6X4JlQ; cookieconsent_status=dismiss; pricesPageSorting=5; _gid=GA1.2.1221637917.1617875573; _ym_isad=1; sharedid=%7B%22id%22%3A%2201F1NR11CV9BFVNRF0MTF124M0%22%2C%22ts%22%3A1617875581646%7D; pbjs-id5id=%7B%22created_at%22%3A%222021-03-28T15%3A35%3A51Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5-ZHMOZ74NBi9jjKJ2SROvr6mIRigL_6aDm25lyJx75g!%22%2C%22universal_uid%22%3A%22ID5-ZHMOjapLxtxrh2xR_eplhE8uC4x0LB01rIk-zcIbVw!%22%2C%22signature%22%3A%22ID5_Acc0CnX2i2IvqzQt3xtyCSQTC_osyHwGvHo_jJ2z_VNdGwqf1GPhk9fZTY8b83zLdaRI8Vwoic0q2Dn-KI_O4O0%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%7D; pbjs-id5id_last=Thu%2C%2008%20Apr%202021%2009%3A53%3A01%20GMT; _gat_gtag_UA_110569829_1=1',
        'content-type': 'text/plain;charset=UTF-8',
        'content-length': str(len(data)),
    }
    r1 = requests.post(url, headers=headers, data=data).content.decode('utf8').split('\n')[1]
    resp = json.loads(r1)
    if 'options' in resp:
        if itemType:
            for i in range(len(resp['options'])):
                if itemType.capitalize() in resp['options'][i]['itemName']:
                    itemEndpoint = resp['options'][i]['uri']
                    itemPic = resp['options'][i]['pictureURL']
                    itemUrl = 'https://rl.insider.gg/en/pc' + itemEndpoint
                    return itemUrl, itemPic
        else:
            option = []
            for i in range(len(resp['options'])):
                option.append(resp['options'][i])
            return 'options', option
    else:
        itemEndpoint = resp['uri']
        itemPic = resp['pictureURL']
        itemUrl = 'https://rl.insider.gg/en/pc' + itemEndpoint
        return itemUrl, itemPic

def grabItem(item):
    colorList = ['Titanium White', 'Black', 'Grey', 'Crimson', 'Pink', 'Cobalt', 'Sky Blue', 'Burnt Sienna', 'Saffron', 'Lime', 'Green', 'Orange', 'Purple']

    itemUrl, itemPic = searchItem(item)
    if 'options' in itemUrl:
        return itemUrl, itemPic
    else:
        r2 = requests.get(itemUrl).content.decode('utf8')
        itemDataPattern = 'var itemData = (.*?)"itemHistory'
        itemPricePattern = 'itemName":"(.*?)","itemColor":"(.*?)".{1,500}currentPriceRange":"(.*?)",'
        reg1 = re.findall(itemDataPattern, r2)
        reg2 = re.findall(itemPricePattern, reg1[0])
        
        if reg2[0][1] not in colorList or reg2[0][1] == 'Default':
            itemName = reg2[0][0]
        else:
            itemName = reg2[0][1] + ' ' + reg2[0][0]
        itemPrice = reg2[0][2]

        return itemUrl, itemPic, itemName, itemPrice