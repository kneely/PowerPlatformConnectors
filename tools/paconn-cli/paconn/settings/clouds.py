# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Cloud configuration for different Power Platform environments.
Supports Commercial, GCC, GCC-High, and DoD clouds.
"""

from knack.util import CLIError


# Cloud configuration keys
AUTHORITY_URL = 'authority_url'
POWERAPPS_URL = 'powerapps_url'
FLOW_URL = 'flow_url'
RESOURCE = 'resource'
CLIENT_ID = 'client_id'

# Default client ID (Azure CLI) - only works for Commercial cloud
AZURE_CLI_CLIENT_ID = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

# Cloud configurations
CLOUD_CONFIGS = {
    'commercial': {
        AUTHORITY_URL: 'https://login.microsoftonline.com/',
        POWERAPPS_URL: 'https://api.powerapps.com',
        FLOW_URL: 'https://api.flow.microsoft.com',
        RESOURCE: 'https://service.powerapps.com/',
        CLIENT_ID: AZURE_CLI_CLIENT_ID
    },
    'gcc': {
        AUTHORITY_URL: 'https://login.microsoftonline.com/',
        POWERAPPS_URL: 'https://gov.api.powerapps.us',
        FLOW_URL: 'https://gov.api.flow.microsoft.us',
        RESOURCE: 'https://gov.service.powerapps.us/',
        CLIENT_ID: None  # Requires custom app registration
    },
    'gcchigh': {
        AUTHORITY_URL: 'https://login.microsoftonline.us/',
        POWERAPPS_URL: 'https://high.api.powerapps.us',
        FLOW_URL: 'https://high.api.flow.microsoft.us',
        RESOURCE: 'https://high.service.powerapps.us/',
        CLIENT_ID: None  # Requires custom app registration
    },
    'dod': {
        AUTHORITY_URL: 'https://login.microsoftonline.us/',
        POWERAPPS_URL: 'https://api.apps.appsplatform.us',
        FLOW_URL: 'https://api.flow.appsplatform.us',
        RESOURCE: 'https://service.apps.appsplatform.us/',
        CLIENT_ID: None  # Requires custom app registration
    },
    'china': {
        AUTHORITY_URL: 'https://login.chinacloudapi.cn/',
        POWERAPPS_URL: 'https://api.powerapps.cn',
        FLOW_URL: 'https://api.flow.microsoft.cn',
        RESOURCE: 'https://service.powerapps.cn/',
        CLIENT_ID: None  # Requires custom app registration
    }
}

# Cloud name aliases for user convenience
CLOUD_ALIASES = {
    'public': 'commercial',
    'usgovernment': 'gcc',
    'usgov': 'gcc',
    'usgovhigh': 'gcchigh',
    'gcc-high': 'gcchigh',
    'usdod': 'dod',
    'usgov-dod': 'dod',
    'mooncake': 'china',
    '21vianet': 'china'
}


def get_cloud_config(cloud_name):
    """
    Get the cloud configuration for a given cloud name.

    Args:
        cloud_name: The name of the cloud (e.g., 'commercial', 'gcc', 'gcchigh', 'dod', 'china')

    Returns:
        dict: The cloud configuration dictionary

    Raises:
        CLIError: If the cloud name is not recognized
    """
    if cloud_name is None:
        return CLOUD_CONFIGS['commercial']

    # Normalize the cloud name
    normalized = cloud_name.lower().strip()

    # Check for aliases
    if normalized in CLOUD_ALIASES:
        normalized = CLOUD_ALIASES[normalized]

    if normalized not in CLOUD_CONFIGS:
        valid_clouds = ', '.join(sorted(CLOUD_CONFIGS.keys()))
        raise CLIError(
            f"Unknown cloud '{cloud_name}'. Valid clouds are: {valid_clouds}. "
            f"Aliases are also supported: {', '.join(sorted(CLOUD_ALIASES.keys()))}"
        )

    return CLOUD_CONFIGS[normalized]


def get_cloud_names():
    """
    Get a list of valid cloud names.

    Returns:
        list: List of valid cloud names
    """
    return list(CLOUD_CONFIGS.keys())


def validate_cloud_settings(cloud_name, client_id, tenant):
    """
    Validate that required settings are provided for non-commercial clouds.

    Args:
        cloud_name: The name of the cloud
        client_id: The client ID provided by the user
        tenant: The tenant provided by the user

    Raises:
        CLIError: If required settings are missing for the cloud
    """
    if cloud_name is None or cloud_name.lower() == 'commercial':
        return

    config = get_cloud_config(cloud_name)

    # Check if client_id is required
    if config[CLIENT_ID] is None and not client_id:
        raise CLIError(
            f"The '{cloud_name}' cloud requires a custom app registration. "
            f"Please provide a client ID using --clid (-i) or in your settings file. "
            f"See README for instructions on creating an app registration."
        )

    # Government clouds require a specific tenant
    if cloud_name.lower() in ['gcc', 'gcchigh', 'dod', 'china']:
        if not tenant or tenant == 'common':
            raise CLIError(
                f"The '{cloud_name}' cloud requires a specific tenant ID. "
                f"Please provide your tenant ID using --tenant (-t) or in your settings file."
            )


def apply_cloud_config(settings, cloud_name):
    """
    Apply cloud configuration to settings, using cloud defaults where settings are not specified.

    Args:
        settings: The Settings object
        cloud_name: The name of the cloud

    Returns:
        Settings: The updated settings object
    """
    config = get_cloud_config(cloud_name)

    # Apply cloud defaults where settings are not explicitly set
    if settings.authority_url == 'https://login.microsoftonline.com/' or settings.authority_url is None:
        settings.authority_url = config[AUTHORITY_URL]

    if settings.powerapps_url == 'https://api.powerapps.com' or settings.powerapps_url is None:
        settings.powerapps_url = config[POWERAPPS_URL]

    if settings.flow_url == 'https://api.flow.microsoft.com' or settings.flow_url is None:
        settings.flow_url = config[FLOW_URL]

    if settings.resource == 'https://service.powerapps.com/' or settings.resource is None:
        settings.resource = config[RESOURCE]

    # Only apply client_id if not set and cloud has a default
    if (settings.client_id == AZURE_CLI_CLIENT_ID or settings.client_id is None) and config[CLIENT_ID]:
        settings.client_id = config[CLIENT_ID]

    return settings
