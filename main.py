import re

def validare_name(nume):
    return bool(re.match(r'^[a-zA-Z- ]+$', nume))

def validare_elemente(element):
    if len(element) not in [3, 4]:
        return False
    nume, prenume, cnp = element[:3]
    if not (validare_name(nume) and validare_name(prenume)):
        return False
    if not validare_cnp(cnp):
        return False
    return {'nume': nume, 'prenume': prenume, 'cnp': cnp}

def validare_name(nume):
    return bool(re.match(r'^[a-zA-Z- ]+$', nume))

def validare_cnp(cnp):
    if not (cnp.isdigit() and len(cnp) == 13):
        return False
    if re.match(r'^[+@!?\\/]+$', cnp):
        return False
    cifre = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    cnp_cifre = [int(cifra) for cifra in cnp]
    control_suma = sum([cnp_cifre[i] * cifre[i] for i in range(12)])
    control_cifra = control_suma % 11
    if control_cifra == 10:
        control_cifra = 1
    return control_cifra == cnp_cifre[-1]

def validare_elemente(element):
    if len(element) not in [3, 4]:
        return False
    nume, prenume, cnp = element[:3]
    if not (validare_name(nume) and validare_name(prenume)):
        return False
    if not validare_cnp(cnp):
        return False
    return {'nume': nume, 'prenume': prenume, 'cnp': cnp}

def citire_si_validare_date(data):
    elemente_validate = []
    for element in data:
        if validare_elemente(element):
            elemente_validate.append({"nume": element[0], "prenume": element[1], "cnp": element[2]})
    return elemente_validate

def salvare_catre_fisier(filename, data):
    with open(filename, 'w') as file:
        for element in data:
            line = f"{element['nume']} {element['prenume']} {element['cnp']}\n"
            file.write(line)

def citire_date():
    data = []
    while True:
        nume = input("Introduceti numele: ")
        prenume = input("Introduceti prenumele: ")
        cnp = input("Introduceti CNP-ul: ")
        data.append((nume, prenume, cnp))
        continuare_date = input("Doriti sa mai introduceti alte date? (da/nu): ")
        if continuare_date.lower() != 'da':
            break
    return data

def main():
    data = citire_date()
    date_validate = citire_si_validare_date(data)
    print("Elementele validate:", date_validate)
    #return data, date_validate

    while True:
        comanda = input("Introduceti comanda (salveaza/iesire): ")
        if comanda == "salveaza":
            filename = input("Introduceti un nume fisierului: ")
            salvare_catre_fisier(filename, date_validate)
            print(f"Datele au fost salvate in fisierul {filename}.")
        elif comanda == "iesire":
            print("Datele validate:", date_validate)
            break
        else:
            print("Comanda necunoscuta. Incearca din nou.")

if __name__ == "__main__":
    main()
