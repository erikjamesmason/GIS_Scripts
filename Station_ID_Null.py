############################################################################################
# Author: Erik Mason
# Date: January 28 2020
# Purpose: Update Traffic Station ID's to Original ID IF NULL
# Inputs: Hosted Feature Layer(Statewide_Traffic_Collector_Master) or comparable
# Outputs: UpdateCursor updates input Hosted Feature Layer

############################################################################################
#import necessary modules
import arcpy
from arcgis.gis import GIS
import os

# assign variables to different context for GIS
gis = GIS("Pro")
fc = gis.content.get("bad175efcff24d699e94be1e25f1b4f3")

# begin main function
def main():

    # set environment
    arcpy.env.workspace = r'C:\Users\ejmason\Documents\
        ArcGIS\Projects\
            Statewide Traffic Stations Project Update 2020\
                Default.gdb'

    # set folder path and "file" name # this seemed to work better with using Editor session
    folderPath = r"C:\Users\ejmason\Documents\ArcGIS\Projects\Statewide Traffic Stations Project Update 2020"
    envName = "Default.gdb"

    # establish an Editing Session
    edit = arcpy.da.Editor(os.path.join(folderPath, envName))
    edit.startEditing(False, True)
    edit.startOperation()

    # Establish table for script to target # for local or hosted
    ftable = r'https://services.arcgis.com/r4A0V7UzH9fcLVvv/arcgis/rest/services/Statewide_Traffic_Stations/FeatureServer/0'

    # if using something local, use this
    #
    # ftable = r'C:\Users\ejmason\Documents\ArcGIS\Projects\Statewide Traffic Stations Project Update 2020\Default.gdb\Statewide_Traffic_Collector_Master_CopyFeatures'
    #

    # fields for cursor to iterate through
    fields = ['Station_ID', 'Station_ID_Original']
    stationid = 'Station_ID'
    stationoriginal = 'Station_ID_Original'

    # Begin Update Cursor iteration with table and fields
    # this works by taking the values in fields (which is a list)
    # then identifying those as row, so the amount of values in your list,
    # which is the variable name "fields", will be the length of your array,
    # meaning you will get an error if there is one 1 value, and you reference row[1]
    # since array starts at 0.
    # if you have 30 values, your array will end at row[29]

    with arcpy.da.UpdateCursor(ftable, fields) as cursor:
        # signify start
        print("Starting Script on " + str(ftable))

        # counter for iteration marking # must add print(x) in loop if counting is desired
        x = 0

        # begin loop
        for row in cursor:

            #identify that StationID is null
            if row[0] is None:
                print("row " + str(x) + ": ")
                print(row[0])

                # this determines if there is a valid value instead of null in original ID
                if row[1] is None:
                    row[0] = row[0]
                    print("row " + str(row) + " is null")

                # this converts the value to a non-null value in stationID
                else:
                    row[0] = row[1]
                    print(row[1])
                    cursor.updateRow(row)
                    print(row)
            # this helps visualize the process of iteration
            else:
                print(row)
            # increment counter
            x += 1
        print("Script Complete")
    # seems that if you have a session open locally with targeted tables/environments, the
    # whole script will run, but not write with an error "Cannot acquire Lock"
    edit.stopOperation()
    edit.stopEditing(True)



if __name__ == '__main__':

    main()