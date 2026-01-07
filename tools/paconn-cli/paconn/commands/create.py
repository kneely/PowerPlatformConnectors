# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
Create command.
"""

from paconn import _CREATE
from paconn.common.util import display
from paconn.settings.util import load_powerapps_and_flow_rp
from paconn.operations.upsert import upsert
from paconn.settings.settingsbuilder import SettingsBuilder
from paconn.settings.clouds import apply_cloud_config


# pylint: disable=too-many-arguments
def create(
        cloud,
        environment,
        api_properties,
        api_definition,
        icon,
        script,
        powerapps_url,
        powerapps_version,
        client_secret,
        settings_file,
        overwrite_settings):
    """
    Create command.
    """
    # Get settings
    settings = SettingsBuilder.get_settings(
        environment=environment,
        settings_file=settings_file,
        api_properties=api_properties,
        api_definition=api_definition,
        icon=icon,
        script=script,
        connector_id=None,
        powerapps_url=powerapps_url,
        powerapps_version=powerapps_version)

    # Apply cloud configuration (CLI argument takes precedence over settings file)
    effective_cloud = cloud or settings.cloud
    apply_cloud_config(settings, effective_cloud)

    powerapps_rp, _ = load_powerapps_and_flow_rp(
        settings=settings,
        command_context=_CREATE)

    connector_id = upsert(
        powerapps_rp=powerapps_rp,
        settings=settings,
        client_secret=client_secret,
        is_update=False,
        overwrite_settings=overwrite_settings)

    display('{} created successfully.'.format(connector_id))
