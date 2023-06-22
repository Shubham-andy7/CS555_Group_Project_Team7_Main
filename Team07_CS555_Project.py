from datetime import datetime
from prettytable import PrettyTable
from dateutil.relativedelta import relativedelta

#User Story: 01 - Dates before current date
def US1_dates_before_current_date(individuals, family):
    Error01_individuals = []
    Error01_family = []
    for id in individuals:
        if individuals[id]['Death']!='NA':
            deathday = datetime.strptime(individuals[id]["Death"], "%Y-%m-%d")
            birthday = datetime.strptime(individuals[id]["Birthday"], "%Y-%m-%d")
            if deathday > datetime.now():
                Error01_individuals.append(individuals[id])
            if birthday > datetime.now():
                Error01_individuals.append(individuals[id])

    for id in family:
        if family[id]["Divorced"] != 'NA':
            divorceday = datetime.strptime(family[id]["Divorced"], "%Y-%m-%d")
            marriageday = datetime.strptime(family[id]["Married"], "%Y-%m-%d")
            if divorceday > datetime.now():
                Error01_family.append(family[id])
            if marriageday > datetime.now():
                Error01_family.append(family[id])

    return Error01_individuals, Error01_family
            
#User Story: 02 - Birth before marriage
def US2_birth_before_marriage(individuals, family):
    Error02 = {'individuals': [], 'family': []}
    for id_indiv in individuals:
        indiv = individuals[id_indiv]
        spouse_id = indiv['Spouse'].strip("{}'")  # Extract spouse ID from the string
        if spouse_id in family:
            fam = family[spouse_id]
            if fam['Married'] != 'NA':
                marriageday = datetime.strptime(fam['Married'], "%Y-%m-%d")
                birthday = datetime.strptime(indiv['Birthday'], "%Y-%m-%d")
                if birthday.date() > marriageday.date():
                    Error02['individuals'].append(indiv)
                    Error02['family'].append(fam)
    return Error02

#User Story: 03 - Birth before death
def US3_birth_before_death(individuals):
    Error03 = []
    for id in individuals:
        if individuals[id]["Death"] != 'NA':
            deathday = datetime.strptime(individuals[id]["Death"], "%Y-%m-%d")
            birthday = datetime.strptime(individuals[id]["Birthday"], "%Y-%m-%d")
            if deathday < birthday:
                Error03.append(individuals[id])
    return Error03

#User Story: 04 - Marriage before divorce
def US4_marriage_before_divorce(family):
    Error04 = []
    for id in family:
        if family[id]["Divorced"] != 'NA':
            divorceday = datetime.strptime(family[id]["Divorced"], "%Y-%m-%d")
            marriageday = datetime.strptime(family[id]["Married"], "%Y-%m-%d")
            if divorceday < marriageday:
                Error04.append(family[id])
    return Error04

#User Story 05: Marriage before death error check
def US5_marriage_before_death(individuals, family):
    Error05 = []
    for id in family:
        if family[id]['Married'] != 'NA':
            marriage_date = datetime.strptime(family[id]['Married'], "%Y-%m-%d")
            husband_id = family[id]['Husband ID']
            wife_id = family[id]['Wife ID']
            if individuals[husband_id]['Death'] != 'NA':
                husband_dday = datetime.strptime(individuals[husband_id]['Death'], "%Y-%m-%d")
                if husband_dday < marriage_date:
                    Error05.append(individuals[husband_id])
            if individuals[wife_id]['Death'] != 'NA':
                wife_dday = datetime.strptime(individuals[wife_id]['Death'], "%Y-%m-%d")
                if wife_dday < marriage_date:
                    Error05.append(individuals[wife_id])
    return Error05

#User Story 06: Divorce before death error check
def US6_divorce_before_death(individuals, family):
    Error06 = []
    for id in family:
        if family[id]['Divorced'] != 'NA':
            divorced_date = datetime.strptime(family[id]['Divorced'], "%Y-%m-%d")
            husband_id = family[id]['Husband ID']
            wife_id = family[id]['Wife ID']
            if individuals[husband_id]['Death'] != 'NA':
                husband_dday = datetime.strptime(individuals[husband_id]['Death'], "%Y-%m-%d")
                if husband_dday < divorced_date:
                    Error06.append(individuals[husband_id])
            if individuals[wife_id]['Death'] != 'NA':
                wife_dday = datetime.strptime(individuals[wife_id]['Death'], "%Y-%m-%d")
                if wife_dday < divorced_date:
                    Error06.append(individuals[wife_id])
    return Error06

# User Story: 07 - Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people
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


# User Story: 08 - Child should be born before the death of the mother and before 9 months after the death of the father
def US8_child_birth_before_parent_death(family, individuals):
    Error08 = []

    for id in family:
        mother_id = family[id]['Wife ID']
        father_id = family[id]['Husband ID']
        children = family[id]['Children']
        mother_death = individuals[mother_id]['Death']
        father_death = individuals[father_id]['Death']

        if mother_death != 'NA' and children:
            mother_death_date = datetime.strptime(mother_death, "%Y-%m-%d")
            for child_id in children:
                child_birth = individuals[child_id]['Birthday']
                child_birth_date = datetime.strptime(child_birth, "%Y-%m-%d")
                if child_birth_date > mother_death_date:
                    Error08.append(f"ERROR US08: {individuals[child_id]['id']} {individuals[child_id]['Name']} {individuals[child_id]['Birthday']} {individuals[mother_id]['Death']} {individuals[father_id]['Death']}")
        
        if father_death != 'NA' and children:
            father_death_date = datetime.strptime(father_death, "%Y-%m-%d")
            for child_id in children:
                child_birth = individuals[child_id]['Birthday']
                child_birth_date = datetime.strptime(child_birth, "%Y-%m-%d")
                if child_birth_date > father_death_date + relativedelta(months=9):
                    Error08.append(f"ERROR US08: {individuals[child_id]['id']} {individuals[child_id]['Name']} {individuals[child_id]['Birthday']} {individuals[mother_id]['Death']} {individuals[father_id]['Death']}")
    
    return Error08

#User Story: 10 - Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
def US10_marriage_after_14(family, individuals):
    Error10 = []

    for id in family:
        
        if family[id]['Married'] != 'NA':
            marriage_date = datetime.strptime(family[id]['Married'], "%Y-%m-%d")
            mother_id = family[id]['Wife ID']
            father_id = family[id]['Husband ID']
            mother_bday = datetime.strptime(individuals[mother_id]['Birthday'], "%Y-%m-%d")
            father_bday = datetime.strptime(individuals[father_id]['Birthday'], "%Y-%m-%d")
            mother_age_at_marriage = relativedelta(marriage_date, mother_bday).years
            if mother_age_at_marriage < 14:
                Error10.append(family[id]['Wife ID'])
            father_age_at_marriage = relativedelta(marriage_date, father_bday).years
            if father_age_at_marriage < 14:
                Error10.append(family[id]['Husband ID'])
    return Error10

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
    with open("Test_Shubham_Gedcom.ged", "r") as gedcomf:
        gedcomfile = gedcomf.readlines()
        gedcomfile = [line.rstrip('\n') for line in gedcomfile]
        output = ""
        # Retrieve the Individuals and Family from the input file
        individuals, family = get_ind_fam_details(gedcomfile)

        # Print The details using Pretty Table Library
        display_gedcom_table(individuals, family)

        # User Story: 01 - Dates before current date
        Error01 = US1_dates_before_current_date(individuals, family)
        output += "User Story: 01 - Dates before current date\n\nErrors related to Dates before current date (US01)\n: " + str(Error01) + "\n\n" + "These are the details for either of the birthdates, deathdates, marriagedates and divorcedates that have occured after the current date." + "\n"
        output+= "------------------------------------------------------------------------------\n\n"

        # User Story: 02 - Birth before marriage
        Error02 = US2_birth_before_marriage(individuals, family)
        output += "User Story: 02 - Birth before marriage\n\nErrors related to birth before marriage (US02)\n: " + str(Error02) + "\n\n" + "These are the details for birth dates that have occured after the marriage date of an individual." + "\n"
        output+= "------------------------------------------------------------------------------\n\n"

        # User Story: 03 - Birth before death
        Error03 = US3_birth_before_death(individuals)
        output += "User Story: 03 - Birth before death\n\nErrors related to Birth before Death (US03)\n: " + str(Error03) + "\n\n" + "These are the details for birth dates that have occured after the death date of an individual." + "\n"
        output+= "------------------------------------------------------------------------------\n\n"

        # User Story: 04 - Marriage before divorce
        Error04 = US4_marriage_before_divorce(family)
        output += "User Story: 04 - Marriage before divorce\n\nErrors related to Marriage before Divorce (US04)\n: " + str(Error04) + "\n\n" + "These are the details for marriage dates that have occured after the divorce date of an individual." + "\n"
        output+= "------------------------------------------------------------------------------\n\n"

        # User Story 05: Marriage before death
        Error05 = US5_marriage_before_death(individuals, family)
        output += "User Story 05: Marriage before death\n\nErrors related to marriage date not being before death date (US05)\n: " + str(Error05) + "\n\n" + "These are the details for marriage dates that have occured after the death date of an individual." + "\n"
        output+= "------------------------------------------------------------------------------\n\n"

        # User Story 06: Divorce before death
        Error06 = US6_divorce_before_death(individuals, family)
        output += "User Story 06: Divorce before death\n\nErrors related to divorce date not being before death date (US06)\n: " + str(Error06) + "\n\n" + "These are the details for divorce dates that have occured after the death date of an individual." + "\n"
        output+= "------------------------------------------------------------------------------\n\n"

        # User Story: 07 - Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people
        Error07 = US7_Death_less_150_after_birth(individuals)
        output += "User Story: 07 - Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people\n\nErrors related to death Less then 150 years after birth (US07)\n: " + str(Error07) + "\n\n" + "These are the details for dead people who had age more than 150 years or alive people with current age more than 150 years." + "\n"
        output+= "------------------------------------------------------------------------------\n\n"

         # User Story: 08 - Child should be born before the death of the mother and before 9 months after the death of the father
        Error08 = US8_child_birth_before_parent_death(family, individuals)
        output += "User Story: 08 - Child should be born before the death of the mother and before 9 months after the death of the father\n\nErrors related to Child birth before parent death (US08)\n: " + str(Error08) + "\n\n" + "These are the details for child who were born after 9 months of death of father or after death of mother." + "\n"
        output+= "------------------------------------------------------------------------------"

        #User Story: 10 - Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
        Error10 = US10_marriage_after_14(family, individuals)
        output += "#User Story: 10 - Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)\n\nErrors related to Parents married under 14 years (US10)\n: " + str(Error10) + "\n\n" + "These are the details for who were married below 14 years." + "\n"
        output+= "------------------------------------------------------------------------------"
        with open("M4B3_Sprint1_Ouput.txt", "w") as out:
            out.write(output)
