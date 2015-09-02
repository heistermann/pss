# -*- coding: utf-8 -*-
"""
Created on Tue Sep 01 11:11:42 2015

@author: heistermann
"""

import wradlib
import numpy as np



def georef_radolan(trgproj):
    """Get reprojected RADOLAN grid coordinates
    """
    # Get coordinates
    grid_xy_radolan = wradlib.georef.get_radolan_grid(900, 900)
    
    # create radolan projection osr object
    proj_stereo = wradlib.georef.create_osr("dwd-radolan")

    # transform radolan polar stereographic projection to target proj
    xy = wradlib.georef.reproject(grid_xy_radolan,
                                  projection_source=proj_stereo,
                                  projection_target=trgproj)
    
    return xy[:, :, 0], xy[:, :, 1]

def get_shp_coords(fpath, trgproj=None):
    """Get shapefile coordinates for overlay
    """
    # Open shapefile
    dataset, layer = wradlib.io.open_shape(fpath)
    # Get coordinates reprojected to target coordinate system
    if trgproj==None:
        lines, keys = wradlib.georef.get_shape_coordinates(layer)
    else:
        lines, keys = wradlib.georef.get_shape_coordinates(layer, dest_srs=trgproj)
    
    return lines, keys


def read_trmm(f):
    """Read TRMM data that comes on NetCDF.
    
    Parameters
    ----------
    f : string (TRMM file path)
    
    Returns
    -------
    out : X, Y, R
        Two dimensional arrays of longitudes, latitudes, and rainfall
        
    """
    data = wradlib.io.read_generic_netcdf(f)
    
    x = data["variables"]["longitude"]["data"]
    y = data["variables"]["latitude"]["data"]
    X, Y = np.meshgrid(x,y)
    X = X - 180.
    R = data["variables"]["r"]["data"][0]
    R = np.roll(R,720,axis=1)
    
    return X, Y, R