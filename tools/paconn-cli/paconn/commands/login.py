# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Login command.
"""

from paconn.authentication.auth import get_authentication
from paconn.common.util import display
from paconn.settings.settingsbuilder import SettingsBuilder
from paconn.settings.clouds import apply_cloud_config, validate_cloud_settings


def login(cloud, client_id, tenant, authority_url, resource, settings_file, force):
    """
    Login command.
    """
    # Validate cloud settings before proceeding
    validate_cloud_settings(cloud, client_id, tenant)

    # Get settings
    settings = SettingsBuilder.get_authentication_settings(
        settings_file=settings_file,
        client_id=client_id,
        tenant=tenant,
        authority_url=authority_url,
        resource=resource)

    # Apply cloud configuration
    apply_cloud_config(settings, cloud)

    get_authentication(
        settings=settings,
        force_authenticate=force)
    display('Login successful.')
