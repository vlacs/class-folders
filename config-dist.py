#######################################################################
# GOOGLE config

# What is the email address of an administrative user in your Google apps domain?
google_apps_username = 'username@yourdomain.com'

# What is the password of the google_admin_email user in google?
google_apps_password = 'secret. safe.'

# What is the name of your Google Apps domain?
google_apps_domain = 'yourdomain.com'

google_apps_debug=True
#######################################################################

## What is the name or IP address of your LDAP server?
db_host = 'db-server'

# What is the name your database?
db_name = 'db-name'

# We need a name to conect to the DB server. Which one can we use?
db_username = 'db-username'

# What is the password for the above username?
db_pw = 'also secret. safe, too.'

shared_folder_format = '{{master_course_name}}-{{master_course_version}} {{student_lastname}}, {{student_firstname}} ({{teacher_lastname}}, {{teacher_firstname}})'
classroom_folder_format = '{{master_course_name}}-{{master_course_version}} ({{teacher_lastname}}, {{teacher_firstname}})'

# TODO: make this comment helpful... You must select all the keys you wish to use in the above format strings.
fetching_sql = """
SELECT enrolment_idstr, master_course_name, master_course_version,
student_lastname, student_firstname, teacher_lastname, teacher_firstname,
whenchanged
FROM some_table
"""

# Persistent storage
# Where do we keep persistent data needed by class-folders.py?
updatehistory_file = '/tmp/updatehistory.shelf'

