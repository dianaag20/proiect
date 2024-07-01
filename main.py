import re
import csv

class InvalidCNPException(Exception):
    pass

def validare_name(nume):
    return bool(re.match(r'^[a-zA-Z- ]+$', nume))

def validare_cnp(cnp):
    if not (cnp.isdigit() and len(cnp) == 13):
        raise InvalidCNPException("CNP-ul trebuie să conțină exact 13 cifre.")
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
    try:
        if not validare_cnp(cnp):
            return False
    except InvalidCNPException as e:
        print(f"Invalid CNP: {e}")
        return False
    return {'nume': nume, 'prenume': prenume, 'cnp': cnp}

def citire_si_validare_date(data):
    elemente_validate = []
    for element in data:
        if validare_elemente(element):
            elemente_validate.append({"nume": element[0], "prenume": element[1], "cnp": element[2]})
    return elemente_validate

def salvare_catre_fisier(filename, data, format_fisier):
    if format_fisier == "txt":
        with open(filename, 'w') as file:
            for element in data:
                line = f"{element['nume']} {element['prenume']} {element['cnp']}\n"
                file.write(line)
    elif format_fisier == "csv":
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['nume', 'prenume', 'cnp'])
            writer.writeheader()
            for element in data:
                writer.writerow(element)

def capitalize_name(name):
    return ' '.join(word.capitalize() for word in name.split())

def citire_date():
    data = []
    while True:
        nume = input("Introduceti numele: ").strip()
        prenume = input("Introduceti prenumele: ").strip()
        nume = capitalize_name(nume)
        prenume = capitalize_name(prenume)
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

    while True:
        comanda = input("Introduceti comanda (salveaza/iesire): ")
        if comanda == "salveaza":
            format_fisier = input("Introduceti formatul fisierului (txt/csv): ").lower()
            filename = input("Introduceti numele fisierului: ")
            if format_fisier in ["txt", "csv"]:
                salvare_catre_fisier(filename, date_validate, format_fisier)
                print(f"Datele au fost salvate in fisierul {filename}.")
            else:
                print("Format necunoscut. Folositi 'txt' sau 'csv'.")
        elif comanda == "iesire":
            print("Datele validate:", date_validate)
            break
        else:
            print("Comanda necunoscuta. Incearca din nou.")

if __name__ == "__main__":
    main()
