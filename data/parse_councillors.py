import simplejson

def number_to_id(ward_no):

    ward_no = ward_no.split(" ")[-1]
    if len(ward_no) == 1:
        ward_no = "00" + ward_no
    elif len(ward_no) == 2:
        ward_no = "0" + ward_no
    return "19100" + ward_no


f = open('councillors.json', 'r')
# data_in = simplejson.loads("[" + f.read() + "]")
# data_in =  f.read()
# print data_in

councillors = {}

for line in f.readlines():
    # print(line)
    obj_in = simplejson.loads(line)
    print simplejson.dumps(obj_in, indent=4)
    tmp = obj_in["results"][0]
    new_obj = {
        "name": tmp["name"],
    }
    if tmp.get("residence_number"):
        new_obj["telephone"] = tmp["residence_number"]
    elif tmp.get("business_number"):
        new_obj["telephone"] = tmp["business_number"]
    if tmp.get("cellnumber"):
        new_obj["cellphone"] = tmp["cellnumber"]
    if tmp.get("email"):
        new_obj["email"] = tmp["email"]
    if tmp.get("address"):
        new_obj["address"] = tmp["address"]
    if tmp.get("party"):
        new_obj["party"] = tmp["party"]
    if tmp.get("subcouncil"):
        new_obj["subcouncil"] = tmp["subcouncil"]

    ward = number_to_id(tmp["ward"])

    img_name = new_obj['name'].lower().replace(" ", "_") + ".jpg"
    new_obj["image"] = img_name
    print simplejson.dumps(new_obj, indent=4)

    councillors[ward] = new_obj

f.close()

f = open("../instance/data_councillors.json", "w")
f.write(simplejson.dumps(councillors, indent=4))
f.close()