import json
import csv
import os

def main():
    print_header()

    filename = input("Please enter json file name : ")
    aci_parsed = read_json_file(filename)

    if aci_parsed:
        write_json_to_csv(aci_parsed, filename)
    else:
        print("Json file doesn't exist!!!")

def read_json_file(filename):
    json_path = os.path.abspath(os.path.join('.', filename))

    if os.path.exists(json_path):
        open_file = open(json_path, 'r')
        aci_parsed = json.load(open_file)
        aci_data = aci_parsed['imdata']

        return aci_data

    else:
        return False

def write_json_to_csv(data, filename):
    fname = filename.split('.')[0]
    csv_path = os.path.abspath(os.path.join('.', os.path.basename(fname) + ".csv"))

    with open(csv_path, 'w', newline='\n', encoding='utf-8') as csv_data:
        csvwriter = csv.writer(csv_data)

        header = ['Tenant', 'Application', 'EPG', 'Contract']
        csvwriter.writerow(header)

        for i in data:
            for key, value in i['fvTenant']['attributes'].items():
                if key == 'name':
                    Tenant = value

            for j in i['fvTenant']['children']:
                if 'fvAp' in j:
                    for key, value in j['fvAp']['attributes'].items():
                        if key == 'name':
                            App = Tenant + "," + value

                    for k in j['fvAp']['children']:
                        if 'fvAEPg' in k:
                            for key, value in k['fvAEPg']['attributes'].items():
                                if key == 'name':
                                    EPG = App + "," + value

                            for l in k['fvAEPg']['children']:
                                if 'fvRsProv' in l:
                                    for key, value in l['fvRsProv']['attributes'].items():
                                        if key == 'tnVzBrCPName':
                                            Prov = EPG + "," + value
                                            mProv = Prov.split(',')
                                            csvwriter.writerow(mProv)

                                elif 'fvRsCons' in l:
                                    for key, value in l['fvRsCons']['attributes'].items():
                                        if key == 'tnVzBrCPName':
                                            Cons = EPG + "," + value
                                            mCons = Cons.split(',')
                                            csvwriter.writerow(mCons)

    csv_data.close()
    print("extract data succesfully !!!")

def print_header():
    print('-----------------------------------------------------')
    print('                     READ JSON')
    print('-----------------------------------------------------')
    print()

if __name__ == '__main__':
    main()