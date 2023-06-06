from datetime import datetime

def get_ind_fam_details(gedcomfile):
    individuals = []
    individual = []
    indidict = {}
    is_individual = False

    for line in gedcomfile:
        if "INDI" in line:
            if individual:
                individuals.append(individual)
            individual = [line]
            is_individual = True
        elif is_individual:
            if line.startswith(("0 @", "1 @", "2 @")):
                individuals.append(individual)
                individual = []
                is_individual = False
            else:
                individual.append(line)

    if individual:
        individuals.append(individual)
    id = None
    for person in individuals:
        for details in range(0, len(person)):
            if 'INDI' in person[details]:
                detail = person[details].split('@')
                id = detail[1]
                indidict[f'{id}'] = {'id': id}
            elif 'NAME' in person[details]:
                detail = person[details].replace('1 NAME ', '')
                indidict[f'{id}']['Name'] = detail
            elif 'SEX' in person[details]:
                detail = person[details].split(' ')
                indidict[f'{id}']['Gender'] = detail[2]
            elif 'BIRT' in person[details]:
                next = details + 1
                indidict[f'{id}']['Alive'] = 'True'
                indidict[f'{id}']['Death'] = 'N/A'
                indidict[f'{id}']['Child'] = 'N/A'
                indidict[f'{id}']['Spouse'] = 'N/A'
                if 'DATE' in person[next]:
                    detail = person[next]
                    detail = detail.replace('2 DATE ', '')
                    detail = datetime.strptime(detail, "%d %b %Y")
                    detail = detail.strftime("%Y-%m-%d")
                    birth = detail
                    birth_date = datetime.strptime(birth, "%Y-%m-%d")
                    current_date = datetime.now()
                    age = current_date.year - birth_date.year
                    if current_date.month < birth_date.month or (current_date.month == birth_date.month and current_date.day < birth_date.day):
                        age -= 1
                    indidict[f'{id}']['Age'] = age
                    indidict[f'{id}']['Birthday'] = detail
            elif 'DEAT' in person[details]:
                next = details + 1
                indidict[f'{id}']['Alive'] = 'False'
                if 'DATE' in person[next]:
                    detail = person[next]
                    detail = detail.replace('2 DATE ', '')
                    detail = datetime.strptime(detail, "%d %b %Y")
                    detail = detail.strftime("%Y-%m-%d")
                    death = detail
                    death_date = datetime.strptime(death, "%Y-%m-%d")
                    indidict[f'{id}']['Death'] = detail
                    age = death_date.year - birth_date.year
                    if death_date.month < birth_date.month or (death_date.month == birth_date.month and death_date.day < birth_date.day):
                        age -= 1
                    indidict[f'{id}']['Age'] = age
            elif 'FAMS' in person[details]:
                detail = person[details].split('@')
                spouseid = detail[1]
                indidict[f'{id}']['Spouse'] = "{\'" + f"{spouseid}" + "\'}"

            elif 'FAMC' in person[details]:
                detail = person[details].split('@')
                childid = detail[1]
                indidict[f'{id}']['Child'] = "{\'" + f"{childid}" + "\'}"

    
    for i, j in indidict.items():
        print(i, j)
        print('\n\n')

    # Return Families
    return indidict


def display_gedcom_table(individuals, families):
    # Print Individuals table
    print("Individuals:")
    for individual in individuals:
        print(individual)

    # Print Families table
    print("Families:")
    for family in families:
        print(family)


if __name__ == "__main__":
    with open("Shubham_Gedcome.ged", "r") as gedcomf:
        gedcomfile = gedcomf.readlines()
        gedcomfile = [line.rstrip('\n') for line in gedcomfile]

        # Retrieve the Individuals and Family from the input file
        individuals, families = get_ind_fam_details(gedcomfile)

        # Print The details using Pretty Table Library
        display_gedcom_table(individuals, families)
