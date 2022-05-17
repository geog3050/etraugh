#Author- Ethan Traugh
#March 11 2022
#Quiz4

import arcpy
import sys

try:
    #set workspace
    arcpy.env.workspace = "C:/Users/Ethan/Documents/ArcGIS/Projects/Quiz4"  
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])

#feature class we want to edit
fc = "airports.shp"
#fields of fc that we want to read and write to
fields = ["FEATURE", "BUFFER"]


try:
    #create field "BUFFER" initialized with 0
    arcpy.AddField_management(fc, fields[1], "SHORT", "", "", "", "", "", "")
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])

try:
    #use update cursor to create an iterable list of the attribute rows
    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            #if FEATURE is Seaplane Base, set BUFFER to 7500
            if row[0] == "Seaplane Base":
                row[1] = 7500
            #if FEATURE is Airport, set BUFFER to 1500
            if row[0] == "Airport":
                row[1] = 1500
            #update the table
            cursor.updateRow(row)
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])

try:
    #create buffer shapefile using the BUFFER field as distance
    arcpy.Buffer_analysis(fc, 'buffer_airports', 'BUFFER')
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])








