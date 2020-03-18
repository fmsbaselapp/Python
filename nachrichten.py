from fake_useragent import UserAgent
from requests_html import HTMLSession
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import re

cred = credentials.Certificate('ServiceAccount.json')
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
    'https://display.edubs.ch/gm1',
)

for haupturl in schulhauslinks:  # TODO: Test entfernen

    a = "1"
    b = "2"
# ======

    # Hier wird die Schule ausgelesen.
    session = HTMLSession()
    r = session.get(haupturl, headers=uarandom)
    schulehtml = r.html.find('body > div > h1', first=True)
    schule = schulehtml.text
    print("""
    -----------"""+schule+"-----------""")
    # Fromatiere schule fuer Target
    schuleTarget2 = re.sub('r"|\s|"', '', schule)
    schuleTarget = re.sub('[äöü]', '', schuleTarget2)
    print(schuleTarget)

 # ======
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

 # ======
    # Gruppiert alle informationen in 3ergruppen = 1 ausfall ->
    # wenn zweiter ausfall true = zwei listen(zb. montag und dienstag) mit den jeweiligen ausfaellen
    alleAusfaelleUnsortiert = anzahlausfaelle1split
    if zweiterausfall:
        # splittet alle ausfaelle in 2 listen bei zweitem tag
        splitIndex = alleAusfaelleUnsortiert.index(zweiteausfalltag)
        ersterTagListe, zweiterTagListeDirty = alleAusfaelleUnsortiert[
            :splitIndex], alleAusfaelleUnsortiert[splitIndex+1:]

        # splittet zweiten tag bei anlaesse
        anlaesseSplit = zweiterTagListeDirty.index('Anlässe')
        zweiterTagListe = zweiterTagListeDirty[:anlaesseSplit]

        # in 3er gruppen sortieren
        N = 3
        alleAusfaelleListe1Tag = [ersterTagListe[n:n+N]
                                 for n in range(0, len(ersterTagListe), N)]

        alleAusfaelleListe2Tag = [zweiterTagListe[n:n+N]
                                 for n in range(0, len(zweiterTagListe), N)]
    else:
        N = 3
        alleAusfaelleListe1Tag = [alleAusfaelleUnsortiert[n:n+N]
                                 for n in range(0, len(alleAusfaelleUnsortiert), N)]
# ======
    # Zaehlt ausfaelle des 1. Tags
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
# ======
    # Zaehlt ausfaelle des 2. Tags
    if zweiterausfall:
        anzahlzweitertag = 0
        anzahlT2 = len(zweiterTagListe) / 3
    else:
        anzahlT2 = 0
# ======
    # =========================================
    # ERSTER TAG
    # =========================================
    x = 0

    # Liest klasse aus HTML
    while x < anzahl1:
        try:
            # ----- INFOS -----# (benoetigt wird: Ausfall(alle Infos), Betroffene klassen, Tag des Ausfalls)

            # SCHULHAUS das bearbeitet wird
            # print(schule)

            # AUSFALL der bearbeitet wird (alle infos)
            print('\n')
            print(alleAusfaelleListe1Tag[x])
            auktellerAufall = alleAusfaelleListe1Tag[x]

            # TAG des Ausfalls
            # print(ersterausfalltag1)
            # print(zweiteausfalltag1)

            # klasse in html suchen
            klasse = r.html.find('body > div > div > div > strong')[x]
            klassetext = klasse.text

            # splittet den klassentext in einen array ( splittet bei komma und lehrzeichen )
            klassetextsplit = re.split(',| ', klassetext)

            klassentextlen = len(klassetextsplit)

            anz = 0  # setzt while loop unten zurueck
 # ======    # Liest verschindene Klassen aus und unterteilt sie in eine Liste
            while anz < klassentextlen:
                try:
                    klass = klassetextsplit[anz]
                    klasseSauber = klass.replace(':', '')
                    print("===> Klasse: " + klasseSauber)

                    klasslen = len(klasseSauber)
                    klassenstufe = klass[0]

                    if klassenstufe.isdigit():

                        print("===> Stufe: " + klassenstufe)

                        zeichen = 1  # setzt while loop unten zurueck
# ======                 # Liest zusammengesetzte Klassen aus. (Bsp. 1ac, 2BD, 3abc)
                        while zeichen <= klasslen:

                            try:
                                # TODO: check if 2. oder 3. stelle ein Buchstabe und nicht eine Zahl ist
                                # 2. oder 3. stelle nicht weiter!s
                                if klasseSauber[zeichen].isalpha():
                                    klassExtracted = klassenstufe + \
                                        klasseSauber[zeichen]
                                    # TODO: final goal is here bring here the ausfaelle!
                                    print(klassExtracted)
                                    zeichen = zeichen + 1
                                    klassFinal = klassExtracted.upper()
                                    print('\n'+schule+'\n'+ersterausfalltag1+'\n'+klassFinal +
                                          '\n'+auktellerAufall[0]+'\n'+auktellerAufall[1]+'\n'+auktellerAufall[2]+'\n')

                                    if klassetext == "Keine Anlässe":
                                        break
                                    if klassetext == "Keine Stellvertretungen":
                                        break
                                    else:
                                        if klassetext == "Keine Neuigkeiten":
                                            break
                                        else:
                                            num1 = x - 1 + zeichen
                                            num = str(num1)
                                            individualDoc = auktellerAufall[0] + \
                                                ' - '+num
                                            print(ersterausfalltag+'=============================='+ individualDoc)
                                            
                                            # fuegt 'am' hinzu bei allen wochentagen
                                            if ersterausfalltag == 'Heute:':
                                                tag1 = 'Ausfall '+ersterausfalltag
                                            else:
                                                tag1 = 'Ausfall am '+ersterausfalltag
                                            try:
                                                db.collection(u'Nachrichten').document(u'Schulen').collection(
                                                    schuleTarget2).document(individualDoc).set({

                                                        u'tag': tag1,
                                                        u'target': schuleTarget+'-'+klassFinal,
                                                        u'klasse': auktellerAufall[0],
                                                        u'grund': auktellerAufall[1],
                                                        u'raum': auktellerAufall[2],


                                                    })
                                            except:
                                                e = sys.exc_info()[0]

                                                print("<p>Error: %s</p>" % e)
                                else:
                                    break

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
# ======
    # =========================================
    # ZWEITER TAG
    # =========================================
    y = 0

    # Liest klasse aus HTML

    while y < anzahlT2:
        try:
            # ----- INFOS -----# (benoetigt wird: Ausfall(alle Infos), Betroffene klassen, Tag des Ausfalls)

            # SCHULHAUS das bearbeitet wird
            # print(schule)

            # AUSFALL der bearbeitet wird (alle infos)
            print('\n')
            print(alleAusfaelleListe2Tag[y])
            auktellerAufall = alleAusfaelleListe2Tag[y]

            # TAG des Ausfalls
            # print(ersterausfalltag1)
            # print(zweiteausfalltag1)

            # klasse in html suchen
            klasse = r.html.find('body > div > div > div > strong')[x+y]
            klassetext = klasse.text

            # splittet den klassentext in einen array ( splittet bei komma und lehrzeichen )
            klassetextsplit = re.split(',| ', klassetext)

            klassentextlen = len(klassetextsplit)

            anz = 0  # setzt while loop unten zurueck
# ======     # Liest verschindene Klassen aus und unterteilt sie in eine Liste
            while anz < klassentextlen:
                try:
                    klass = klassetextsplit[anz]
                    klasseSauber = klass.replace(':', '')
                    print("===> Klasse: " + klasseSauber)

                    klasslen = len(klasseSauber)
                    klassenstufe = klass[0]

                    if klassenstufe.isdigit():

                        print("===> Stufe: " + klassenstufe)

                        zeichen = 1  # setzt while loop unten zurueck
# ======                 # Liest zusammengesetzte Klassen aus. (Bsp. 1ac, 2BD, 3abc)
                        while zeichen <= klasslen:

                            try:

                                if klasseSauber[zeichen].isalpha():
                                    klassExtracted = klassenstufe + \
                                        klasseSauber[zeichen]

                                    print(klassExtracted)
                                    zeichen = zeichen + 1
                                    klassFinal = klassExtracted.upper()
                                    print('\n'+schule+'\n'+zweiteausfalltag+'\n'+klassFinal +
                                          '\n'+auktellerAufall[0]+'\n'+auktellerAufall[1]+'\n'+auktellerAufall[2]+'\n')

                                    if klassetext == "Keine Anlässe":
                                        break
                                    if klassetext == "Keine Stellvertretungen":
                                        break
                                    else:
                                        if klassetext == "Keine Neuigkeiten":
                                            break
                                        else:
                                            num1 = x + y - 1 + zeichen
                                            num = str(num1)
                                            individualDoc = auktellerAufall[0] + \
                                                ' - '+num
                                            # TODO:
                                            print(
                                                zweiteausfalltag+'==============================' + individualDoc)
                                            # fuegt 'am' hinzu bei allen wochentagen
                                            if zweiteausfalltag == 'Morgen:':
                                                tag2 = 'Ausfall '+zweiteausfalltag
                                            else:
                                                tag2 = 'Ausfall am '+zweiteausfalltag
                                            try:
                                                db.collection(u'Nachrichten').document(u'Schulen').collection(
                                                    schuleTarget2).document(individualDoc).set({
                                                        u'tag': tag2,
                                                        u'target': schuleTarget+'-'+klassFinal,
                                                        u'klasse': auktellerAufall[0],
                                                        u'grund': auktellerAufall[1],
                                                        u'raum': auktellerAufall[2],


                                                    })
                                                
                                            except:
                                                e = sys.exc_info()[0]

                                                print("<p>Error: %s</p>" % e)
                                else:
                                    break
                            except:
                                break
                        anz = anz + 1
                    else:
                        print("Keine Stufe erkannt!")
                        anz = anz + 1

                except:

                    break
            y = y + 1
        except:
            break
