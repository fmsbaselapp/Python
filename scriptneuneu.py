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

for haupturl in schulhauslinks:

    a = "1"
    b = "2"

    # Hier wird die Schule ausgelesen.
    session = HTMLSession()
    r = session.get(haupturl, headers=uarandom)
    schulehtml = r.html.find('body > div > h1', first=True)
    schule = schulehtml.text

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
        ersterausfalltaghtml = r.html.find('body > div > div > div > strong')[0]
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

    keinausfallhtml = r.html.find('body > div > h2')[1]
    keinausfall = keinausfallhtml.text

    anzahlzweitertag = 0
    if zweiterausfall == True:
        anzahlausfaelle2 = r.html.text
        anzahlausfaelle2split = anzahlausfaelle2.split('\n')
        del (anzahlausfaelle2split)[0:anzahlerstertagganz]

        for position2 in anzahlausfaelle2split:
            if position2 == keinausfall:
                break
            else:
                anzahlzweitertag = anzahlzweitertag + 1

    anzahl2 = anzahlzweitertag / 3
    anzahlausfaellekomplett = int(anzahl1 + anzahl2)
    anzahlausfaellekomplett0 = anzahl1 + anzahl2

    x = 0
    t = ''
    filename = bytes(schule, 'utf-8')
    filenamehex = filename.hex()
    filenamex = './text/'+filenamehex+'.txt'
    filenamealt = bytes((schule+" Alt"), 'utf-8')
    filenamealthex = filenamealt.hex()
    filenamealtx = './text/'+filenamealthex+'.txt'

    while x < anzahl1:
        feld = x

        try:
            # 2. Hier wird der Ausfall und die Klasse ausgelesen.
            ausfall = r.html.find('body > div > div')[x]
            ausfalltext = ausfall.text
            ausfallcode = ausfalltext.encode('utf-8')
            ausfallhex = ausfallcode.hex()

            file = open(filenamex, "w")
            file.write(t)
            file.close()

        except:
            break

        x = x + 1
        t = t + ausfallhex

    file = open(filenamex, "r")
    vergleich = file.read()
   
    filealt = open(filenamealtx, "r")
    vergleichalt = filealt.read()
   

    if vergleich == vergleichalt:
        aktuell = "False"
    else:
        aktuell = "True"
        a = "1"
        b = "2"

        # Hier wird die Schule ausgelesen.
        session = HTMLSession()
        r = session.get(haupturl)
        schulehtml = r.html.find('body > div > h1', first=True)
        schule = schulehtml.text

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
            ersterausfalltaghtml = r.html.find('body > div > div > div > strong')[0]
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

        keinausfallhtml = r.html.find('body > div > h2')[1]
        keinausfall = keinausfallhtml.text

        anzahlzweitertag = 0
        if zweiterausfall == True:
            anzahlausfaelle2 = r.html.text
            anzahlausfaelle2split = anzahlausfaelle2.split('\n')
            del (anzahlausfaelle2split)[0:anzahlerstertagganz]

            for position2 in anzahlausfaelle2split:
                if position2 == keinausfall:
                    break
                else:
                    anzahlzweitertag = anzahlzweitertag + 1

        anzahl2 = anzahlzweitertag / 3
        anzahlausfaellekomplett = int(anzahl1 + anzahl2)
        anzahlausfaellekomplett0 = anzahl1 + anzahl2

        anlaessetexthtml = r.html.find('body > div > h2')[1]
        anlaessetext = anlaessetexthtml.text

        if anzahlausfaellekomplett == 0:
            anzahlausfaellekomplett1 = anzahlausfaellekomplett + 1
        else:
            anzahlausfaellekomplett1 = anzahlausfaellekomplett

        anlaessehtml = r.html.find('body > div > div')[anzahlausfaellekomplett1]
        anlaesse = anlaessehtml.text

        anzahlmitanlaesse = 5 + anzahlerstertag + anzahlzweitertag

        anlaessefertightml = r.html.find('body > div > h2')[2]
        anlaessefertig = anlaessefertightml.text

        anzahlanlaessecounter = 0
        if anlaesse == "Keine Anlässe":
            keinanlass = True
        else:
            keinanlass = False
            anzahlanlaesse = r.html.text
            anzahlanlaessesplit = anzahlanlaesse.split('\n')
            del (anzahlanlaessesplit)[0:anzahlmitanlaesse]

            for position3 in anzahlanlaessesplit:
                if position3 == anlaessefertig:
                    break
                else:
                    anzahlanlaessecounter = anzahlanlaessecounter + 1

        anzahl3 = anzahlanlaessecounter / 3
        anzahlausfaellekomplett2 = anzahlausfaellekomplett1 + int(anzahl3)

        anlassnamehtml = r.html.find('body > div > h2')[1]
        anlassnametext = anlassnamehtml.text
        anlassname = "-" + anlassnametext

        # Hier werden die Daten aus der Datenbank geloescht.
        tag = (
            "Montag:", "Dienstag:", "Mittwoch:", "Donnerstag:", "Freitag:", "Heute:", "Keine Stellvertretungen",
            "Anlässe")
        for loeschkombo in tag:
            loeschtag = a + loeschkombo
            db.collection(u'Ausfaelle').document(u'Schulen').collection(schule).document(loeschtag).delete()
        for loeschkombo in tag:
            loeschtag = b + loeschkombo
            db.collection(u'Ausfaelle').document(u'Schulen').collection(schule).document(loeschtag).delete()
        db.collection(u'Anlaesse').document(u'Schulen').collection(schule).document(anlassname).delete()

        # Hier werden die Dokumente erstellt.
        leerarray = ('' + '\n' + '' + '\n' + '' + '\n')
        leerarraysplit = leerarray.split('\n')

        leer = {u'0': leerarraysplit}

        leerarray1 = ('' + '\n' + '' + '\n')
        leerarraysplit1 = leerarray1.split('\n')

        leer1 = {u'0': leerarraysplit1}

        if keinausfalltag == False:
            db.collection(u'Ausfaelle').document(u'Schulen').collection(schule).document(ersterausfalltag1).set(leer)
        if zweiterausfall == True:
            db.collection(u'Ausfaelle').document(u'Schulen').collection(schule).document(zweiteausfalltag1).set(leer)
        if keinanlass == False:
            db.collection(u'Anlaesse').document(u'Schulen').collection(schule).document(anlassname).set(leer)

        # 1. Hier werden die Ausfaelle in die Datenbank geladen.
        x = 0
        while x < anzahl1:
            feld = x

            try:
                # 2. Hier wird der Ausfall und die Klasse ausgelesen.
                ausfall = r.html.find('body > div > div')[x]
                ausfalltext = ausfall.text

                klasse = r.html.find('body > div > div > div > strong')[x]
                klassetext = klasse.text

                # 3. Hier wird die Klasse ersetzt und neu eingefuegt.
                ausfalltextneu = ausfalltext.replace(klassetext + " ", "")
                komplettausfall = klassetext + "\n" + ausfalltextneu
                komplettausfallsplit = komplettausfall.split('\n')

                # 4. Hier wird geprÃŒft.
                feld = str(x)
                if keinausfall == True:
                    db.collection(u'Ausfaelle').document(u'Schulen').collection(schule).document(ersterausfalltag1).set(
                        leer)
                    break
                else:
                    if klassetext == "Keine Anlässe":
                        break
                    else:
                        if klassetext == "Keine Neuigkeiten":
                            break

                        # 5. Ausfall
                        else:
                            ausfaelle = {
                                feld: komplettausfallsplit
                            }
                            db.collection(u'Ausfaelle').document(u'Schulen').collection(schule).document(
                                ersterausfalltag1).update(ausfaelle)

                    # 6. Zaehlung der Ausfaelle.
                    x = x + 1
            except:
                break

        y = int(anzahl1)
        w = 0
        while y < anzahlausfaellekomplett0:
            feld2 = w
            try:
                # 2. Hier wird der Ausfall und die Klasse ausgelesen.
                ausfall0 = r.html.find('body > div > div')[y]
                ausfalltext0 = ausfall0.text

                klasse0 = r.html.find('body > div > div > div > strong')[y]
                klassetext0 = klasse0.text

                # 3. Hier wird die Klasse ersetzt und neu eingefuegt.
                ausfalltextneu0 = ausfalltext0.replace(klassetext0 + " ", "")
                komplettausfall0 = klassetext0 + "\n" + ausfalltextneu0
                komplettausfallsplit0 = komplettausfall0.split('\n')

                feld2 = str(w)

                if keinausfall == True:
                    db.collection(u'Ausfaelle').document(u'Schulen').collection(schule).document(zweiteausfalltag1).set(
                        leer)
                    break
                else:
                    if klassetext0 == "Keine Anlässe":
                        break
                    else:
                        if klassetext0 == "Keine Neuigkeiten":
                            break

                        # 5. Ausfall
                        else:
                            ausfaelle2 = {
                                feld2: komplettausfallsplit0
                            }
                            db.collection(u'Ausfaelle').document(u'Schulen').collection(schule).document(
                                zweiteausfalltag1).update(ausfaelle2)

                    # 6. Zaehlung der Ausfaelle.
                    y = y + 1
                    w = w + 1
            except:
                break

        z = anzahlausfaellekomplett1
        q = 0
        while z <= anzahlausfaellekomplett2:
            feld3 = q
            try:
                anlass = r.html.find('body > div > div')[z]
                anlasstext = anlass.text
                anlasstextsplit = anlasstext.split('\n')
                del (anlasstextsplit)[1]

                feld3 = str(q)
                if anlasstext == "Keine Anlässe":
                    break
                else:
                    if anlasstext == "Keine Neuigkeiten":
                        break
                    else:
                        anlaesse1 = {
                            feld3: anlasstextsplit
                        }
                        db.collection(u'Anlaesse').document(u'Schulen').collection(schule).document(
                            anlassname).update(anlaesse1)

                z = z + 1
                q = q + 1
            except:
                break

    file.close()
    #filealt.close()

    filealt = open(filenamealtx, "w")
    file = open(filenamex, "r")

    neuesfile = file.read()
    filealt.write(neuesfile)

    filealt.close()
    file.close()
