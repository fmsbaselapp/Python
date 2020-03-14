from fake_useragent import UserAgent
from requests_html import HTMLSession
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('ServiceAccountTest.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

ua = UserAgent()
uarandom = {'User-Agent': ua.random}
schulhauslinks = ('https://display.edubs.ch/bfsa', 'https://display.edubs.ch/bfsb', 'https://display.edubs.ch/bfsc',
                  'https://display.edubs.ch/bfsd', 'https://display.edubs.ch/dr1', 'https://display.edubs.ch/fzg1',
                  'https://display.edubs.ch/fms1', 'https://display.edubs.ch/gm1', 'https://display.edubs.ch/gb1',
                  'https://display.edubs.ch/gkg1', 'https://display.edubs.ch/gl1', 'https://display.edubs.ch/ii1',
                  'https://display.edubs.ch/kh1', 'https://display.edubs.ch/bibliothek',
                  'https://display.edubs.ch/medialab1', 'https://display.edubs.ch/sb1', 'https://display.edubs.ch/dw1',
                  'https://display.edubs.ch/dli1', 'https://display.edubs.ch/hb1', 'https://display.edubs.ch/sleo',
                  'https://display.edubs.ch/sand1', 'https://display.edubs.ch/alb1', 'https://display.edubs.ch/tb',
                  'https://display.edubs.ch/vog1', 'https://display.edubs.ch/wr1', 'https://display.edubs.ch/joh1',
                  'https://display.edubs.ch/dli2', 'https://display.edubs.ch/ts1', 'https://display.edubs.ch/wg1',
                  'https://display.edubs.ch/zbag1', 'https://display.edubs.ch/zbal1')
schulhauslinksTest = ('https://display.edubs.ch/fms1', 'https://display.edubs.ch/bfsa')

for haupturl in schulhauslinksTest: #TODO: Test entfernen

    a = "1"
    b = "2"

    # Hier wird die Schule ausgelesen.
    session = HTMLSession()
    r = session.get(haupturl, headers=uarandom)
    schulehtml = r.html.find('body > div > h1', first=True)
    schule = schulehtml.text
    print(schule)

    anzahlausfaelle1 = r.html.text
    anzahlausfaelle1split = anzahlausfaelle1.split('\n')
    del (anzahlausfaelle1split)[0:4]

    try:
        ersterausfalltaghtml = r.html.find('body > div > h3', first=True)
        ersterausfalltag = ersterausfalltaghtml.text
        ersterausfalltag1 = a + ersterausfalltag
        keinausfalltag = False
    except:
        keinausfalltag = True
        ersterausfalltaghtml = r.html.find(
            'body > div > div > div > strong')[0]
        ersterausfalltag = ersterausfalltaghtml.text
        ersterausfalltag1 = a + ersterausfalltag

    try:
        zweiteausfalltaghtml = r.html.find('body > div > h3')[1]
        zweiteausfalltag = zweiteausfalltaghtml.text
        zweiteausfalltag1 = b + zweiteausfalltag
        zweiterausfall = True
    except:
        zweiterausfall = False
        zweiteausfalltaghtml = r.html.find('body > div > h2')[1]
        zweiteausfalltag = zweiteausfalltaghtml.text
        zweiteausfalltag1 = b + zweiteausfalltag

    anzahlerstertag = 0
    for position in anzahlausfaelle1split:
        if position == zweiteausfalltag:
            break
        else:
            anzahlerstertag = anzahlerstertag + 1

    anzahlerstertagganz = anzahlerstertag + 5

    anzahlx = anzahlerstertag / 3

    if anzahlx < 1:
        anzahl1 = 0
    else:
        anzahl1 = anzahlx

    x = 0
    zeichen = 1
    anz = 0
    e = 0 #evtl delete
    while x < anzahl1:
        try:
            klasse = r.html.find('body > div > div > div > strong')[x]
            klassetext = klasse.text
            klassetextsplit = klassetext.split(',')
            
            klassentextlen = len(klassetextsplit)

            
            while anz < klassentextlen:
                
                
                klass = klassetextsplit[anz]
                klasseSauber = klasse.replace(':', '')
                print("======> Klasse: " + klasseSauber)

                klasslen = len(klasse)
                klassenstufe = klasse[0]

                klassenzahl = klassenstufe.isdigit()
                
                
        

                if klassenzahl == True:
                    print("======> Klassenstufe erkannt: " + klassenstufe)
                    
                    while zeichen <= klasslen:
                        klassExtracted = klassenstufe + klasse[zeichen]
                        print(klassExtracted)
                        anz = anz + 1
                        p = p + 1
                        e = e + 1
                else:
                    anz = anz + 1
                    p = p + 1
                    e = e + 1
                    print("Keine Stufe erkannt!")
        
        except:
            break
        

        x = x + 1

        

  