from trac.core import *
from trac.perm import IPermissionRequestor, IPermissionGroupProvider,IPermissionPolicy,PermissionSystem
from trac.wiki.model import WikiPage

try:
   set = set
except NameError:
   from sets import Set as set

__all__ = ['userpageconcealer']


class UserPageConcealer(Component):
    implements(IPermissionRequestor, IPermissionPolicy)
    
    group_providers = ExtensionPoint(IPermissionGroupProvider)

    def __init__(self):
        root = self.config.get('userpageconcealer', 'root')
        if root.startswith('/wiki/') :
            root = root.split('/wiki/',1).pop()
        self._userpagebase = root.split('/',1).pop(0)

    # IPermissionPolicy(Interface)
    def check_permission(self, action, username, resource, perm):
        if resource is None or resource.id is None:
            return None

        if resource.realm == 'wiki' and action in ('WIKI_VIEW','WIKI_MODIFY'):
            wiki = WikiPage(self.env, resource.id)
            return self.check_wiki_access(perm, resource, action, wiki.name, username)
        return None

    # IPermissionRequestor methods
    def get_permission_actions(self):
        return []

    def _prep_page(self, page):
        return page.upper().replace('/','_')

    def _protected_page(self, page):
        upagebase = self._prep_page(self._userpagebase)
        page = self._prep_page(page)
        self.env.log.debug('Now checking for %s with userpage_basepath = %s' % (page, upagebase))

        member_of = []
        if page.startswith(upagebase) or page == upagebase:
              member_of.append(upagebase)

        return member_of

    def _ownuser_page(self, page, username):
        self.env.log.debug('confirm page = %s is owned by %s' % (page, username))
        page = self._prep_page(page)
        upagebase = self._prep_page(self._userpagebase)

        userpage = page.split(upagebase + '_').pop()
        return ( userpage.startswith(username.upper()) )

    # Public methodsf
    def check_wiki_access(self, perm, res, action, page, username):
        """Return if this req is permitted access to the given ticket ID."""

        try:
            member_of = self._protected_page(page)
            if not member_of:
                self.env.log.debug('%s is not a private page' % page)
                return None
            for p in member_of:
                self.env.log.debug('Checking protected area: %s' % p)
                
                if self._ownuser_page(page, username):
                    return True

                # this plugin denied even if admin request access.
                # make this plugin disable if you(admin) need to view or edit userpage.

        except TracError:
            return None

        return False
