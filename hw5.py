import arcpy
import sys
###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Ethan Traugh", "etraugh"])

###################################################################### 
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population) 
# 
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems. 
# 
###################################################################### 
def calculateDensity(fcPolygon, attribute, geodatabases):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = geodatabases
    # If fc is not a polygon, throw an error and quit
    checkIfPolygonFeatureClass(fcPolygon)

    descFc = arcpy.Describe(fcPolygon)
    srefFc = descFc.spatialReference

    # Give warning if feature class has geographic coordinate system
    if srefFc.type == "Geographic": 
        print("Warning: Feature class - " + descFc.name + "has a geographic coordinate system." + 
        "Change fc coordinate system for more accurate area calculation")

    # Creates and calculates area field
    arcpy.management.AddField(fcPolygon,"area_sqmiles", "DOUBLE")
    arcpy.CalculateGeometryAttributes_management(fcPolygon, 
                                                [["area_sqmiles", "AREA_GEODESIC"]], 
                                                "MILES_US", 
                                                "SQUARE_MILES_US")

    # Creates and calculates density field                                           
    arcpy.management.AddField(fcPolygon,"density", "DOUBLE")
    with arcpy.da.UpdateCursor(fcPolygon, ["area_sqmiles", attribute, "density"]) as cursor:
        for row in cursor:
            if row[1] == 0:
                row[3] = 0
            else:
                row[2] = row[1]/row[0]
            cursor.updateRow(row)
###################################################################### 
# Problem 2 (40 Points)
# 
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase, 
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
# 
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#        
###################################################################### 
def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = geodatabase

    # Check if feature classes are correct type
    checkIfPolygonFeatureClass(fcClipPolygon)
    checkIfPolylineFeatureClass(fcLine)

    descClip = arcpy.Describe(fcClipPolygon)
    descLine = arcpy.Describe(fcLine)

    srefClip = descClip.spatialReference
    srefLine = descLine.spatialReference

    # If feature classes don't have same coordinate system, switch fcLine
    # coordinate system to that of fcClipPolygon
    if srefClip.PCSCode is not srefLine.PCSCode:
        arcpy.Project_management(fcLine, "Line", srefClip)
        print("Features do not have the same coordinate sytem."
        + " Features will be projected to" + srefClip.name)

    # Create a new layer only containing wanted object from fcClipPolygon
    query = polygonIDFieldName + " = " + "'" + clipPolygonID + "'"
    arcpy.Select_analysis(fcClipPolygon, "clip", query)
    # Clip line fc using the selected fc object 
    arcpy.Clip_analysis("Line", "clip", "clipped_line")
    
    # Sums the length of the lines and returns it
    arcpy.Statistics_analysis("clipped_line", "sum_line", [["Shape_Length", "SUM"]])
    with arcpy.da.SearchCursor("sum_line", "SUM_Shape_Length") as cursor:
        for row in cursor:
            print(row[0])
            return row[0]
######################################################################
# Problem 3 (30 points)
# 
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################
def countObservationsWithinDistance(fcPoint, distance, distanceUnit, geodatabase):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = geodatabase
    # Check if feature class is of type point
    checkIfPointFeatureClass(fcPoint) 

    # Add point count field
    arcpy.management.AddField(fcPoint, "Count", "LONG")

    # Create a new layer that counts amount of points within point buffers
    arcpy.analysis.SummarizeNearby(fcPoint, fcPoint, "fc_sum", distance_type = "straight_line", distances = distance, distance_units = distanceUnit)
    # Store point counts into dictionary
    count_dict = {}
    with arcpy.da.SearchCursor("fc_sum", ["Point_Count", "CITY_NAME"]) as cursor:
        for row in cursor:
            count_dict[row[1]] = row[0]
    # Join new layer point count with original layer using city name as join field
    with arcpy.da.UpdateCursor(fcPoint, ["Count", "CITY_NAME"]) as cursor:
        for row in cursor:
            row[0] = count_dict[row[1]]
            cursor.updateRow(row)

    
# Determines whether given feature class is a Point feature class
def checkIfPointFeatureClass(fcPoint):
    if arcpy.Describe(fcPoint).shapeType !=  "Point":
        print(fcPoint + " is not a Point feature class.")
        exit()
# Determines whether given feature class is a Polygon feature class
def checkIfPolygonFeatureClass(fcPolygon):
    if arcpy.Describe(fcPolygon).shapeType !=  "Polygon":
        print(fcPolygon + " is not a Polygon feature class.")
        exit()
# Determines whether given feature class is a Polyline feature class
def checkIfPolylineFeatureClass(fcPolyline):
    if arcpy.Describe(fcPolyline).shapeType != "Polyline":
        print(fcPolyline + " is not a Polyline feature class.")

######################################################################
# TESTING TESTING TESTING
#fc = "states48_albers"
#field = "POPULATION"
#work = "C:/Users/Ethan/Documents/hw5.gdb/hw5.gdb"
#calculateDensity(fc, field, work)
#line = "north_america_rivers"
#estimateTotalLineLengthInPolygons(line, fc, "STATE_NAME", "Iowa", work)
#countObservationsWithinDistance("eu_cities", 60, "MILES", work)



######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')