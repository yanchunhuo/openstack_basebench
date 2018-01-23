#!-*- coding:utf8 -*-

def getDefaultSecGroupId(secGroups,secGroup_name):
    for secGroup in secGroups:
        if secGroup.name==secGroup_name:
            return secGroup.id

def getAdminFloatNetId(adminNets,adminNet_name):
    for adminNet in adminNets:
        if adminNet.name==adminNet_name:
            return adminNet.id

def getTestImageId(images,image_name):
    for image in images:
        if image.name==image_name:
            return image.id

def getFlavorId(flavors,flavor_type):
    for flavor in flavors:
        if flavor.type==flavor_type:
            return flavor.id


def getNetId(nets,net_name):
    for net in nets:
        if net.name==net_name:
            return net.id

def getVolumeTypeId(volumeTypes,volumeType_type):
    for volumeType in volumeTypes:
        if volumeType.type==volumeType_type:
            return volumeType.id


def getFlavorName(flavors,flavor_type):
    for flavor in flavors:
        if flavor.type==flavor_type:
            return flavor.name

