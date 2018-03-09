import requests, time, json
from configBot import *
headersKore = {"content-type": "application/json;charset=UTF-8"}


def builderStreams1(Input, userIdKore, authTokenKore, KorePlatform):
        url = KorePlatform+"/api/1.1/users/"+userIdKore+"/builder/streams"#Calling the builder Api for Kore
        payload = "{\"name\":\""+Input+"\",\"type\":\"taskbot\",\"description\":\"drfgd\",\"color\":\"#FF7A00\",\"categoryIds\":[\"451902a073c071463e2fe7f6\"],\"skipMakeEditLinks\":false,\"purpose\":\"customer\",\"errorCodes\":{\"pollError\":[]},\"visibility\":{\"namespace\":[],\"namespaceIds\":[]},\"defaultLanguage\":\"en\"}"
        try:
                response = requests.post(url, data=payload, headers=headersKore)
                streamid=response.json()['_id']
                name=response.json()['name']
                #print("builder streams 1", response.text)
        except:
                raise Exception("Error while creating builder streams")        
        return name,streamid

def builderStreams1_5(Input, userIdKore, authTokenKore, KorePlatform):
        url = "http://localhost/api/1.1/users/"++"/builder/streams"
        querystring = {"rnd":"9in6m"}
        response = requests.get( url, headers=headers, params=querystring)
        print(response.text)

def marketStreams1(Input, userIdKore, authTokenKore, KorePlatform, name, streamid):
        url1 = KorePlatform+"/api/1.1/market/streams"#Calling the Market streams Api
        if KorePlatform.split("//")[1].split(".")[0] == "pilot-bots":
            icon = "59c0f641da89738e6f467d82"
        elif KorePlatform.split("//")[1].split(".")[0] == "bots":
            icon = "5aa1181126295e40159f6bd7"
        elif KorePlatform.split("//")[1].split(".")[0] == "localhost":
            icon = "5aa1163a7776c04cd2b37f3c"
        else:
            icon = "58d2376ab99576e94c2daf2c"
        payload1 = "{\"_id\":\""+streamid+"\",\"name\":\""+name+"\",\"description\":\"faq\",\"categoryIds\":[\"451902a073c071463e2fe7f6\"],\"icon\":\""+icon+"\",\"keywords\":[],\"languages\":[],\"price\":1,\"screenShots\":[],\"namespace\":\"private\",\"namespaceIds\":[],\"color\":\"#3AB961\",\"bBanner\":\"\",\"sBanner\":\"\",\"bBannerColor\":\"#3AB961\",\"sBannerColor\":\"#3AB961\",\"profileRequired\":true,\"sendVcf\":false}"
        try:
                response1 = requests.post(url1, data=payload1, headers=headersKore)
                response1.raise_for_status()
                #print("market streams 1",response1.text)
        except Exception as e:
                raise Exception("Error while creating Market streams"+str(e))

def builderStreams2(Input, userIdKore, authTokenKore, KorePlatform, streamid):
        url = KorePlatform+"/api/1.1/builder/streams/"+streamid+"/dialogs"
        querystring = {"rnd":"7hl7dm"}
        try:
                response = requests.get(url, headers=headersKore, params=querystring)
                response.raise_for_status()
                #print("builderstreams 2",response.text)
        except:
                raise Exception("Error while creating Setting Default dialog task streams")

def builderStreams3(Input, userIdKore, authTokenKore, KorePlatform, streamid, dgValue):
        url = KorePlatform+"/api/1.1/builder/streams/"+streamid+"/defaultDialogSettings"
        #Setting the Default Dialog Task to Default Fallback Intent. 
        querystring = {"rnd":"jw4tcv"}
        payload = "{\"defaultDialogId\":\""+dgValue[1]+"\"}"
        try:
                response = requests.put(url, data=payload, headers=headersKore, params=querystring)
                response.raise_for_status()
        except:
                print("RESP post",response)
                raise Exception("Error while creating Setting Default dialog task streams")        

def getAccountId(userIdKore, authTokenKore, KorePlatform):

    url = KorePlatform+"/api/1.1/users/"+userIdKore+"/AppControlList"
    headers = {
    'authorization': authTokenKore,
    'bot-language': "en",
    'content-type': "application/json",
    }
    response = requests.get( url, headers=headers)
    response = json.loads(response.text)
    #print(response.text)
    ret =  response["associatedAccounts"][0]["accountId"]
    return ret

def createKoreBot(Input, userIdKore, authTokenKore, KorePlatform):
        headersKore['host']= "localhost"
        headersKore['user-agent']= "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        headersKore['accept']= "application/json, text/plain, */*"
        headersKore['accept-language']= "en-US,en;q=0.5"
        headersKore['referer']= "http://localhost/botbuilder"
        headersKore['authorization']= authTokenKore
        headersKore['bot-language']= "en"
        headersKore['accountid']= getAccountId(userIdKore,authTokenKore,KorePlatform)
        name, streamid = builderStreams1(Input, userIdKore, authTokenKore, KorePlatform)

        marketStreams1(Input, userIdKore, authTokenKore, KorePlatform, name, streamid)
        dgValue = addIntentKore('Default Fallback Intent',streamid,userIdKore,authTokenKore,KorePlatform)

        builderStreams2(Input, userIdKore, authTokenKore, KorePlatform, streamid)
        builderStreams3(Input, userIdKore, authTokenKore, KorePlatform, streamid, dgValue)


        return streamid, dgValue

def addIntentKore(Input,streamid,userIdKore,authTokenKore,KorePlatform):
        querystring = {"rnd":"tjywhl"}

        url = KorePlatform+"/api/1.1/builder/streams/"+streamid+"/components"
        payload = json.dumps({"desc":"","type":"intent","intent":Input})
        try:
                response = requests.post( url+"?rnd=h3uyn", data=payload, headers=headersKore)
                response.raise_for_status()
                name=response.json()['name']
                component=response.json()['_id']
        except:
                print(response.text, Input)
                raise Exception("Error while Adding intent to kore 1")


        url2 = KorePlatform+"/api/1.1/builder/streams/"+streamid+"/dialogs"
        payload2 = "{\"name\":\""+name+"\",\"shortDesc\":\"News updates\",\"nodes\":[{\"nodeId\":\"intent0\",\"type\":\"intent\",\"componentId\":\""+component+"\",\"transitions\":[{\"default\":\"\",\"metadata\":{\"color\":\"#f3a261\",\"connId\":\"dummy0\"}}],\"metadata\":{\"left\":30,\"top\":170}}],\"visibility\":{\"namespace\":\"private\",\"namespaceIds\":[\"\"]}}"
        try:
                response2 = requests.post( url2, data=payload2, headers=headersKore)
                name=response2.json()['name']
                dialogId=response2.json()['_id']
        except:
                raise Exception("Error while Adding intent to kore 2")


        url3 = KorePlatform+"/api/1.1/builder/streams/"+streamid+"/components/"+component+""
        payload3 = "{\"name\":\""+name+"\",\"dialogId\":\""+dialogId+"\"}"
        try:
                response3 = requests.put(url3, data=payload3, headers=headersKore)
        except:
                raise Exception("Error while Adding intent to kore 3")

        idKores=[component,dialogId]

        payload = {"name":"ResponseFor"+Input.replace(" ",""),"type":"message","message":[{"channel":"default","text":Input+" has been recognized.","type":"basic"}]}
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headersKore)
            response.raise_for_status()
            msgId=response.json()['_id']
            idKores+=[msgId]
        except Exception as e:
                print(e)
                print(url, payload)
                raise Exception("Error while Adding intent to kore 4")

        url4 = KorePlatform+"/api/1.1/builder/streams/"+streamid+"/dialogs/"+dialogId
        payload ={"streamId":streamid,"name":name,"nodes":[{"nodeId":"intent0","type":"intent","componentId":component,"transitions":[{"default":"message1","metadata":{"color":"#299d8e","connId":"dummy0"}}],"metadata":{"left":21,"top":20},"nodeOptions":{"transitionType":"auto"}},{"nodeId":"message1","type":"message","componentId":msgId,"transitions":[{"default":"message1","metadata":{"color":"#299d8e","connId":"dummy1"}}],"nodeOptions":{"transitionType":"auto"}}],"visibility":{"namespaceIds":[userIdKore],"namespace":"private"}}
        response = requests.put(url4, data=json.dumps(payload), headers=headersKore)
        return idKores

def addKoreUtterances(Input, idKore, streamid, intentid, userIdKore, authTokenKore, KorePlatform):
        url = KorePlatform+"/api/1.1/users/"+userIdKore+"/builder/sentences"
        #payload = "{\"taskId\":\""+idKore+"\",\"sentence\":\""+Input+"\",\"streamId\":\""+streamid+"\",\"taskName\":\""+intentid+"\",\"type\":\"DialogIntent\"}"
        payload = json.dumps({"taskId":idKore,"sentence":Input,"streamId":streamid,"taskName":intentid,"type":"DialogIntent"})
        while 1:
            try:
                response = requests.post( url, data=payload, headers=headersKore)
                if response.status_code==409: break
                response.raise_for_status()
            except:
                print("Error while adding training Utterances")
                if not 'response' in locals(): response={}
                else: print("addKoreUtterances", Input, idKore, streamid, intentid, userIdKore, authTokenKore, KorePlatform, response.status_code, response.text)

def trainKore(streamid,userIdKore,authTokenKore,KorePlatform):
        url = KorePlatform+"/api/1.1/users/"+userIdKore+"/builder/sentences/ml/train"
        querystring = {"streamId":streamid,"rnd":"8ff5ai"}
        payload = "{}"
        headers = {'authorization': authTokenKore}
        try:
                response = requests.post(url, data=payload, headers=headers, params=querystring)
        except:
                raise Exception("Error while training Utterances")        

        return response

