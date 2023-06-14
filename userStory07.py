from datetime import datetime
from prettytable import PrettyTable


'''
Auther: Priyanka Koul
User Story: 07 
 Requirement: Death should be less than 150 years after birth for dead people, 
      and current date should be less than 150 years after birth for all living people

'''
def US7_Death_less_150_after_birth(individuals):

    Error07 = []
    current_date = datetime.now()
    for id in individuals.keys():
        birth = individuals[id]["Birthday"]
        death = individuals[id]["Death"]
        alive = individuals[id]["Alive"]
        
        if alive == 'False' and death != 'NA':
            birth_date = datetime.strptime(birth, "%Y-%m-%d")
            death_date = datetime.strptime(death, "%Y-%m-%d")
            age_at_death = death_date.year - birth_date.year

            if age_at_death > 150:
                Error07.append(f"ERROR US07: {individuals[id]['id']} {individuals[id]['Death']} {individuals[id]['Name']} Age: {age_at_death}")
        
        if alive == 'True':
            birth_date = datetime.strptime(birth, "%Y-%m-%d")
            age = current_date.year - birth_date.year

            if age > 150:
                Error07.append(f"ERROR US07: {individuals[id]['id']} {individuals[id]['Death']} {individuals[id]['Name']} Age: {age}")

    return Error07


def get_ind_fam_details(gedcomfile):
    individuals = []
    individual = []
    indidict = {}
    is_individual = False
    families = []
    family = []
    famdict = {}
    is_family = False

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
        if "FAM" in line:
            if family:
                families.append(family)
            family = [line]
            is_family = True
        elif is_family:
            if line.startswith(("0 @", "1 @", "2 @")):
                families.append(family)
                family = []
                is_family = False
            else:
                family.append(line)

    if individual:
        individuals.append(individual)
    id = None
    for person in individuals:
        for details in range(0, len(person)):
            if 'INDI' in person[details]:
                detail = person[details].split('@')
                id = detail[1]
                indidict[f'{id}'] = {'id': id}
                indidict[f'{id}']['Name'] = detail
                indidict[f'{id}']['Gender'] = 'NA'
                indidict[f'{id}']['Birthday'] = 'NA'
                indidict[f'{id}']['Death'] = 'NA'
                indidict[f'{id}']['Alive'] = 'False'
                indidict[f'{id}']['Child'] = 'NA'
                indidict[f'{id}']['Spouse'] = 'NA'
            elif 'NAME' in person[details]:
                detail = person[details].replace('1 NAME ', '')
                indidict[f'{id}']['Name'] = detail
            elif 'SEX' in person[details]:
                detail = person[details].split(' ')
                indidict[f'{id}']['Gender'] = detail[2]
            elif 'BIRT' in person[details]:
                next = details + 1
                indidict[f'{id}']['Alive'] = 'True'
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
    
    if family:
        families.append(family)
    id = None
    for fam in families:
        for details in range(0, len(fam)):
            if 'FAM' in fam[details]:
                detail = fam[details].split('@')
                id = detail[1]
                famdict[f'{id}'] = {'id': id}
                famdict[f'{id}']['Husband ID'] = 'NA'
                famdict[f'{id}']['Husband Name'] = 'NA'
                famdict[f'{id}']['Wife ID'] = 'NA'
                famdict[f'{id}']['Wife Name'] = 'NA'
                famdict[f'{id}']['Married'] = 'NA'
                famdict[f'{id}']['Divorced'] = 'NA'
                famdict[f'{id}']['Children'] = [] 
            elif 'HUSB' in fam[details]:
                detail = fam[details].split('@')
                husbid = detail[1]
                famdict[f'{id}']['Husband ID'] = husbid
                famdict[f'{id}']['Husband Name'] = indidict.get(husbid, {}).get('Name', 'Unknown')
            elif 'WIFE' in fam[details]:
                detail = fam[details].split('@')
                wifeid = detail[1]
                famdict[f'{id}']['Wife ID'] = wifeid
                famdict[f'{id}']['Wife Name'] = indidict.get(wifeid, {}).get('Name', 'Unknown')
            elif 'CHIL' in fam[details]:
                detail = fam[details].split('@')
                childid = detail[1]
                famdict[f'{id}']['Children'].append(childid)
            
            elif 'MARR' in fam[details]:
                next = details + 1
                if 'DATE' in fam[next]:
                    detail = fam[next]
                    detail = detail.replace('2 DATE ', '')
                    detail = datetime.strptime(detail, "%d %b %Y")
                    detail = detail.strftime("%Y-%m-%d")
                    famdict[f'{id}']['Married'] = detail
            elif 'DIV' in fam[details]:
                next = details + 1
                if 'DATE' in fam[next]:
                    detail = fam[next]
                    detail = detail.replace('2 DATE ', '')
                    detail = datetime.strptime(detail, "%d %b %Y")
                    detail = detail.strftime("%Y-%m-%d")
                    famdict[f'{id}']['Divorced'] = detail
    
    # Return Families
    return indidict, famdict


def display_gedcom_table(individuals, family):
    
    #Print individuals table
    #print(individuals)
    output_tables = ""
    with open('M3_B2_output.txt','w') as output:
        inditable = PrettyTable()
        inditable.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Death', 'Alive', 'Child', 'Spouse', 'Age']
        for i in individuals.keys():
            inditable.add_row(list(individuals[i].values()))
        output_tables += 'Individuals:' + '\n' + str(inditable) + '\n'

        #print(family)
        #Print Families table
        famtable = PrettyTable()
        famtable.field_names = ['ID', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Married', 'Divorced', 'Children']
        for i in family.keys():
            famtable.add_row(list(family[i].values()))
        output_tables += 'Families:' + '\n' + str(famtable) + '\n'

        output.write(output_tables)


if __name__ == "__main__":
    with open("Shubham_Gedcome.ged", "r") as gedcomf:
        gedcomfile = gedcomf.readlines()
        gedcomfile = [line.rstrip('\n') for line in gedcomfile]

        # Retrieve the Individuals and Family from the input file
        individuals, family = get_ind_fam_details(gedcomfile)

        # Print The details using Pretty Table Library
        display_gedcom_table(individuals, family)

        # User Story: 07 - Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people
        Error07 = US7_Death_less_150_after_birth(individuals)
        print("Errors related to death Less then 150 years after birth (US07): ", Error07)