# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Validate command.
"""

from paconn import _VALIDATE

from paconn.common.util import display
from paconn.settings.util import load_powerapps_and_flow_rp
from paconn.settings.settingsbuilder import SettingsBuilder
from paconn.settings.clouds import apply_cloud_config

import paconn.operations.validate


def validate(
        cloud,
        api_definition,
        powerapps_url,
        powerapps_version,
        settings_file):
    """
    Validate command.
    """
    # Get settings
    settings = SettingsBuilder.get_settings(
        environment=None,
        settings_file=settings_file,
        api_properties=None,
        api_definition=api_definition,
        icon=None,
        script=None,
        connector_id=None,
        powerapps_url=powerapps_url,
        powerapps_version=powerapps_version)

    # Apply cloud configuration (CLI argument takes precedence over settings file)
    effective_cloud = cloud or settings.cloud
    apply_cloud_config(settings, effective_cloud)

    powerapps_rp, _ = load_powerapps_and_flow_rp(
        settings=settings,
        command_context=_VALIDATE)

    result = paconn.operations.validate.validate(
        powerapps_rp=powerapps_rp,
        settings=settings)

    if result:
        display(result)
    else:
        display('{} validated successfully.'.format(settings.api_definition))
