"""
Compile a list of wards, together with their details, ready to be imported as javascript.

The ward info was copied from:
    http://www.capetown.gov.za/en/councilonline/Pages/ViewWardDetails.aspx?FirstWardSequenceNo=1&LastWardSequenceNo=
"""

import simplejson


def number_to_id(ward_no):

    tmp = str(ward_no)
    if len(tmp) == 1:
        tmp = "00" + tmp
    elif len(tmp) == 2:
        tmp = "0" + tmp
    return "19100" + tmp


f = open('ward_info.txt', 'r')
f2 = open('static/ward-info.js', 'w')

f2.write("wards = [\n")
lines = f.readlines()
for i in range(len(lines)):
    line = lines[i]
    tmp = line.split('\t')
    ward_no = int(tmp[0].split(" ")[-1])
    ward_id = number_to_id(ward_no)
    councillor = tmp[1]
    desc = "".join(tmp[2::]).replace("\n", "")

    item = {
        'id': ward_id,
        'ward_no': ward_no,
        'councillor': councillor,
        'description': desc
    }
    item["html"] = "<strong>Ward No. " + str(ward_no) + "</strong>"

    f2.write('\t' + simplejson.dumps(item))
    # {"id": "' + str(ward_id) + '", "councillor": "' + councillor + '", "description": "' + desc + '", "html": "Ward": "' + str(ward_id) + '"}')

    # add comma
    if i != len(lines) - 1:
        f2.write(",")

    # add linebreak
    f2.write("\n")
f2.write("]\n")

f.close()
f2.close()

