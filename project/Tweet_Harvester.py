import snscrape.modules.twitter as snt
import pandas as pd
import datetime
import pickle
search_limit = 1000
collector = "Miguel Luis Martinez" #CHANGE THIS TO YOUR NAME
def extract_tweet(tweet,keywords): #return tweet as a list matching the above format
    group = 'Group 57'
    category = 'MRCS'
    topic = 'The Marcos family won all cases filed against them'
    tweet_type = ''
    content = [
        tweet.url,
        group,collector,category,topic,keywords,
        f'@{tweet.user.username}',tweet.user.displayname,tweet.user.rawDescription,'',
        tweet.user.created,tweet.user.friendsCount,tweet.user.followersCount,tweet.user.location,
        tweet.rawContent,'','',tweet.date,'',
        '',tweet.likeCount,tweet.replyCount,tweet.retweetCount,tweet.quoteCount,tweet.viewCount,
        '','',''
    ]
    return content


def harvest_tweets(urls=[]): #harvest tweets from twitter using the keywords
    now = datetime.datetime.now().strftime("%y-%m-%d %H-%M-%S")
    search_terms = []
    for i in ["marcos","imelda","ferdinand"]: #essential keywords - Subject: Marcoses
        for j in ["all","lahat","wala","none","not",""]: #supporting keywords - Quantifier: All
            for k in ["case","kaso","trial","charges","filed",""]: #supporting keywords - Object: Cases
                for l in ["won","lost","nanalo","panalo","dismiss","ibinasura","junked","acquitted","not guilty"]: #supporting keywords - Verb: Won
                    search_terms.append(f"{i} {j} {k} {l}") #generate all 4-word combinations of the above
    tweets = []
    valid_search_terms = []
    #dataframe columns for spreadsheet
    columns = [
            'ID','Timestamp','Tweet URL',
            'Group','Collector','Category','Topic','Keywords',
            'Account handle','Account name','Account bio','Account type',
            'Joined','Following','Followers','Location',
            'Tweet','Tweet Translated','Tweet Type','Date posted','Screenshot',
            'Content Type','Likes','Replies','Retweets','Quote Tweets','Views',
            'Rating','Reasoning','Remarks'
            ]

    c = 1
    if len(urls) == 0:
        for search_term in search_terms:
            print(f"Using search term {search_term}")
            for i,tweet in enumerate(snt.TwitterSearchScraper(f'{search_term} since:2016-01-01 until:2022-12-31').get_items()):
                if i>search_limit:
                    print(f"Search limit for {search_term} reached!")
                    break
                if tweet.retweetedTweet is not None: #exclude retweets to avoid duplicates
                    continue
                tweets.append([f"57-{c}",now] + extract_tweet(tweet,search_term))
                print(f"Tweet {c} found!")
                c += 1
    else:
        for url in urls:
            twitid = url.split('/')[-1] #extract the tweet id for each tweet
            try:
                for i,tweet in enumerate(snt.TwitterTweetScraper(twitid).get_items()):
                    tweets.append([f"57-{c}",now] + extract_tweet(tweet,""))
                    print(f"Tweet {c} found!")
            except:
                    print(f"Error on tweet {c}")
                    tweets.append([f"57-{c}",now] + [\
                        url, 'Group 57', collector, 'MRCS', 'The Marcos family won all cases filed against them', '', \
                        '','','','', \
                        '','','','', \
                        '','','','','', \
                        '','','','','','', \
                        '','','' \
                    ]
                )
            c += 1
        df = pd.DataFrame(tweets, columns=columns).drop_duplicates(subset=['Tweet URL']) #remove duplicate tweets
        with open(f"results.bak.pkl","wb") as f:
            pickle.dump(df,f)
        df.to_csv(f"results - {now}.csv",index=False)
        print(f"Search terms used: {valid_search_terms}")

def load_tweets(urls = [],bakpath = "results.bak.pkl"):
    now = datetime.datetime.now().strftime("%d%m%Y  %H-%M-%S")
    #open the backup file
    with open(bakpath,"rb") as f:
        df = pickle.load(f)
    if len(urls) > 0:
        #preserve url order in getting results
        df2=df[0:0]
        for url in urls:
            df_temp = df[df["Tweet URL"]==url]
            print(df_temp)
            df2 = pd.concat([df2,df_temp])

        df2.to_csv(f"results-included - {now}.csv",index=False)
        df3 = df[~df["Tweet URL"].isin(urls)]
        df3.to_csv(f"results-excluded - {now}.csv",index=False)




#URLs of 170 tweets used in the project. Used for recovering tweets.
urls=[
"https://twitter.com/marcossoldier07/status/744091843663585280",
"https://twitter.com/EliseoRamos3/status/803737817180291072",
"https://twitter.com/ann_winter1224/status/802579707682140160",
"https://twitter.com/m_n0thing/status/1044173081323819008",
"https://twitter.com/Litemint12/status/1304407195568742402",
"https://twitter.com/davjr77856492/status/1304351706554265600",
"https://twitter.com/WinwinEklabu/status/1438406819827752962",
"https://twitter.com/9uva9j79o8lXwTW/status/1451015684880683009",
"https://twitter.com/patxchott/status/1448510697931898881",
"https://twitter.com/QuateAdi/status/1464646650136174594",
"https://twitter.com/airacelleayos/status/1472421350778146823",
"https://twitter.com/myfarm2022/status/1468750284159545351",
"https://twitter.com/MontesclarosRj/status/1486003233516630021",
"https://twitter.com/magaliamman/status/1500707182530416640",
"https://twitter.com/mochi_moch1104/status/1523907905526894593",
"https://twitter.com/IrisLuna216/status/1523813638368333824",
"https://twitter.com/univerSHAQ/status/728570307712196608",
"https://twitter.com/jaijeeeee/status/1450694009375002632",
"https://twitter.com/LelangmoVlogger/status/1469948429447041026",
"https://twitter.com/Victor05210/status/1481826357176901633",
"https://twitter.com/HarloharP/status/1478977805992210435",
"https://twitter.com/jacknpoy12/status/1508178537664192512",
"https://twitter.com/angelbhear/status/1526600873794842624",
"https://twitter.com/3riic15/status/1524921857341784066",
"https://twitter.com/najlegazpi/status/1572430060925382656",
"https://twitter.com/JGimoro/status/939056131351240704",
"https://twitter.com/Civic15303981/status/1465100169171529728",
"https://twitter.com/Civic15303981/status/1468858915576512516",
"https://twitter.com/IstgFrf80463309/status/1513039990745628672",
"https://twitter.com/gorgymac/status/1460844075834228736",
"https://twitter.com/Foilsick1/status/1542402888441270272",
"https://twitter.com/Jaybee19403528/status/1512727380816982021",
"https://twitter.com/RobertoMazoJr1/status/1460642185318383616",
"https://twitter.com/BrecasioS/status/709516903207669761",
"https://twitter.com/shaiyeee_xmh/status/1503734418686443520",
"https://twitter.com/JhazChewIt/status/1454639649008144393",
"https://twitter.com/glicelicious/status/738709671465385985",
"https://twitter.com/kumerjgarcia/status/1494093394024747008",
"https://twitter.com/vianangbantaye/status/1477679128954294275",
"https://twitter.com/KittyreiyuKy/status/1473802667344687111",
"https://twitter.com/alon_dy/status/903647792505245696",
"https://twitter.com/JGimoro/status/903285494246662144",
"https://twitter.com/alkevinnavarro/status/806905569286066176",
"https://twitter.com/amylauderdake/status/1296913578771939328",
"https://twitter.com/amylauderdake/status/1296909657802305542",
"https://twitter.com/chillyy_8/status/1492875453715333121",
"https://twitter.com/TommyFl99321967/status/932506183784632320",
"https://twitter.com/TommyFl99321967/status/932142148794966017",
"https://twitter.com/Du30USA/status/731104795193286656",
"https://twitter.com/PilapilRheza/status/1439182889074135045",
"https://twitter.com/Grayhams3/status/1474735060511244288",
"https://twitter.com/DevinJWinters/status/1404140640162648066",
"https://twitter.com/TitleistGolfer5/status/1582352973320966144",
"https://twitter.com/1H3LLuVahB/status/1502133001169162247",
"https://twitter.com/congressmanFAM/status/1479639256197136386",
"https://twitter.com/marita_tiongco/status/1471977099376611332",
"https://twitter.com/t_dhines/status/1458706507374100481",
"https://twitter.com/elignacio06/status/1446305528389406725",
"https://twitter.com/altiche_s/status/1446130138844786723",
"https://twitter.com/IndiannoGibbs/status/1439555362089103366",
"https://twitter.com/RudolphApostol/status/1562295632722685953",
"https://twitter.com/ioannesesledieu/status/1506543916425912321",
"https://twitter.com/mchappytoys/status/1501727421774831617",
"https://twitter.com/Dzhoods/status/1455115425461665794",
"https://twitter.com/theguru91010011/status/1427782528249720837",
"https://twitter.com/magaliamman/status/1498235782301028354",
"https://twitter.com/magaliamman/status/1496080416172052485",
"https://twitter.com/dilin818/status/1524254528454811648",
"https://twitter.com/thecuriousvina/status/1516758635417808900",
"https://twitter.com/amylauderdake/status/1296915962164215808",
"https://twitter.com/angeliloulou/status/1480260292437176326",
"https://twitter.com/ParkJanzTV1/status/1438359956630040580",
"https://twitter.com/FierceTita/status/1279407208048910337",
"https://twitter.com/egsyrey_24/status/1028557036387069954",
"https://twitter.com/ImeeMirando/status/1497770677415419907",
"https://twitter.com/Jeromeceb1/status/1494139477601624069",
"https://twitter.com/aljohari22/status/1493274576612065287",
"https://twitter.com/PilapilRheza/status/1452118071972220932",
"https://twitter.com/BenieVine/status/1001334767294414848",
"https://twitter.com/jbx907/status/768803667571081217",
"https://twitter.com/MiniJennni/status/1525018108385443840",
"https://twitter.com/CHEESEC47359950/status/1534344565624549376",
"https://twitter.com/BreinSierra/status/1447065312256352265",
"https://twitter.com/mariskybell1/status/1496404308447100928",
"https://twitter.com/AvrianeC/status/1522660119225712640",
"https://twitter.com/ocreole047/status/1531610144659808257",
"https://twitter.com/yurinomoka/status/1523703693652422657",
"https://twitter.com/YkyzZyky/status/1504487353523474445",
"https://twitter.com/genephillipians/status/1448738688750403584",
"https://twitter.com/BreinSierra/status/1447066384668659714",
"https://twitter.com/MNoyalcab/status/1446396942834028544",
"https://twitter.com/jylrdgls/status/1443753502728024100",
"https://twitter.com/LGamulo/status/1260044852764397568",
"https://twitter.com/fireprincess___/status/1173619056219324416",
"https://twitter.com/xingpopismybop/status/1072445401746296834",
"https://twitter.com/LazerKim/status/910397807990681601",
"https://twitter.com/OrchidNarvaez/status/801188328926126080",
"https://twitter.com/FierceTita/status/1440266984013250569",
"https://twitter.com/FierceTita/status/1440162100349792261",
"https://twitter.com/Simply_Ana77/status/1584900198979239937",
"https://twitter.com/MelynaVergara23/status/731918993892610048",
"https://twitter.com/VoiGlen/status/1598880022160609282",
"https://twitter.com/Abundare2022/status/1509850540876124166",
"https://twitter.com/Abundare2022/status/1505727392039710720",
"https://twitter.com/EaglesSouthern/status/1475777560428838914",
"https://twitter.com/DodongPags/status/1468776767498616834",
"https://twitter.com/FierceTita/status/1445305262865195008",
"https://twitter.com/MsDior04/status/1440508941155254272",
"https://twitter.com/diwang_mao/status/1318466166927421440",
"https://twitter.com/milkyway1969/status/1441462625611575306",
"https://twitter.com/IoSonoPatrick/status/1293747456396554240",
"https://twitter.com/magaliamman/status/1504044163460861954",
"https://twitter.com/cdion_stwain/status/1444643478923669510",
"https://twitter.com/henryIX_9th/status/1445344870135074818",
"https://twitter.com/Highvan14/status/795970939447963648",
"https://twitter.com/Wingsky6/status/1522786912565882880",
"https://twitter.com/analizacruz18/status/1489644358445854722",
"https://twitter.com/JhazChewIt/status/1464039028030803989",
"https://twitter.com/RommelPamotong1/status/1462539413477466114",
"https://twitter.com/GIGVL/status/1034248144920268800",
"https://twitter.com/_rvjs/status/719110699683676160",
"https://twitter.com/maria47215/status/1545164112334041089",
"https://twitter.com/Depric0n/status/1523755951219568642",
"https://twitter.com/Efferve83207851/status/1500803538615959555",
"https://twitter.com/RandomMusing5/status/1456392426759737348",
"https://twitter.com/AmarilloSlayer/status/1494007323093651456",
"https://twitter.com/JennielynSanti1/status/1477838141327560704",
"https://twitter.com/RobertoMazoJr1/status/1461003843568017409",
"https://twitter.com/Sl33py_J0hn/status/1575984055526756353",
"https://twitter.com/iamsparky79/status/1529959740905705473",
"https://twitter.com/zi_Thyrys/status/1524920955688001541",
"https://twitter.com/zi_Thyrys/status/1524221346745520129",
"https://twitter.com/c_tengee/status/1504592564300795905",
"https://twitter.com/AldrinYuga/status/1500244360843362304",
"https://twitter.com/Jnvlmcon/status/1497096850226266120",
"https://twitter.com/daniyyckah/status/1454323327217008646",
"https://twitter.com/louiehidalgo2/status/1033298529593131008",
"https://twitter.com/ayereesh/status/731720610800271360",
"https://twitter.com/hoonja_san/status/1446422974714695684",
"https://twitter.com/chicotibalas/status/1428944357919363073",
"https://twitter.com/hotmanila/status/1457323689062453253",
"https://twitter.com/Dwyreson_Moy/status/1447695914198462467",
"https://twitter.com/lightbringer620/status/1207194773515165696",
"https://twitter.com/ZheyPhiOrianez/status/1014391065334329344",
"https://twitter.com/che_mendioro/status/1054772712281845760",
"https://twitter.com/pinoypo17/status/1009629588262014976",
"https://twitter.com/omanest23/status/1474773528448671745",
"https://twitter.com/jo_rve/status/1515381809172738052",
"https://twitter.com/JadeBoltiad0r/status/932160132229693440",
"https://twitter.com/pinky1618/status/765208360257982464",
"https://twitter.com/kulafulafu/status/932593934013931520",
"https://twitter.com/palengkero1/status/1517027876914163717",
"https://twitter.com/benzkie0514/status/1506745948801744908",
"https://twitter.com/LiamKyle02/status/1460825368529489924",
"https://twitter.com/iamArgentum7/status/1457363476033064965",
"https://twitter.com/jollyAnnMJ/status/1473061320211992580",
"https://twitter.com/vargaz_milka/status/1445818695188504580",
"https://twitter.com/KulayPinoy/status/1445671921631199232",
"https://twitter.com/Kim38370027Kim/status/1448899532213743616",
"https://twitter.com/NormaTrinidad19/status/1185808326631792641",
"https://twitter.com/AsiyaAtasha/status/1556112782617374720",
"https://twitter.com/WillowCrimson_T/status/1485973071496417284",
"https://twitter.com/titoroddacz/status/1569841405119561728",
"https://twitter.com/iamsparky79/status/1531347261476589568",
"https://twitter.com/Realmenarzo50/status/1521104944891265024",
"https://twitter.com/rdmarcelo/status/1519177583958835202",
"https://twitter.com/FISLETA/status/1513508521144647683",
"https://twitter.com/FISLETA/status/1509066090059804681",
"https://twitter.com/zycjaerx/status/1499358493945458699",
"https://twitter.com/heyitseverleigh/status/1445363893639921666",
]

if (input("Enter yes to recover the tweets used in the project, otherwise get all tweets from search.").lower() in ['y','yes']):
    print("Using project tweets...")
else:
    urls = []

if (input("Enter yes to get new tweets, otherwise load tweets from a pickle file").lower() in ['y','yes']):
    harvest_tweets(urls)
else:
    load_tweets(urls)