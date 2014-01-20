import csv
import simplejson

def number_to_id(ward_no):

    ward_no = str(ward_no)
    if len(ward_no) == 1:
        ward_no = "00" + ward_no
    elif len(ward_no) == 2:
        ward_no = "0" + ward_no
    return "19100" + ward_no


def clean_rand_amount(str_in):

    tmp = str_in.split(".")[0]

    return "R{:,.0f}".format(int(tmp))

data_in = list(csv.reader(open('city_budget.txt', 'rU'), delimiter='\t'))
headings_in = data_in[0]
data_in = data_in[1::]

i_ward = -2
i_cost = -1
i_dept = 3
i_name = 4
i_desc = 5

print headings_in
print (len(data_in))

projects_by_ward = {}

for row in data_in:
    ward_id = number_to_id(row[i_ward])
    if not projects_by_ward.get(ward_id):
        projects_by_ward[ward_id] = []
    projects_by_ward[ward_id].append({
        "cost": clean_rand_amount(row[i_cost]),
        "department": row[i_dept],
        "name": row[i_name],
        "description": row[i_desc]
    })

tmp = projects_by_ward["19100020"]
for project in tmp:
    print project

print len(projects_by_ward)

f = open('../data_budget.json', 'w')
f.write(simplejson.dumps(projects_by_ward, indent=4))