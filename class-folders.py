#!/usr/bin/env python

import bsddb
import getopt
import os
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import re
import shelve
import sys
import urllib
import gdata.apps.service
import gdata.apps.organization.client
import gdata.apps.groups.client
import gdata.docs.client
import gdata.docs.data
import gdata.acl.data
import config

app_name = 'class-folders'

def usage():
    print """
class-folders.py

    -h, --help
        Print this message.

    -u, --forceupdate=enrolment_idstr
        Force the folder for the specified enrolment_idstr to be updated next time this script runs.
    """

def process_argv():
    # process options
    argv = sys.argv
    opts, args = getopt.getopt(argv[1:], "hu:", ["help", "forceupdate=", ])
    for option, arg in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-u", "--forceupdate"):
            try :
                update_history = shelve.open(config.updatehistory_file)
                update_history.__delitem__(arg)
                update_history.close()
                print "enrolment_idstr '%s' set for update next run" % arg
            except bsddb._bsddb.DBNotFoundError :
                print "enrolment_idstr '%s' not found in update history (already set to update)" % arg
            sys.exit()

def create_client():
    client = gdata.docs.client.DocsClient(source=app_name)

    #Toggle HTTP Debugging based on config
    client.http_client.debug = config.google_apps_debug

    #Attempt to login with supplied information, catch and notify on failure
    try:
        client.ClientLogin(email=config.google_apps_username, password=config.google_apps_password, source=app_name)
    except gdata.client.BadAuthentication:
        exit('Invalid user credentials given.')
    except gdata.client.Error:
        exit('Login Error')

    return client

def create_folder(name):
    folder = gdata.docs.data.Resource(type='folder', title=title)

    if parent != None:
        parent = client.GetResourceById(parent)

    #Use the Client Object to create the folder in the root of their Drive or the collection specified.
    folder = client.CreateResource(folder, collection=parent)

def db_execute(dbconn, q, *args) :
    cur = dbconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(q, *args)
    return cur

def format_prepper(format):
    return format.replace('{{', '').replace('}}', '')

def name_munger(format, data):
    format_keys = [
            'master_course_name',
            'master_course_version',
            'student_firstname',
            'student_lastname',
            'teacher_firstname',
            'teacher_lastname'
            ]
    for k in format_keys:
        format = format.replace(k, data[k])
    return format

# what we do next: https://docs.google.com/a/vlacs.org/document/d/1DJdalGh_QCYRIg0RItUuvFyqhhZlJvyj3j75gJBvJQM/edit

def main():
    process_argv()

    dbconn = psycopg2.connect(host = config.db_host, database = config.db_name, user = config.db_username, password = config.db_pw)
    res = db_execute(dbconn, config.fetching_sql)

    google_client = create_client()
    
    update_history = shelve.open(config.updatehistory_file)
    for row in res:
        if row['enrolment_idstr'] not in update_history:
            enrolment_folder_name = name_munger(format_prepper(config.shared_folder_format), row)
            classroom_folder_name = name_munger(format_prepper(config.classroom_folder_format), row)
            print "Would make these folders: ", row['enrolment_idstr'], enrolment_folder_name, classroom_folder_name
            update_history[row['enrolment_idstr']] = {'enrolment_folder_name': enrolment_folder_name, 'classroom_folder_name': classroom_folder_name, 'whenchanged': row['whenchanged']}
    
    update_history.close()
    
if __name__ == "__main__":
    sys.exit(main())
