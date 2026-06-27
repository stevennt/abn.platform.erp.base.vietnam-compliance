import click
import erpnext
import frappe
from packaging import version

import vietnam_compliance

IC_VERSION = version.parse(vietnam_compliance.__version__)


VERSIONS_TO_COMPARE = [
    {
        "app_name": "Frappe",
        "current_version": version.parse(frappe.__version__),
        "required_major": 16,
    },
    {
        "app_name": "ERPNext",
        "current_version": version.parse(erpnext.__version__),
        "required_major": 16,
    },
]


def execute():
    for app in VERSIONS_TO_COMPARE:
        app_name = app["app_name"]
        app_version = app["current_version"]
        required_major = app["required_major"]

        if app_version.major < required_major:
            show_error_and_exit(
                f"Incompatible {app_name} Version: \n"
                f"{app_name} version {app_version} not compatible with Vietnam Compliance.\n"
                f"Please upgrade {app_name} to version {required_major} or above.\n"
            )


def show_error_and_exit(error_message):
    click.secho(error_message, fg="red")
    raise SystemExit(1)
