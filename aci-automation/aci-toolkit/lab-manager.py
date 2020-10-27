# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode
import acitoolkit.acitoolkit as aci
import csv
import os

def import_csv(csvfilename):
    """
    Import file 'csvfilename' and return its content as a list.
    
    Arguments:
        csvfilename {str} -- path of the file to be imported.
    Returns:
        [list] -- List with data read from 'csvfilename'.
    """

    data = []
    
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=';')
        for row in reader:
            if row:  # avoid blank lines
                data.append(row)
    
    return data

def validate_partecipants(course_partecipants):
    
    if course_partecipants < 1:
        raise Exception(' !!! The number of course partecipants should be a positive integer! Input value: {} '.format(course_partecipants))

def validate_lab(lab):

    if lab < 1 and lab > 8:
        raise Exception(' !!! Could not restore to the selected lab! lab IDs are included between 1 and 8. Input value: {} '.format(lab))


def main():

    #################### CONFIGURATION MENU #################################################################
    print("\n ********* Welcome to the LAB-MANAGER configurator! ********* ")
    print(" Please provide the following information to set up the labs on the Cisco APIC Sandbox. ")
    #
    course_partecipants = int(input(' COURSE PARTECIPANTS NUMBER: '))
    validate_partecipants(course_partecipants)
    lab = int(input(' RESTORE TO LAB #: '))
    validate_lab(lab)
    #
    #################### GET CREDENTIALS & APIC LOGIN #######################################################
    #
    ## Credentials
    #
    description = 'ACI Fabric Setup'
    creds = aci.Credentials('apic', description)
    creds.add_argument('--delete', action='store_true',
                    help='Delete the configuration from the APIC')
    args = creds.get()
    #
    ## Login to the APIC
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')

    #################### CREATE & PUSH ACI FABRIC (TENANT, VRF, BD, EPG) ####################################
    #
    ## Create ACI Fabric (Tenant, VRF, BD and EPG)
    #
    # TODO: implement logic to restore labs
    #
    ## Push
    resp = session.push_to_apic(tenant.get_url(),
                                tenant.get_json())
    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)

if __name__ == "__main__":
    main()