def get_country(name:str):
    Length = int(name[0:3])
    final = 3+Length
    non_junk = name[:final]
    country = non_junk[final-2:final]
    print(country)
    return country


def parse_merchant(name: str):
    Length = int(name[0:3])
    final = 3+Length
    non_junk = name[:final]
    CC = non_junk[3:3+4]
    name = non_junk[7:final-2]
    country = non_junk[final-2:final]
    print(country,CC,name)
    return [CC,name,country]


countries = [ "AR", "BO", "BR", "CL", "CO", "EC", "GY", "PY", "PE", "SR", "UY", "VE" ] 
merchant = parse_merchant("0223004Red Tree GeneralHU not be here he should not be about he should not be here when your mother ")
if merchant[2] in countries:
    print(True,"c")

if 3000 <= int(merchant[0]) <=3308:
    print(True,"cc")