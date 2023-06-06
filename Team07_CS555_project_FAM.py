from datetime import datetime

def get_ind_fam_details(gedcomfile):
    families = []
    family = []
    famdict = {}
    is_family = False

    for line in gedcomfile:
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

    if family:
        families.append(family)
    id = None
    for fam in families:
        for details in range(0, len(fam)):
            if 'FAM' in fam[details]:
                detail = fam[details].split('@')
                id = detail[1]
                famdict[f'{id}'] = {'id': id}
            elif 'HUSB' in fam[details]:
                detail = fam[details].split('@')
                husbid = detail[1]
                famdict[f'{id}']['Husband'] = husbid
            elif 'WIFE' in fam[details]:
                detail = fam[details].split('@')
                wifeid = detail[1]
                famdict[f'{id}']['Wife'] = wifeid
            elif 'CHIL' in fam[details]:
                if 'Children' not in famdict[f'{id}']:
                    famdict[f'{id}']['Children'] = []
                detail = fam[details].split('@')
                childid = detail[1]
                famdict[f'{id}']['Children'].append(childid)

    for i, j in famdict.items():
        print(i, j)
        print('\n\n')

    # Return Families
    return famdict


def display_family(families):
    # Print Families table
    print("Families:")
    for family in families:
        print(family)


if __name__ == "__main__":
    with open("Shubham_Gedcome.ged", "r") as gedcomf:
        gedcomfile = gedcomf.readlines()
        gedcomfile = [line.rstrip('\n') for line in gedcomfile]

        # Retrieve the Family details from the input file
        _, families = get_ind_fam_details(gedcomfile)

        # Print the family details
        display_family(families)
