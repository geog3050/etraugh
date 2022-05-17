import sys
import arcpy
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
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
def printFeatureClassNames(workspace):
    try:
        #set workspace
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        feature_classes = arcpy.ListFeatureClasses()
        for fc in feature_classes:
            desc = arcpy.Describe(fc)
            print(desc.name + " is a " + desc.shapeType + " feature class")
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    try:
        #set workspace
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        fields = arcpy.ListFields(inputFc)
        for field in fields:
            if checkIfNumber(field.type):
                print("{0} is of type {1}"
                .format(field.name, field.type))
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):

    try:
        #Creates a list of all the feature classes with specified shapeType
        arcpy.env.workspace = input_geodatabase
        arcpy.env.overwriteOutput = True
        fc = arcpy.ListFeatureClasses(feature_type = shapeType)
        #creates a gdb one file back from the input_geodatabase location
        arcpy.CreateFileGDB_management(input_geodatabase[:input_geodatabase.rfind('/')], output_geodatabase)
        #inserts feature classes of type shapeType into the new gdb
        arcpy.FeatureClassToGeodatabase_conversion(fc, input_geodatabase[:input_geodatabase.rfind('/')]+ "/" + output_geodatabase)

    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])




###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):

    try:
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        #Join feature layer and table
        temp_layer = arcpy.AddJoin_management(inputFc, idFieldInputFc, inputTable, 
                                                idFieldTable, "KEEP_COMMON")
        # Copy the layer to a new permanent feature class
        arcpy.CopyFeatures_management(temp_layer, inputFc[:-4])
        
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddError(e.args[0])




def checkIfNumber(value):
    if value == "Float" or value == "Integer":
        return True
    else:
        return False

#printFeatureClassNames( "C:/Users/Ethan/Documents/GeospatialProgramming/HW3/hw3.gdb")

        ######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')