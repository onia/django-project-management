import ldap
ldap.set_option(ldap.OPT_REFERRALS, 0)
from django.contrib.auth.models import User
from projects.models import ServiceAccount
import logging

# Constants
AUTH_LDAP_SERVER = 'Your LDAP Server'
AUTH_LDAP_BASE_USER = "cn=Your, o=BaseUser"
AUTH_LDAP_BASE_PASS = "Your Base Password"

class LDAPBackend:

        def __init__(self):

                self.base = ''
                self.AUTH_LDAP_SERVER = ''
                self.AUTH_LDAP_BASE_USER = ''
                self.AUTH_LDAP_BASE_PASS = ''


        def authenticate(self, username=None, password=None):
                scope = ldap.SCOPE_SUBTREE
                filter = "(&(objectclass=person) (samAccountName=%s))" % username
                ret = ['dn', 'mail', 'givenName', 'sn']

                ldap_user = False
                valid_ldap_user = False
        # Authenticate the base user so we can search
                # Locate the LDAP users in one of our directories so we can then
                # authenticate her
                for service_account in ServiceAccount.objects.filter(active=True):

                        base = service_account.base_dn
        
                        try:
                                l = ldap.open(service_account.ldap_servers)
                                l.protocol_version = ldap.VERSION3
                                l.simple_bind_s(service_account.bind_dn, service_account.bind_pw)
                        except ldap.LDAPError, e:
                                break

                        try:
                                result_id = l.search(base, scope, filter, ret)
                                result_type, result_data = l.result(result_id, 0)

                # If the user does not exist in LDAP, Fail.
                                if result_data[0][0]:
                                        ldap_user = result_data[0]
                                        break
                        except ldap.LDAPError, e:
                                print '''Error connecting to %s: %s''' % ( service_account.ldap_servers, e )

                if ldap_user:

                # Attempt to bind to the user's DN
                                try:
                                        l.simple_bind_s(ldap_user[0],password)
                                        valid_ldap_user = True
                                except ldap.INVALID_CREDENTIALS:
                                        valid_ldap_user = False
                                        pass
                                

                if valid_ldap_user:     


                # The user existed and authenticated. Get the user
                # record or create one with no privileges.
                                try:
                                        user = User.objects.get(username__exact=username)
                                except ldap.INVALID_CREDENTIALS:
                         # Name or password were bad. Fail.
                                        return None
                                except:
                        # Theoretical backdoor could be input right here. We don't
                        # want that, so input an unused random password here.
                        # The reason this is a backdoor is because we create a
                        # User object for LDAP users so we can get permissions,
                        # however we -don't- want them able to login without
                        # going through LDAP with this user. So we effectively
                        # disable their non-LDAP login ability by setting it to a
                        # random password that is not given to them. In this way,
                        # static users that don't go through ldap can still login
                        # properly, and LDAP users still have a User object.

                                        # Get the users first_name, last_name and email address, set some defaults if they
                                        # don't exists in AD
                                        email = result_data[0][1].get('mail', '''%s@change-me.com''' % username )
                                        first_name = result_data[0][1].get('givenName', ' ')
                                        last_name = result_data[0][1].get('sn', ' ')
                                        

                                        from random import choice
                                        import string
                                        temp_pass = ""
                                        for i in range(8):
                                                temp_pass = temp_pass + choice(string.letters)
                                        user = User.objects.create_user(username,
                                                email[0] ,temp_pass)
                                        user.is_staff = False
                                        user.first_name = first_name[0]
                                        user.last_name = last_name[0]
                                        user.save()
                                        
                    # Success.
                                return user
                   

                else:
                        return None

        def get_user(self, user_id):
                try:
                        return User.objects.get(pk=user_id)
                except User.DoesNotExist:
                        return None


