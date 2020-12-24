from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):

   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)

def has_permission(self, perm, obj = None):
    try:
        user_perm = self.user_permissions.get(codename = perm)
    except ObjectDoesNotExist:
        user_perm = False
    if user_perm:
        return True
    else:
        return False

def permission_required(*perms):
    return user_passes_test(lambda u: any(u.has_perm(perm) for perm in perms), login_url = '/')

