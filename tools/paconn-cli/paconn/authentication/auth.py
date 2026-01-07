# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
Authentication methods
"""

from knack.util import CLIError

from paconn.authentication.profile import Profile
from paconn.authentication.tokenmanager import TokenManager


def get_authentication(settings, force_authenticate, cloud=None):
    """
    Logs the user in and saves the token in a file.
    """
    tokenmanager = TokenManager()
    credentials = tokenmanager.read()

    token_expired = TokenManager.is_expired(credentials)

    # Get new token
    if token_expired or force_authenticate:
        profile = Profile(
            client_id=settings.client_id,
            tenant=settings.tenant,
            resource=settings.resource,
            authority_url=settings.authority_url,
            cloud=cloud)

        credentials = profile.authenticate_device_code()

        tokenmanager.write(credentials)

        token_expired = TokenManager.is_expired(credentials)

    # Couldn't acquire valid token
    if token_expired:
        raise CLIError('Couldn\'t get authentication')


def remove_authentication():
    tokenmanager = TokenManager()
    tokenmanager.delete_token_file()


def get_cached_auth_settings():
    """
    Returns cached authentication settings from the token file.
    These settings are stored during login and can be used by other commands.

    Returns:
        dict: Dictionary containing cached auth settings (cloud, client_id, tenant,
              authority_url, resource) or empty dict if no cached settings exist.
    """
    tokenmanager = TokenManager()
    credentials = tokenmanager.read()

    if not credentials or TokenManager.is_expired(credentials):
        return {}

    return {
        'cloud': credentials.get('cloud'),
        'client_id': credentials.get('client_id'),
        'tenant': credentials.get('tenant'),
        'authority_url': credentials.get('authority_url'),
        'resource': credentials.get('resource')
    }
