import csv


def carica_da_file(file_path):
    try:
        f=open(file_path,"r",encoding="utf-8")
        reader=csv.DictReader(f, skipinitialspace=True)
        l=[]
        for line in reader:
            l.append(line)

        anni=set()
        for foto in l:
            anni.add(foto['anno'])
        dati={}
        for anno in anni:
            temp=[]
            for el in l:
                if anno==el['anno']:
                    temp.append(el)
            dati[anno]=temp
        f.close()
        return dati

    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):

    codici=set()
    for i in album:
        for j in album[i]:
            codici.add(j["codice"])

    if codice not in codici and mese>=1 and mese<=12:
        try:
            f=open(file_path,"a",encoding="utf-8")
            f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
            f.close()

            anno=str(anno)
            mese=str(mese)

            foto={"codice":codice,"titolo":titolo,"autore":autore,"mese":mese,"anno":anno}
            if anno in album:
                album[anno].append(foto)
            else:
                album[anno]=[foto]

            return foto

        except FileNotFoundError:
            return None

    else:
        return None


def cerca_foto(album, codice):

    presente=False
    for anno in album:
        for foto in album[anno]:
            if foto["codice"]==codice:
                presente=True
                return foto["codice"]+", "+foto["titolo"]+", "+foto["autore"]+", "+foto["mese"]+", "+foto["anno"]

    if not presente:
        return None


def elenco_foto_anno_per_titolo(album, anno):
    anno=str(anno)
    if anno in album:
        titoli=[]
        for foto in album[anno]:
            titoli.append(foto["titolo"])

        return sorted(titoli)
    else:
        return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
