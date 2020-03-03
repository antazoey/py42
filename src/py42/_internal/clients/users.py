import json

from py42._internal.base_classes import BaseAuthorityClient
from py42._internal.clients.util import get_all_pages
import py42.settings as settings


class UserClient(BaseAuthorityClient):
    def create_user(
        self,
        org_uid,
        username,
        email=None,
        password=None,
        first_name=None,
        last_name=None,
        notes=None,
    ):
        uri = u"/api/User"
        data = {
            u"orgUid": org_uid,
            u"username": username,
            u"email": email,
            u"password": password,
            u"firstName": first_name,
            u"lastName": last_name,
            u"notes": notes,
        }
        return self._default_session.post(uri, data=json.dumps(data))

    def get_by_id(self, user_id, **kwargs):
        uri = u"/api/User/{0}".format(user_id)
        params = kwargs
        return self._default_session.get(uri, params=params)

    def get_by_uid(self, user_uid, **kwargs):
        uri = u"/api/User/{0}".format(user_uid)
        params = dict(idType=u"uid", **kwargs)
        return self._default_session.get(uri, params=params)

    def get_by_username(self, username, **kwargs):
        uri = u"/api/User"
        params = dict(username=username, **kwargs)
        return self._default_session.get(uri, params=params)

    def get_current(self, **kwargs):
        uri = u"/api/User/my"
        params = kwargs
        return self._default_session.get(uri, params=params)

    def _get_page(
        self,
        active=None,
        email=None,
        org_uid=None,
        role_id=None,
        page_num=None,
        page_size=None,
        q=None,
        **kwargs
    ):
        uri = u"/api/User"
        params = dict(
            active=active,
            email=email,
            orgUid=org_uid,
            roleId=role_id,
            pgNum=page_num,
            pgSize=page_size,
            q=q,
            **kwargs
        )

        return self._default_session.get(uri, params=params)

    def get_all(self, active=None, email=None, org_uid=None, role_id=None, q=None, **kwargs):
        return get_all_pages(
            self._get_page,
            settings.items_per_page,
            u"users",
            active=active,
            email=email,
            org_uid=org_uid,
            role_id=role_id,
            q=q,
            **kwargs
        )

    def block(self, user_id):
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._default_session.put(uri)

    def unblock(self, user_id):
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._default_session.delete(uri)

    def deactivate(self, user_id, block_user=None):
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        data = {u"blockUser": block_user}
        return self._default_session.put(uri, data=json.dumps(data))

    def reactivate(self, user_id, unblock_user=None):
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        params = {u"unblockUser": unblock_user}
        return self._default_session.delete(uri, params=params)

    def change_org_assignment(self, user_id, org_id):
        uri = u"/api/UserMoveProcess"
        data = {u"userId": user_id, u"parentOrgId": org_id}
        return self._default_session.post(uri, data=json.dumps(data))
