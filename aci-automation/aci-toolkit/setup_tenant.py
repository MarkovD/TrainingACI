# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode
import acitoolkit.acitoolkit as aci

def main():

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
    ## TENANT, VRF & Bridge Domains
    #
    tenant = aci.Tenant("MMTENANT0")
    tenant.descr = "Created using ACITOOLKIT"

    vrf = aci.Context("VRF-INSIDE", tenant)

    bd1 = aci.BridgeDomain("BD100", tenant)
    bd1.add_context(vrf)
    bd2 = aci.BridgeDomain("BD200", tenant)
    bd2.add_context(vrf)
    #
    ## Application Profile & EPGs
    #
    app_profile = aci.AppProfile("AP0", tenant)

    epg1 = aci.EPG("EPG100", app_profile)
    epg1.add_bd(bd1)

    epg2 = aci.EPG("EPG200", app_profile)
    epg2.add_bd(bd2)
    #
    ## Contract
    #
    # Define a contract with a single entry
    contract = aci.Contract("permit-icmp", tenant)
    entry1 = aci.FilterEntry("icmp", 
                            parent=contract,
                            applyToFrag='no',
                            etherT='ip',
                            prot='icmp')
    
    # Apply contract in both directions
    
    # apply from epg1 to epg2
    epg1.provide(contract)
    epg2.consume(contract)

    # apply from epg2 to epg1
    epg1.consume(contract)
    epg2.provide(contract)
    #
    ## Push to APIC
    #
    resp = session.push_to_apic(tenant.get_url(),
                                    tenant.get_json())
    if not resp.ok:
        print('%% Error: Could not push {} configuration to APIC'.format(tenant.name))
        print(resp.text)
    #
    #########################################################################################################
    #
    print(" *** SCRIPT EXECUTED SUCCESSFULLY! *** ")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass