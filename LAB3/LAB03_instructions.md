# LAB03 - Application Profile (AP) and EndPoint Group (EPG)

## Table of Contents

- [LAB03 - Application Profile (AP) and EndPoint Group (EPG)](#lab03---application-profile-(ap)-and-endpoint-group-(epg))
  - [Introduction](#introduction)
  - [Configuration Procedure](#configuration-procedure)
    - [ACI Application Profile](#aci-application-profile)
    - [ACI EndPoint Groups](#aci-endpoint-groups)
  - [Conclusions](#conclusions)

## Introduction

In this lab you will configure the following objects on the Cisco APIC inside the tenant you created in the [previous lab](../LAB2/LAB02_instructions.md):
- 1x Application Profile
- 2x EndPoint Groups

As reference, the following image reports the relationships between these three objects as they are modelled in the ACI Management Information Tree (MIT):

![mit](images/mit.png)

To perform the configuration steps reported in the following section, please access to the Cisco APIC Sandbox @ [this link](https://sandboxapicdc.cisco.com/#) using the credential below:

- User ID: admin
- Password: ciscopsdt

> :warning: When you encounter "{*my_ID*}" in the configuration steps, remember to replace it with the ID you were given at the beginning of this course.
> 
> E.g. if you have ID = **10**, the string **MMTENANT{*my_ID*}** becomes **MMTENANT10**.

## Configuration Procedure

### ACI Application Profile

1. On the menu bar, click **Tenants**.
2. Look for your tenant (**MMTENANT{*my_ID*}**) and double-click on it.
3. Right-click on **Application Profiles** and select **Create Application Profile**.
4. In the _Create Application Profile_ dialog box...
   1. Fill the **Name** field with **AP{*my_ID*}**
   2. In the _EPGs_ section, click the "**+**" button.
   3. ******************TODO FROM HERE**
   4. Click the **Submit** button.

### ACI EndPoint Groups

## Conclusion

In this lab you created a tenant on the Cisco APIC and configured part of its "_networking side_", i.e. a VRF and a Bridge Domain. In the [next lab](../LAB4/LAB04_instructions.md) you will configure the "_application profile_" of your tenant.

> :heavy_check_mark: Congratulations! You have successfully completed this lab!
