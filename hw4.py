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
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 

#the new distance field "STR_DIST"will be in the linear unit of the input features
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = input_geodatabase

    #Checks if correct feature type is given
    checkIfPointFeatureClass(fcPoint)
    checkIfPolylineFeatureClass(fcPolyline)

    #Near_analysis appends the distances from each point to the line in the point feature class
    try:
        arcpy.Near_analysis(fcPoint, fcPolyline)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])

    try:
        #this deletes the unwanted fields that are also created from the near_analysis
        arcpy.DeleteField_management(fcPoint, ["NEAR_FID", "NEAR_FC"])
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])
    

######################################################################
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon, join):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = input_geodatabase

    # Checks if feature layers are correct type
    checkIfPointFeatureClass(fcPoint)
    checkIfPolygonFeatureClass(fcPolygon)

    # Adds new field to polygon layer. This field will be an integer and will store the amount of
    # Points with the specefied attribute values that are inside of each polygon.
    try:
        newField = pointFieldValue.upper().replace(" - ", "_").replace(" ", "_") + "_COUNT"  
        arcpy.management.AddField(fcPolygon, newField, "LONG")
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])                            
    
    # Creates temporary layer containing only points that have wanted attribute values
    try:
        query = pointFieldName + " = " + "'" + pointFieldValue + "'"
        arcpy.management.MakeFeatureLayer(fcPoint, "selected", query, input_geodatabase)
        arcpy.SummarizeWithin_analysis(fcPolygon, "selected", "result", "ONLY_INTERSECTING")
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])
    
    # Creates a dictionary where the amount of points in the polygon is mapped to the join value
    try:
        objectPoints = {}
        with arcpy.da.SearchCursor("result", [join, "POINT_COUNT"]) as cursor:
            for row in cursor:
                objectPoints[row[0]] = row[1]
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])
    
    # Populating new point count field of input fc with the point count calculated by SummarizeWithin
    with arcpy.da.UpdateCursor(fcPolygon, [join, newField]) as cursor:
        for row in cursor:
            if row[0] in objectPoints.keys():
                row[1] = objectPoints[row[0]]
            else:
                row[1] = 0
            cursor.updateRow(row)
######################################################################
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace, join):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = workspace

    # Checks if given feature layers are correct type
    checkIfPointFeatureClass(fcPoint)
    checkIfPolygonFeatureClass(fcPolygon)
    # Creates a list "typeOfPoints" that contains all possible values in the pointFieldName attribute
    try:
        typeOfPoints = []
        with arcpy.da.SearchCursor(fcPoint, [pointFieldName]) as cursor:
            for row in cursor:
                if row[0] not in typeOfPoints:
                    typeOfPoints.append(row[0])
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])
    
    
    # counts the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) 
    # within each polygon and append the counts to a new field into the polygon feature class
    
    try:
        for type in typeOfPoints:
            countPointsByTypeWithinPolygon(workspace, fcPoint, pointFieldName, type, fcPolygon, join)
            print(str(type) + " count appended")
        print("Complete")
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])
##########################################################################################################

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
# Testing
#env = "C:/Users/Ethan/Documents/ArcGIS/Projects/HW4/hw3.gdb"
#blocks = "block_groups"
#routes = "bike_routes"
#facility = "facilities"
#hospital = "hospitals"


#calculateDistanceFromPointsToPolylines(env, hospital, routes)
#countCategoricalPointTypesWithinPolygons(facility, "FACILITY", blocks, env, "FIPS")
######################################################################

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')


