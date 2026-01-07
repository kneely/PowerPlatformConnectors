# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
User profile management class using MSAL (Microsoft Authentication Library).
"""
import msal
import time
from urllib.parse import urljoin


class Profile:
    """
    A Class representing user profile.
    Uses MSAL for authentication with support for national clouds.
    """

    def __init__(self, client_id, tenant, resource, authority_url, cloud=None):
        self.client_id = client_id
        self.tenant = tenant
        self.resource = resource
        self.authority_url = authority_url
        self.cloud = cloud

    def _get_authority(self):
        """
        Construct the full authority URL.
        """
        return urljoin(self.authority_url, self.tenant)

    def _get_scopes(self):
        """
        Get the scopes for the resource.
        MSAL uses scopes instead of resource. The default scope is {resource}/.default
        """
        # Remove trailing slash if present for scope construction
        resource = self.resource.rstrip('/')
        return [f"{resource}/.default"]

    def _create_public_client_app(self):
        """
        Create a PublicClientApplication for device code flow.
        """
        return msal.PublicClientApplication(
            client_id=self.client_id,
            authority=self._get_authority()
        )

    def authenticate_device_code(self):
        """
        Authenticate the end-user using device auth.
        Returns a token dictionary compatible with the existing tokenmanager.
        """
        app = self._create_public_client_app()
        scopes = self._get_scopes()

        # Initiate device code flow
        flow = app.initiate_device_flow(scopes=scopes)

        if 'user_code' not in flow:
            raise ValueError(
                f"Failed to initiate device flow: {flow.get('error_description', 'Unknown error')}"
            )

        # Display the message to user
        print(flow['message'])

        # Wait for user to authenticate
        result = app.acquire_token_by_device_flow(flow)

        if 'access_token' not in result:
            error_desc = result.get('error_description', result.get('error', 'Unknown error'))
            raise ValueError(f"Authentication failed: {error_desc}")

        # Convert MSAL token format to the format expected by tokenmanager
        # MSAL returns expires_in (seconds from now), we need expires_on (timestamp)
        expires_in = result.get('expires_in', 3600)
        expires_on = time.time() + expires_in

        credentials = {
            'token_type': result.get('token_type', 'Bearer'),
            'access_token': result['access_token'],
            'expires_on': expires_on,
            'refresh_token': result.get('refresh_token'),
            'id_token': result.get('id_token'),
            'client_id': self.client_id,
            'resource': self.resource,
            'authority_url': self.authority_url,
            'tenant': self.tenant,
            'cloud': self.cloud
        }

        # Extract oid from id_token_claims if available
        if 'id_token_claims' in result:
            credentials['oid'] = result['id_token_claims'].get('oid')

        return credentials
