# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Download command.
"""

from paconn import _DOWNLOAD

from paconn.common.util import display
from paconn.settings.util import load_powerapps_and_flow_rp
from paconn.settings.settingsbuilder import SettingsBuilder
from paconn.settings.clouds import apply_cloud_config
from paconn.authentication.auth import get_cached_auth_settings

import paconn.operations.download


# pylint: disable=too-many-arguments
def download(
        cloud,
        environment,
        connector_id,
        destination,
        powerapps_url,
        powerapps_version,
        settings_file,
        overwrite):
    """
    Download command.
    """
    # Get cached auth settings from login
    cached_settings = get_cached_auth_settings()

    # Get settings
    settings = SettingsBuilder.get_settings(
        environment=environment,
        settings_file=settings_file,
        api_properties=None,
        api_definition=None,
        icon=None,
        script=None,
        connector_id=connector_id,
        powerapps_url=powerapps_url,
        powerapps_version=powerapps_version)

    # Apply cloud configuration (CLI argument > settings file > cached login)
    effective_cloud = cloud or settings.cloud or cached_settings.get('cloud')
    apply_cloud_config(settings, effective_cloud)

    powerapps_rp, _ = load_powerapps_and_flow_rp(
        settings=settings,
        command_context=_DOWNLOAD)

    directory = paconn.operations.download.download(
        powerapps_rp=powerapps_rp,
        settings=settings,
        destination=destination,
        overwrite=overwrite)

    display('The connector is downloaded to {}.'.format(directory))
