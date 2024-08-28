Step 1: DEFINE CUSTOM PERMISSIONS

in the models.py, under Book model, I added the following permissions under class Meta
can_view, can_create, can_edit, and can_delete
Step 2: CREATE VIEWS 
The second step was to create views that made use of @permission_required as follows:
@permission_required('relationship_app.can_view', raise_exception=True)
@permission_required('relationship_app.can_create', raise_exception=True)
@permission_required('relationship_app.can_edit', raise_exception=True)
@permission_required('relationship_app.can_delete', raise_exception=True)
Step 3: Create Groups
I went to admin page and added groups as follows:
Editors
Viewers
Admins

Step 4: Adding Permissions to groups
I went on the admin site and then added specific permissions to different groups
Step 5: Assigning users to groups
I logged into admin site and then added users specifically to different groups.