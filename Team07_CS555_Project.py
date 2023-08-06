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


#User Story: 09 - Birth before marriage of parents


def US09_birth_before_death_of_parents(family, individuals):
    Error09 = []
    for id in family:
        children = family[id]['Children']
        marriage_date = datetime.strptime(family[id]['Married'], "%Y-%m-%d")
        for child_id in children:
            child_birth = individuals[child_id]['Birthday']
            child_birth_date = datetime.strptime(child_birth, '%Y-%m-%d')
            if child_birth_date < marriage_date:
                Error09.append(f"ERROR US09: {individuals[child_id]['id']} {individuals[child_id]['Name']} {individuals[child_id]['Birthday']}")
    return Error09
    

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

# User Story: 11 - No bigamy: Marriage should not occur during marriage to another spouse
def US11_No_Bigamy(family, individuals):
    Error11 = []
    marriage_dates = {}
    widowed_flag = 0
    for fam_id in family:
        husband_id = family[fam_id]['Husband ID']
        wife_id = family[fam_id]['Wife ID']
        if family[fam_id]['Divorced'] == 'NA':
            if individuals[husband_id]['Death'] != 'NA':
                husband_death = individuals[husband_id]['Death']
                if husband_death:
                    widowed_flag = 1
        if husband_id in marriage_dates and marriage_dates[husband_id] >= family[fam_id]['Married']:
            Error11.append(f"ERROR US11: Bigamy detected for husband {husband_id} in family {fam_id}")
        if wife_id in marriage_dates and marriage_dates[wife_id] >= family[fam_id]['Married'] and widowed_flag==0:
            Error11.append(f"ERROR US11: Bigamy detected for wife {wife_id} in family {fam_id}")
        marriage_dates[husband_id] = family[fam_id]['Married']
        marriage_dates[wife_id] = family[fam_id]['Married']

    return Error11

# User Story: 12 - Parents not too old: Mother should be less than 60 years older than her children and father should be less than 80 years older than his children

def US12_Parents_not_too_old(family, individuals):
    Error12 = []
    child_ids = []
    for id in family:
        father_id = family[id]['Husband ID']
        mother_id = family[id]['Wife ID']
        child_ids = family[id]['Children']

        if individuals[father_id]['Alive'] == 'False':
            date = datetime.strptime(individuals[father_id]['Death'], "%Y-%m-%d")
        else:
            date = datetime.now()
        father_age = date.year - datetime.strptime(individuals[father_id]['Birthday'], "%Y-%m-%d").year

        if individuals[mother_id]['Alive'] == 'False':
            date = datetime.strptime(individuals[mother_id]['Death'], "%Y-%m-%d")
        else:
            date = datetime.now()
        mother_age = date.year - datetime.strptime(individuals[mother_id]['Birthday'], "%Y-%m-%d").year

        for child in child_ids:
            if individuals[child]['Alive'] == 'False':
                date = datetime.strptime(individuals[child]['Death'], "%Y-%m-%d")
            else:
                date = datetime.now()
            child_age = date.year - datetime.strptime(individuals[child]['Birthday'], "%Y-%m-%d").year

            if father_age - 80 > child_age or mother_age - 60 > child_age:
                Error12.append(f"Child {child} has parents too old to him")
            
    return Error12

#User Story: 13 - Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
def US13_siblings_spacing(individuals, family):
    Error13 = []

    for id in family:
        child_ids = family[id]['Children']

        if len(child_ids) > 1:
            children = []
            for i in range(len(child_ids)):
                children.append(individuals[child_ids[i]])
            for i in range(len(children)):
                for j in range(i + 1, len(children)):
                    child = children[i]
                    sibling = children[j]
                    child_birth = datetime.strptime(child['Birthday'], "%Y-%m-%d")
                    sibling_birth = datetime.strptime(sibling['Birthday'], "%Y-%m-%d")
                    birthdelta = relativedelta(child_birth, sibling_birth)
                    if birthdelta.days > 2 or (birthdelta.days == 2 and birthdelta.seconds > 0) or birthdelta.months < 8:
                        Error13.append("Sibling birthdays should be less than 2 days apart or greater than 8 months apart.\nChild IDs with Error: " + str(child_ids))
    return Error13

#User Story: 14 - No more than five siblings should be born at the same time
def US14_multiple_births_less_than_5(individuals, family):
    Error14 = []

    for id in family:
        child_ids = family[id]['Children']

        if len(child_ids) > 0:
            children = {}
            for i in range(len(child_ids)):
                children.update(individuals[child_ids[i]])
            birthdays = []
            for i in range(len(children)):
                birthdays.append(children['Birthday'])
            birthdays.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
            birthdays = [datetime.strptime(birthday, '%Y-%m-%d') for birthday in birthdays]
            count = 0
            for i in range(len(birthdays)):
                compare_date = birthdays[i]
                day_range = 2
                birthdays_in_range = []
                for birthday in birthdays:
                    if compare_date - relativedelta(days=day_range) <= birthday <= compare_date + relativedelta(days=day_range):
                        birthdays_in_range.append(birthday)
                if len(birthdays_in_range) > 5:
                    Error14.append("No more than five siblings should be born at the same time.\n Child IDs with Error: " + str(child_ids))
                    break
    return Error14
# User Story: 15 - Fewer than 15 siblings: There should be fewer than 15 siblings in a family

def US15_Fewer_than_15_siblings(family):
    Error15 = []
    for fam_id in family.keys():
        if "Children" in family[fam_id]:
            num_siblings = len(family[fam_id]["Children"])
            print(num_siblings)
            if num_siblings >= 15:
                Error15.append(f"ERROR US15: {fam_id} has {num_siblings} siblings, which is more than 15.")
    return Error15

# User Story: 16 - Male last name: All male members of a family should have the same last name

def US16_Male_Last_Name(individuals, family):
    Error16 = []
    for fam_id in family.keys():
        if "Husband ID" in family[fam_id]:
            father_last_name = family[fam_id]["Husband Lastname"]
            if "Children" in family[fam_id]:
                for child_id in family[fam_id]["Children"]:
                    if individuals[child_id]["Gender"] == "M" and individuals[child_id]["Lastname"] != father_last_name:
                        Error16.append(f"ERROR US16: {individuals[child_id]['Name']} has a different last name: {individuals[child_id]['Lastname']} than the father's last name: {father_last_name}")
    return Error16


# User Story: 17 - Parents should not marry any of their descendants
def US17_Parent_Shouldnt_marry_descendants(individuals, family):
    Error17 = []

    def is_spouse_descendant(person_id, spouse_id):
        if person_id not in individuals or spouse_id not in individuals:
            return False
        if spouse_id in individuals[person_id]['Child']:
            return True
        for child_id in individuals[person_id]['Child']:
            if is_spouse_descendant(child_id, spouse_id):
                return True
        return False

    for fam_id, family_data in family.items():
        if "Husband ID" in family_data and "Children" in family_data:
            husband_id = family_data["Husband ID"]
            children = family_data["Children"]
            for child_id in children:
                # Check if the husband (father) is marrying one of their descendants (children)
                if child_id == husband_id or is_spouse_descendant(husband_id, child_id):
                    Error17.append(f"ERROR US17: {individuals[husband_id]['Name']} (ID: {husband_id}) is marrying their descendant: {individuals[child_id]['Name']} (ID: {child_id})")
        
        if "Wife ID" in family_data and "Children" in family_data:
            wife_id = family_data["Wife ID"]
            children = family_data["Children"]
            for child_id in children:
                # Check if the wife (mother) is marrying one of their descendants (children)
                if child_id == wife_id or is_spouse_descendant(wife_id, child_id):
                    Error17.append(f"ERROR US17: {individuals[wife_id]['Name']} (ID: {wife_id}) is marrying their descendant: {individuals[child_id]['Name']} (ID: {child_id})")
    
    return Error17

# User Story: 18 - Siblings should not marry one another
def US18_Siblings_Shouldnt_Marry(individuals, family):
    Error18 = []

    for fam_id, family_data in family.items():
        if "Children" in family_data:
            children = family_data["Children"]
            for i in range(len(children)):
                for j in range(i + 1, len(children)):
                    sibling1_id = children[i]
                    sibling2_id = children[j]
                    if sibling1_id in individuals and sibling2_id in individuals:
                        sibling1_parents = (individuals[sibling1_id].get("Husband ID"), individuals[sibling1_id].get("Wife ID"))
                        sibling2_parents = (individuals[sibling2_id].get("Husband ID"), individuals[sibling2_id].get("Wife ID"))
                        if sibling1_parents == sibling2_parents and sibling1_parents != ("NA", "NA"):
                            Error18.append(f"ERROR US18: Siblings {individuals[sibling1_id]['Name']} (ID: {sibling1_id}) and {individuals[sibling2_id]['Name']} (ID: {sibling2_id}) are married to each other.")
    
    return Error18

def is_sibling(individual_1, individual_2, family):
    if not individual_1 or not individual_2:
        return False

    father_1_id = eval(individual_1.get('Spouse', 'NA'))
    mother_1_id = eval(individual_1.get('Child', 'NA'))
    father_2_id = eval(individual_2.get('Spouse', 'NA'))
    mother_2_id = eval(individual_2.get('Child', 'NA'))

    if not father_1_id or not mother_1_id or not father_2_id or not mother_2_id:
        return False

    return (father_1_id == father_2_id) and (mother_1_id == mother_2_id)


NA = 'NA'

def is_sibling(individual_1, individual_2, family):
    if not individual_1 or not individual_2:
        return False

    father_1_id = eval(individual_1.get('Spouse', NA))
    mother_1_id = eval(individual_1.get('Child', NA))
    father_2_id = eval(individual_2.get('Spouse', NA))
    mother_2_id = eval(individual_2.get('Child', NA))

    if not father_1_id or not mother_1_id or not father_2_id or not mother_2_id:
        return False

    return (father_1_id == father_2_id) and (mother_1_id == mother_2_id)


# User Story: 19 - First cousins should not marry: First cousins should not marry one another
def US19_First_Cousin_should_not_marry(family, individuals):
    Error19 = []

    for family_info in family.values():
        children = family_info.get('Children', [])
        if len(children) > 1:
            for i in range(len(children)):
                for j in range(i + 1, len(children)):
                    cousin_1_id = children[i]
                    cousin_2_id = children[j]

                    individual_1 = individuals.get(cousin_1_id, {})
                    individual_2 = individuals.get(cousin_2_id, {})

                    if is_sibling(individual_1, individual_2, family):
                        Error19.append((cousin_1_id, cousin_2_id))

    return Error19


# User Story: 20 - Aunts and uncles: Aunts and uncles should not marry their nieces or nephews
def US20_Aunts_and_uncles(individuals, family):
    Error20 = []

    for fam_info in family.values():
        aunts_uncles_ids = set()

        for child_id in fam_info.get('chil', []):
            child_info = individuals.get(child_id[0], {})
            if not child_info:
                continue

            parents = child_info.get('Spouse', NA)
            if parents != NA:
                parents_ids = eval(parents)
                aunts_uncles_ids.update(parents_ids)

        husb_id = fam_info.get('husbId', [None])[0]
        wife_id = fam_info.get('wifeId', [None])[0]

        if husb_id:
            aunts_uncles_ids.discard(husb_id)
        if wife_id:
            aunts_uncles_ids.discard(wife_id)

        for aunt_uncle_id in aunts_uncles_ids:
            nieces_nephews_ids = []
            for fam_id, fam in family.items():
                if fam_id == fam_info['id']:
                    continue

                for child_id in fam.get('chil', []):
                    if child_id[0] == aunt_uncle_id:
                        nieces_nephews_ids.append(aunt_uncle_id)
                        break

            for niece_nephew_id in nieces_nephews_ids:
                Error20.append((aunt_uncle_id, niece_nephew_id))

    return Error20

#User Story: 21 - Correct gender for role: Husband in family should be male and wife in family should be female
def US21_correct_gender_for_role(individuals, family):
    Error21 = []
    for family_id in family.keys():
        husband_id = family[family_id]["Husband ID"]
        wife_id = family[family_id]["Wife ID"]
        if individuals[husband_id]["Gender"] != "M":
            Error21.append("Husband ID " + str(husband_id) + "has the incorrect gender role.")
        if individuals[wife_id]["Gender"] != "F":
            Error21.append("Wife ID " + str(wife_id) + "has the incorrect gender role.")
    return Error21

#User Story: 22 - Unique IDs: All individual IDs should be unique and all family IDs should be unique
def US22_unique_IDs(individuals, family):
    Error22 = []
    for id in family:
        compare_id = id
        count = 0
        duplicates = []
        for id in family:
            if id == compare_id:
                count += 1
        if count > 1:
            if compare_id in duplicates:
                pass
            else:
                Error22.append("Family ID " + str(compare_id) + " is a duplicate.")
                duplicates.append(compare_id)
    for id in individuals:
        compare_id = id
        count = 0
        duplicates = []
        for id in individuals:
            if id == compare_id:
                count += 1
        if count > 1:
            if compare_id in duplicates:
                pass
            else:
                Error22.append("Individual ID " + str(compare_id) + " is a duplicate.")
                duplicates.append(compare_id)
    return Error22

#User Story: 23 Unique name and birth date: No more than one individual with the same name and birth date should appear in a GEDCOM file
def US23_Unique_Name_and_Birth_Date(individuals):
    unique_ids = {}  # Dictionary to store the combination of name and birth date as unique identifiers
    Error23 = []

    for ind_id in individuals:
        
        name = individuals[ind_id]['Name']
        birth_date = individuals[ind_id]['Birthday']

        # Create a unique identifier by concatenating the name and birth date
        identifier = f"{name}|{birth_date}"

        if identifier in unique_ids:
            # If the identifier is already present in the dictionary, it indicates a duplicate
            # Add an error message to the error_list
            
            Error23.append(f"ERROR US23: individual found with same name {name} and birth date {birth_date}")
            
        # Add the identifier to the dictionary to keep track of encountered individuals
        unique_ids[identifier] = ind_id

    return Error23

# User Story: 24: Unique families by spouses: No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
def US24_Unique_Families_by_Spouses(family):
    unique_families = {}  # Dictionary to store the combination of spouses' names and marriage dates as unique identifiers
    Error24 = []

    for fam_id in family:
        husband_name = family[fam_id]['Husband Name']
        wife_name = family[fam_id]['Wife Name']
        marriage_date = family[fam_id]['Married']

        # Create a unique identifier by concatenating the spouses' names and marriage date
        identifier = f"{husband_name}|{wife_name}|{marriage_date}"

        if identifier in unique_families:
            # If the identifier is already present in the dictionary, it indicates a duplicate
            # Add an error message to the error_list
            Error24.append(f"ERROR US24: Duplicate family found with spouses {husband_name} and {wife_name} " +
                              f"and marriage date {marriage_date}")

        # Add the identifier to the dictionary to keep track of encountered families
        unique_families[identifier] = fam_id

    return Error24

#User Story 29: List deceased - List all deceased individuals in a GEDCOM file
def US29_list_deceased(individuals):
    List29 = []

    for id in individuals.keys():
        if individuals[id]['Alive'] == 'False':
            List29.append(individuals[id]['Name'] + " " +  individuals[id]['Lastname'])

    return List29

#User Story 30: List living married - List all living married peopole in a GEDCOM file
def US30_list_living_married(individuals):
    List30 = []

    for id in individuals.keys():
        if individuals[id]['Alive'] == 'True' and individuals[id]['Spouse'] != 'NA':
            List30.append(individuals[id]['Name'] + " " +  individuals[id]['Lastname'])

    return List30

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
                indidict[f'{id}']['Lastname'] = 'NA'
                indidict[f'{id}']['Gender'] = 'NA'
                indidict[f'{id}']['Birthday'] = 'NA'
                indidict[f'{id}']['Death'] = 'NA'
                indidict[f'{id}']['Alive'] = 'False'
                indidict[f'{id}']['Child'] = 'NA'
                indidict[f'{id}']['Spouse'] = 'NA'
            elif 'GIVN' in person[details]:
                detail = person[details].replace('2 GIVN ', '')
                indidict[f'{id}']['Name'] = detail
            elif 'SURN' in person[details]:
                detail = person[details].replace('2 SURN ', '')
                indidict[f'{id}']['Lastname'] = detail
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
                famdict[f'{id}']['Husband Lastname'] = 'NA'
                famdict[f'{id}']['Wife ID'] = 'NA'
                famdict[f'{id}']['Wife Name'] = 'NA'
                famdict[f'{id}']['Wife Lastname'] = 'NA'
                famdict[f'{id}']['Married'] = 'NA'
                famdict[f'{id}']['Divorced'] = 'NA'
                famdict[f'{id}']['Children'] = [] 
            elif 'HUSB' in fam[details]:
                detail = fam[details].split('@')
                husbid = detail[1]
                famdict[f'{id}']['Husband ID'] = husbid
                famdict[f'{id}']['Husband Name'] = indidict.get(husbid, {}).get('Name', 'Unknown')
                famdict[f'{id}']['Husband Lastname'] = indidict.get(husbid, {}).get('Lastname', 'Unknown')
            elif 'WIFE' in fam[details]:
                detail = fam[details].split('@')
                wifeid = detail[1]
                famdict[f'{id}']['Wife ID'] = wifeid
                famdict[f'{id}']['Wife Name'] = indidict.get(wifeid, {}).get('Name', 'Unknown')
                famdict[f'{id}']['Wife Lastname'] = indidict.get(wifeid, {}).get('Lastname', 'Unknown')
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
        inditable.field_names = ['ID', 'Name', 'Lastname', 'Gender', 'Birthday', 'Death', 'Alive', 'Child', 'Spouse', 'Age']
        for i in individuals.keys():
            inditable.add_row(list(individuals[i].values()))
        output_tables += 'Individuals:' + '\n' + str(inditable) + '\n'

        #print(family)
        #Print Families table
        famtable = PrettyTable()
        famtable.field_names = ['ID', 'Husband ID', 'Husband Name', 'Husband Lastname', 'Wife ID', 'Wife Name', 'Wife Lastname', 'Married', 'Divorced', 'Children']
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

        # User Story: 10 - Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
        Error10 = US10_marriage_after_14(family, individuals)
        output += "User Story: 10 - Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)\n\nErrors related to Parents married under 14 years (US10)\n: " + str(Error10) + "\n\n" + "These are the details for who were married below 14 years." + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story: 11 - No bigamy: Marriage should not occur during marriage to another spouse
        Error11 = US11_No_Bigamy(family, individuals)
        output += "User Story: 11 - No bigamy: Marriage should not occur during marriage to another spouse\n\nErrors related to Bigamy (US11):\n" + str(Error11) + "\n\n" + "These are errors related to Bigamy." + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story: 12 - Parents not too old: Mother should be less than 60 years older than her children and father should be less than 80 years older than his children
        Error12 = US12_Parents_not_too_old(family, individuals)
        output += "User Story: 12 - Parents not too old: Mother should be less than 60 years older than her children and father should be less than 80 years older than his children\n\nErrors related to Too old parents (US12):\n" + str(Error12) + "\n\n" + "These are errors related to Parents who are too old to their child." + "\n"
        output+= "------------------------------------------------------------------------------"
        
        # User Story: 13 - Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
        Error13 = US13_siblings_spacing(individuals, family)
        output += "User Story: 13 - Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)\n\nErrors related to siblings birthday too close (US13):\n" + str(Error13) + "\n\n" + "These errors are related to siblings whose birthdays are too close together." + "\n"
        output+= "------------------------------------------------------------------------------"

        #User Story: 14 - No more than five siblings should be born at the same time
        Error14 = US14_multiple_births_less_than_5(individuals, family)
        output += "User Story: 14 - No more than five siblings should be born at the same time\n\nErrors related to more than five siblings being born at the same time:\n" + str(Error14) + "\n\n" + "These errors are related to more than five siblings being born at the same time, exceeding the reasonable limit." + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story: 15 - Fewer than 15 siblings: There should be fewer than 15 siblings in a family
        Error15 = US15_Fewer_than_15_siblings(family)
        output += "User Story: 15 - There should be fewer than 15 siblings in a family\n\nErrors related to more than 15 siblings (US15)\n: " + str(Error15) + "\n\n" + "These are the details of fewer than 15 siblings in a family." + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story: 16 - Male last name: All male members of a family should have the same last name
        Error16 = US16_Male_Last_Name(individuals, family)
        output += "User Story: 16 - All male members of a family should have the same last name\n\nErrors related to All male members of a family should have the same last name (US16)\n: " + str(Error16) + "\n\n" + "These are the details of All male members of a family should have the same last name." + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story: 17 - No marriages to descendants: Parents should not marry any of their descendants
        Error17 = US17_Parent_Shouldnt_marry_descendants(individuals, family)
        output += "User Story: 17 - Parents should not marry any of their descendants\n\nErrors related to marriage to descendants:\n" + str(Error17) + "\n\n" + "These are the parents identified as married to descendants." + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story: 18 - Siblings should not marry: Siblings should not marry one another
        Error18 = US18_Siblings_Shouldnt_Marry(individuals, family)
        output += "User Story: 18 - Siblings should not marry one another\n\nErrors related to siblings marrying each other:\n" + str(Error18) + "\n\n" + "These are the siblings who are married to each other." + "\n"
        output+= "------------------------------------------------------------------------------"

        #User Story: 19 - First cousins should not marry: First cousins should not marry one another

        Error19 = US19_First_Cousin_should_not_marry(family, individuals)
        output += "User Story: 19 - First cousins should not marry: First cousins should not marry one another\n\n(US19)\n: " + str(Error19) + "\n\n" + "These are the details of all first cousins who are married" + "\n"
        output+= "------------------------------------------------------------------------------"

        #User Story: 20 - Aunts and uncles: Aunts and uncles should not marry their nieces or nephews

        Error20 = US20_Aunts_and_uncles(family, individuals)
        output += "User Story: 20 - Aunts and uncles: Aunts and uncles should not marry their nieces or nephews\n\n(US20)\n: " + str(Error20) + "\n\n" + "These are the details of all uncles and aunts who are married to their nieces or nephews" + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story: 21 - Correct gender for role
        Error21 = US21_correct_gender_for_role(individuals, family)
        output += "User Story: 21 - Husband in family should be male and wife in family should be female\n\nErrors related to incorrect gender for roles:\n" + str(Error21) + "\n\n" + "These errors are for either a father or mother having the incorrect gender." + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story: 22 - Unique IDs
        Error22 = US22_unique_IDs(individuals, family)
        output += "User Story: 22 - All individual IDs should be unique and all family IDs should be unique\n\nErrors related to duplicate IDs:\n" + str(Error22) + "\n\n" + "These errors are for duplicate family or individual IDs." + "\n"
        output+= "------------------------------------------------------------------------------"

        #User Story 23: Unique name and birth date: No more than one individual with the same name and birth date should appear in a GEDCOM file
        Error23 = US23_Unique_Name_and_Birth_Date(individuals)
        output += "User Story: 23 - No more than one individual with the same name and birth date\n\nErrors related to No more than one individual with the same name and birth date(US23)\n: " + str(Error23) + "\n\n" + "These are the details of No more than one individual with the same name and birth date." + "\n"
        output+= "------------------------------------------------------------------------------"
        
        # User Story 24: Unique families by spouses: No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
        Error24 = US24_Unique_Families_by_Spouses(family)
        output += "User Story: 24 - No more than one family with the same spouses by name and the same marriage date \n\nErrors related to No more than one family with the same spouses by name and the same marriage date(US24)\n: " + str(Error23) + "\n\n" + "These are the details of No more than one family with the same spouses by name and the same marriage date ." + "\n"
        output+= "------------------------------------------------------------------------------"

        # User Story 29: List deceased - List all deceased individuals in a GEDCOM file
        List29 = US29_list_deceased(individuals)
        output += "User Story 29: List of all deceased people in the GEDCOM file:\n" + str(List29) + "\n\n"
        output+= "------------------------------------------------------------------------------"

        # User Story 30: List living married - List all living married people in a GEDCOM file
        List30 = US30_list_living_married(individuals)
        output += "User Story 30: List of all living people who are married in the GEDCOM file:\n" + str(List30) + "\n\n"
        output+= "------------------------------------------------------------------------------"

        with open("M4B3_Sprint1_Ouput.txt", "w") as out:
            out.write(output)

        print(family)
        print(individuals)
