import os, csv, random, argparse, datetime, requests
import xml.dom.minidom

header = ['ID','Last Name', 'First Name', 'Gender (M/F)', 'HKID', 'Date of Birth', 'Floor', 'Building', 'Street', 'Phone Number', 'Emergency Contact First Name', 'Emergency Contact Last Name', 'Emergency Contact Number', 'Emergency Contact Relationship' ]
building = []
street = []
gender = ['M','F']
floor = []
lastName = ['Choy','Guan','Hu','Yi','Kwok','Tse','Cheang','Chu','Peng','Hou','Song','Chai','Feng','Hei','Yick','Cho','Chao','Kan','Chong','Yu','Shum','Liu','Wang','Luk','Lei','Teng','Chin','Yan','Wong','Ho','Shen','Woo','Lou','Ngan','Man','Or','An','Sze','Lee','Au-Yeung','Yiu','Nip','To','Ying','Cui','Au','Lin','Chi','Fu','Yun','She','Tao','Chui','Kwong','Fong','Kung','Choi','Wa','Law','Mahtani','Gong','Suen','Ching','Shin','Chow','Lim','Lam','Che','Kam','Pak','Li','Lan','Mo','Ko','James','Kang','Pun','Lai','Ip','Mok','Kwan','Seto','Chiu','Tam','Lau','Cheng','Tsui','Ke','Koo','Yung','Wan','Sui','Chuk','Ngai','So','Wu','Chan','Auyeung','Su','Sim','Tu','Sun','Ning','Tso','Gu','Shiu','Jung','Szeto','Ji','Lung','Chun','Tan','Tung','Ng','Yin','Pan','Yuen','Yum','Pong','Kei','Yee','Tsoi','Huen','Chou','Tong','Dai','Jin','Yam','Hui','Lok','Hong','Hon','Lo','Cheuk','Ma','Heung','Hang','Siu','Ding','Fan','Chang','Yim','Yao','Shui','Fung','Wei','Liang','Chung','Meng','Ku','Shi','Ling','Yip','Wo','Keung','Rao','Chen','Mou','Tian','Chau','Kim','Hung','Cheung','Tai','Chuen','Daswani','Ge','Wen','Yeo','Shek','You','Sha','Bao','Lao','Ming','Yue','Lui','Deng','Cai','Yang','Liao','Gan','Ting','Poon','He','Tang','Sin','Lu','Tsang','Tseung']
firstName = ['Wing','Chi','Kit','Ying','Yan','Chun','Tsz','Man','Ming','Kin','Ching','Yuen','Fung','Mei','Kai','Cheuk','Wai','Pak','Yuk','Sin','Wei','Pui','Cy','Hoi','May','Chung','Sze','Choi','Hiu','Chu','Ling','Lin','Yin','Fei','Wan','Yee','Tong','Fong','Hong','Hui','Kei','Kam','Hon','Ka','Lei','Sing','Xiao','Kong','Ren','Min','Hei','Shu','Yang','Yun','Chen','Ning','Jie','Tao','Chong','Ye','Xin','Su','Xu','Kwun','Sheung','Yui','Yuet','Chui','Jin','Han','Ah','Qing','Nan','Bon','Mi','Peng','Hao','Jae','Xi','Lan','Hy','Bin','Long','Ty','Meng','Tai','Chin','Lou','Neo','Zhi','Li']
relationship = ['Father', 'Husband', 'Mother', 'Partner', 'Wife']

def downloadData(url, downloadFileName):
    
    #Delete Existing File
    os.remove(downloadFileName)

    #Download XML
    res = requests.get(url)
    with open(downloadFileName, 'wb') as ff:
        ff.write(res.content)

def parseBuildingStreetXML():
    doc = xml.dom.minidom.parse('./sourceData/building.xml')
    
    buildingName = doc.getElementsByTagName("EnglishBuildingName1")
    for bdn in buildingName:
        try:
            building.append(bdn.firstChild.nodeValue)
        except:
            pass

    streetName = doc.getElementsByTagName("EnglishAddress2")
    for sn in streetName:
        try:
            x = sn.firstChild.nodeValue
            if ((not "&" in x) and (not ":" in x) and (len(x) < 30)):
                street.append(x)
        except:
            pass

def getFloor():
    return "Flat " + random.choice("ABCDEFG") + " " +  str(random.randint(1, 40)) + "/F"

def getFirstName():
    x = random.randint(0,10)
    if (x == 0):
        return random.choice(firstName)
    else:
        return random.choice(firstName) + " " + random.choice(firstName)

def getPhoneNumber():
    return random.choice([random.randint(20000000,39999999), random.randint(50000000,69999999), random.randint(80000000,99999999)])

def getHKID():
    hkid = [0] * 8
    hkid[0] = ord(random.choice("ABCDEGHKMPRVYZ")) - 55
    for i in range(1,7):
        hkid[i] = random.randint(0, 9)
    
    s = chr(hkid[0] + 55)
    for i in range(1, 7):
        s += str(hkid[i])

    #check digit (incorrect)
    for i in range(0,7):
        hkid[7] += hkid[i] * (8-i)
    hkid[7] = hkid[7] % 11

    if hkid[7]==10:
        s += "A"
    else:
        s += str(hkid[7])
    return s

def getDoB():
    return datetime.datetime(random.randint(1930,2021), random.randint(1,12), random.randint(1,28)).strftime('%m/%d/%Y')
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help="Number of Record", required=True, type=int)
    parser.add_argument("-u", "--update", help="Update data", action='store_true')

    args = parser.parse_args()
    n = args.number
    update = args.update

    #delete existing file
    os.remove("./DummyData.csv")

    #open the file in append mode
    with open("./DummyData.csv", "a", newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        #update building from data.gov.hk
        if update:
            downloadData('https://www.rvd.gov.hk/datagovhk/bnb-u.xml', './sourceData/building.xml')
            print ("[+] Building data updated")
        
        parseBuildingStreetXML()
        
        #write to csv
        progress = 0.1
        id = 0
        for i in range(0,n):
            id += 1

            row = [id, getFirstName(), random.choice(lastName), random.choice(gender), getHKID(), getDoB(), getFloor(), random.choice(building), random.choice(street), getPhoneNumber(), getFirstName(), random.choice(lastName), getPhoneNumber(), random.choice(relationship)]
            writer.writerow(row)

            # print progress every 10%
            if (id == int(n * progress)):
                print(" [+] Progress: " + str(int(100 * progress)) + "%")
                progress += 0.1

if __name__ == "__main__":
    main()
