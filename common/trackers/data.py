# -*- coding: utf-8 -*-

from common import config_settings


trackers_api_data = {
    'ITT':
        {
            "url": config_settings.tracker_config.ITT_URL,
            "api_key": config_settings.tracker_config.ITT_APIKEY,
            "pass_key": config_settings.tracker_config.ITT_PID,
            "announce": f"{config_settings.tracker_config.ITT_URL}/announce/{config_settings.tracker_config.ITT_PID}"
        }
    ,
    'SIS':
        {
            "url": config_settings.tracker_config.SIS_URL,
            "api_key": config_settings.tracker_config.SIS_APIKEY,
            "pass_key": config_settings.tracker_config.SIS_PID,
            "announce":  f"{config_settings.tracker_config.SIS_URL}/announce/{config_settings.tracker_config.SIS_PID}"
        }

}

