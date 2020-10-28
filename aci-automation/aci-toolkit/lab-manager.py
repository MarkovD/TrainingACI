# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode
import acitoolkit.acitoolkit as aci

def validate_partecipants(course_partecipants):
    
    if course_partecipants < 1:
        raise Exception(' !!! The number of course partecipants should be a positive integer! Input value: {} '.format(course_partecipants))

def validate_lab(lab_id):

    if lab_id < 1 and lab_id > 4:
        raise Exception(' !!! Could not restore to the selected lab! lab IDs are included between 1 and 4. Input value: {} '.format(lab_id))

def get_bd(bd_name, tenant):

    for t_child in tenant._children:
        if type(t_child) == aci.BridgeDomain and t_child.name == bd_name:
            return t_child

def get_epg(epg_name, tenant, ap_name):

    for t_child in tenant._children:
        if type(t_child) == aci.AppProfile and t_child.name == ap_name:
            for ap_child in t_child._children:
                if type(ap_child) == aci.EPG and ap_child.name == epg_name:
                    return ap_child

def main():

    #################### CONFIGURATION MENU #################################################################
    print("\n ********* Welcome to the LAB-MANAGER configurator! ********* ")
    print(" Please provide the following information to set up the labs on the Cisco APIC Sandbox. ")
    #
    course_partecipants = int(input(' COURSE PARTECIPANTS NUMBER: '))
    validate_partecipants(course_partecipants)
    lab_id = int(input(' RESTORE TO LAB #: '))
    validate_lab(lab_id)
    #
    #################### DEFINE LAB LIST ####################################################################
    #
    lab = [lab1, lab2, lab3, lab4]
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
    #
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
    #
    #################### CREATE & PUSH ACI CONFIG ###########################################################
    #
    ## Define ACI config per lab
    #
    tenant_list = []
    for l in range(lab_id):
        tenant_list = lab[l](course_partecipants, tenant_list)
    #
    ## Push to APIC
    #
    for cp in range(course_partecipants):
        tenant = tenant_list[cp]
        resp = session.push_to_apic(tenant.get_url(),
                                    tenant.get_json())
        if not resp.ok:
            print('%% Error: Could not push {} configuration to APIC'.format(tenant.name))
            print(resp.text)

    print("\n ********* LABS RESTORED! ********* \n")

def lab1(course_partecipants, tenant_list = []):
    
    new_tenant_list = tenant_list
    
    return new_tenant_list

def lab2(course_partecipants, tenant_list = []):

    new_tenant_list = []
    for cp in range(1, course_partecipants+1):
        
        tenant = aci.Tenant("MMTENANT{}".format(cp))

        vrf = aci.Context("VRF-INSIDE", tenant)

        bd1 = aci.BridgeDomain("BD100", tenant)
        bd1.add_context(vrf)
        bd2 = aci.BridgeDomain("BD200", tenant)
        bd2.add_context(vrf)
        
        new_tenant_list.append(tenant)

    return new_tenant_list

def lab3(course_partecipants, tenant_list):
    
    new_tenant_list = []
    for cp in range(1, course_partecipants+1):
        
        tenant = tenant_list[cp-1]

        app_profile = aci.AppProfile("AP{}".format(cp), tenant)

        epg1 = aci.EPG("EPG100", app_profile)
        bd1 = get_bd("BD100", tenant)
        epg1.add_bd(bd1)

        epg2 = aci.EPG("EPG200", app_profile)
        bd2 = get_bd("BD200", tenant)
        epg2.add_bd(bd2)
        
        new_tenant_list.append(tenant)

    return new_tenant_list

def lab4(course_partecipants, tenant_list = []):
    
    new_tenant_list = []
    for cp in range(1, course_partecipants+1):
        
        tenant = tenant_list[cp-1]

        # Define a contract with a single entry
        contract = aci.Contract("permit-icmp", tenant)
        entry1 = aci.FilterEntry("icmp", 
                                parent=contract,
                                applyToFrag='no',
                                etherT='ip',
                                prot='icmp')
        
        # Apply contract in both directions
        
        ## Get EPGs 
        epg1 = get_epg("EPG100",tenant, "AP{}".format(cp))
        epg2 = get_epg("EPG200",tenant, "AP{}".format(cp))

        ## apply from epg1 to epg2
        epg1.provide(contract)
        epg2.consume(contract)

        ## apply from epg2 to epg1
        epg1.consume(contract)
        epg2.provide(contract)

        new_tenant_list.append(tenant)

    return new_tenant_list


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass