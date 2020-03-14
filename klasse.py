from fake_useragent import UserAgent
from requests_html import HTMLSession
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import re

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
schulhauslinksTest = (
    'https://display.edubs.ch/gl1',
    "https://display.edubs.ch/hb1")

for haupturl in schulhauslinksTest:  # TODO: Test entfernen

    a = "1"
    b = "2"

    # Hier wird die Schule ausgelesen.
    session = HTMLSession()
    r = session.get(haupturl, headers=uarandom)
    schulehtml = r.html.find('body > div > h1', first=True)
    schule = schulehtml.text
    print("""
    -----------"""+schule+"-----------""")

    anzahlausfaelle1 = r.html.text
    anzahlausfaelle1split = anzahlausfaelle1.split('\n')
    del (anzahlausfaelle1split)[0:4]

    try:
        ersterausfalltaghtml = r.html.find('body > div > h3', first=True)
        ersterausfalltag = ersterausfalltaghtml.text
        ersterausfalltag1 = a + ersterausfalltag
        keinausfalltag = False

    except:  # keine Stellvertretungen
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

    except:  # kein zweiter Tag
        zweiterausfall = False
        zweiteausfalltaghtml = r.html.find('body > div > h2')[1]
        zweiteausfalltag = zweiteausfalltaghtml.text
        zweiteausfalltag1 = b + zweiteausfalltag

    # gruppiert alle informationen in 3ergruppen = 1 ausfall
    alleAusfälleUnsortiert = anzahlausfaelle1split
    N = 3
    alleAusfälleListe = [alleAusfälleUnsortiert[n:n+N]
                         for n in range(0, len(alleAusfälleUnsortiert), N)]

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

    # Liest klasse aus HTML
    while x < anzahl1:
        try:
            # ----- INFOS -----# (benötigt wird: Ausfall(alle Infos), Betroffene klassen, Tag des Ausfalls)

            # SCHULHAUS das bearbeitet wird
            # print(schule)

            # AUSFALL der bearbeitet wird (alle infos)
            print('\n')
            print(alleAusfälleListe[x])
            auktellerAufall = alleAusfälleListe[x]

            # TAG des Ausfalls
            # print(ersterausfalltag1)
            # print(zweiteausfalltag1)

            # klasse in html suchen
            klasse = r.html.find('body > div > div > div > strong')[x]
            klassetext = klasse.text

            # splittet den klassentext in einen array ( splittet bei komma und lehrzeichen )
            klassetextsplit = re.split(',| ', klassetext)

            klassentextlen = len(klassetextsplit)

            anz = 0  # setzt while loop unten zurück
            # Liest verschindene Klassen aus und unterteilt sie in eine Liste
            while anz < klassentextlen:
                try:
                    klass = klassetextsplit[anz]
                    klasseSauber = klass.replace(':', '')
                    print("===> Klasse: " + klasseSauber)

                    klasslen = len(klasseSauber)
                    klassenstufe = klass[0]

                    if klassenstufe.isdigit():

                        print("===> Stufe: " + klassenstufe)

                        zeichen = 1  # setzt while loop unten zurück
                        # Liest zusammengesetzte Klassen aus. (Bsp. 1ac, 2BD, 3abc)
                        while zeichen <= klasslen:
                            
                            try:
                                # TODO: check if 2. oder 3. stelle ein Buchstabe und nicht eine Zahl ist
                                # 2. oder 3. stelle nicht weiter!s
                                if klasseSauber[zeichen].isalpha():
                                    klassExtracted = klassenstufe + \
                                        klasseSauber[zeichen]
                                    # TODO: final goal is here bring here the ausfälle!
                                    print(klassExtracted)
                                    zeichen = zeichen + 1
                                    klassFinal = klassExtracted.upper()
                                    print('\n'+schule+'\n'+ersterausfalltag1+'\n'+klassFinal +
                                          '\n'+auktellerAufall[0]+'\n'+auktellerAufall[1]+'\n'+auktellerAufall[2]+'\n')

                                    if klassetext == "Keine Anlässe":
                                        break
                                    else:
                                        if klassetext == "Keine Neuigkeiten":
                                            break
                                        else:
                                            db.collection(u'Ausfaelle').document(u'Schulen').collection(
                                                schule).document(ersterausfalltag1).update({'klasse': })
                                                
                            except:
                                break
                        anz = anz + 1
                    else:
                        print("Keine Stufe erkannt!")
                        anz = anz + 1

                except:

                    break
            x = x + 1
        except:
            break
