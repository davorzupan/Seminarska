from razred import oznaka
import knjiznica
import os

N = 50

def uvod():
    knjiznica.izpis(N)
    knjiznica.uvod()
    knjiznica.datum()
    knjiznica.izpis(N)

def lokacijeProgramov():
    global Txt2Bow
    global BowKMeans
    global BowTrainBinSVM
    global BowClassify
    global ucnaZbirkaBesedil
    global zbirkaBesedilPreverjanja
    Txt2Bow = knjiznica.lokacijaDatoteke("Lokacija programa Txt2Bow: ")
    BowKMeans = knjiznica.lokacijaDatoteke("Lokacija programa BowKMeans: ")
    BowTrainBinSVM = knjiznica.lokacijaDatoteke("Lokacija programa BowTrainBinSVM: ")
    BowClassify = knjiznica.lokacijaDatoteke("Lokacija programa BowClassify: ")
    ucnaZbirkaBesedil = knjiznica.lokacijaDatoteke("Lokacija besedilne datoteke za ucenje: ")
    zbirkaBesedilPreverjanja = knjiznica.lokacijaDatoteke("Lokacija besedilne datoteke za prevejanje: ")


def izgradnjaDatotecneStrukture():
    global korenskaMapa
    global statistikaMapa
    global razbitiClanki
    korenskaMapa = knjiznica.najdiLokacijoMape(ucnaZbirkaBesedil)
    korenskaMapa = knjiznica.ustvariNovoMapo(korenskaMapa)
    korenskaMapa+="/"
    statistikaMapa = korenskaMapa + "Statistika/"
    razbitiClanki = korenskaMapa + "Razbiti_Clanki/"
    os.mkdir(statistikaMapa)
    os.mkdir(razbitiClanki)

def prviDel():
    try:
        ukaz = Txt2Bow + " -inlndoc:"+ucnaZbirkaBesedil+ " -o:"+statistikaMapa+"prvo.bow -stopword:none -stemmer:none -ngramlen:1"
        os.system(ukaz)
        print("\n\n Pretvorba v BOW uspesna.")
    except:
        print("\nUkaz se ni uspesno izvedel!")


def obdelavaPrvegaBesedila():
    trenutniSeznamOznak = []
    oznake = []
    print("Obdelava dokumenta v postopku....\nLahko traja nekaj sekund...")
    ucnoBesedilo = open(ucnaZbirkaBesedil,"r")
    for vrsta in iter(ucnoBesedilo):
        #   Bedarija da posebej shranjujem oba dela... zna pridit kasneje prav
        info, clanek = knjiznica.izlusciPosameznaDela(vrsta)
        trenutniSeznamOznak, stevilkaClanka = knjiznica.infoObdelava(info)
        #   Prehod skozi oznake, še vedno ista vrstica
        for oz in trenutniSeznamOznak:
            tmp = oznaka(oz,stevilkaClanka)
            #   Zacnem polniti ali pa preverjam ali je ze notri nek element in inkrementiram njegovo vrednost
            oznake = knjiznica.dodajOznakoVBazo(oznake,tmp)
    ucnoBesedilo.close()
    oznake = knjiznica.sortiranje(oznake)
    knjiznica.shraniStatistiko(oznake, statistikaMapa,"Statistika_Oznak_1")
    knjiznica.izpis(N)

def drugiDel():
    vpr = 1
    print()
    while (vpr == 1):
        clust = input("Na koliko clustrov zelis razdeliti dokument: ")
        #   Ustvari datoteko za vsako število...
        try:
            tmpLokacija = statistikaMapa+clust+"_clustrov/"
            os.mkdir(tmpLokacija)
            os.chdir(tmpLokacija)
            ukaz = BowKMeans + " -i:"+statistikaMapa+"prvo.bow -clusts:"+clust
            os.system(ukaz)
        except:
            print("Na toliko clustrov se je ze razdelilo...")
        odg = int(input("Zelis ponoviti razdelitev? \n0 == Ne\n1 == Da\nIzbira:"))
        if (odg != 1):
            break
    knjiznica.izpis(N)
    print("Clustriranje koncano...")


def uporabaKlasifikatorjev():
    vpr = 1
    while(vpr == 1):
        print("BowClassify...")
        kategorija = input("Kategorija: ")
        jedro = input("Jedro [L... linerna   P... polinomska]: ")
        kategorija = kategorija.upper()
        jedro = jedro.upper()
        lokacijaUcenja = statistikaMapa +kategorija+"_"+jedro+"/prvo.bowmd"
        print(lokacijaUcenja)
        if(os.path.isfile(lokacijaUcenja)):
            print("obstaja...")
        else:
            print("Ta klasifikacija ni bila izvedena!")

    odg =input("Zelis ponoviti uporabo BowClassify? \n0 == Ne\n1 == Da\nIzbira:")
        if (odg != "1"):
        break



def obdelavaDrugegaBesedila():
    trenutniSeznamOznak = []
    oznake = []
    print("Obdelava dokumenta v postopku....\nLahko traja nekaj sekund...")
    ucnoBesedilo = open(zbirkaBesedilPreverjanja,"r")
    for vrsta in iter(ucnoBesedilo):
        info, clanek = knjiznica.izlusciPosameznaDela(vrsta)
        trenutniSeznamOznak, stevilkaClanka = knjiznica.infoObdelava(info)
        #   Prehod skozi oznake, še vedno ista vrstica
        for oz in trenutniSeznamOznak:
            tmp = oznaka(oz,stevilkaClanka)
            #   Zacnem polniti ali pa preverjam ali je ze notri nek element in inkrementiram njegovo vrednost
            oznake = knjiznica.dodajOznakoVBazo(oznake,tmp)
        knjiznica.shraniPosamezenClanek(stevilkaClanka,clanek,razbitiClanki)
    ucnoBesedilo.close()
    oznake = knjiznica.sortiranje(oznake)
    knjiznica.shraniStatistiko(oznake, statistikaMapa,"Statistika_Oznak_2")

    global seznamKategorijDrugegaBesedila
    seznamKategorijDrugegaBesedila = oznake
    knjiznica.izpis(N)
    '''
    seznamKategorijDrugegaBesedila je seznam vseh objektov, ki so sestavljeni iz imena,
    pogostosti pojavitve in seznamu dokumentov v katerem se nahajajo.
    To uporabiš kasneje pri preverjanju ali nek dokument res je označen pod neko kategorijo ali ne...

    '''
    uporabaKlasifikatorjev()
    


def tretjiDel():
    vpr = 1
    while(vpr == 1):
        odg = input("Prikazi podatke o pogostosti klasifikatorjev prvega dokumenta? [Y/N]")
        odg = odg.upper()
        if (odg == "Y"):
            niz = statistikaMapa+"Statistika_Oznak_1.txt"
            os.system(niz)

        kategorija = input("Kategorija za klasifikacijo: ")
        kategorija = kategorija.upper()

        linPol = input("Linearna ali polinomska oblika jedra: [L... linerna   P... polinomska]")
        linPol = linPol.upper()

        __tmpImeDatoteke = kategorija + "_" + linPol + "/"
        tmpLokacija = statistikaMapa + __tmpImeDatoteke

        try:
            os.mkdir(tmpLokacija)
            os.chdir(tmpLokacija)
            if (linPol == "L"):
                ukaz = BowTrainBinSVM + " -i:"+statistikaMapa+"prvo.bow -t:linear -o:"+tmpLokacija+"prvo.bowmd -cat:"+kategorija
            else:
                ukaz = BowTrainBinSVM + " -i:"+statistikaMapa+"prvo.bow -t:polynomial -ker_p:3 -o:"+tmpLokacija+"prvo.bowmd -cat:"+kategorija
            os.system(ukaz)
        except:
            print("Ta klasifikacija je ze bila opravljena...")
        odg =input("Zelis ponoviti klasificiranje? \n0 == Ne\n1 == Da\nIzbira:")
        if (odg != "1"):
            break
    #   Zakljucek ucenja razlicnih klasifikatorjev

    #   preverjanje nad drugim besedilom:
    obdelavaDrugegaBesedila()



def main():
    uvod()
    lokacijeProgramov()
    izgradnjaDatotecneStrukture()
    obdelavaPrvegaBesedila()
    prviDel()
    drugiDel()
    tretjiDel()

if (__name__ == "__main__"):
    main()
