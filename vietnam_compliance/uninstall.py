import click

from vietnam_compliance.vat_vietnam.constants import BUG_REPORT_URL
from vietnam_compliance.vat_vietnam.uninstall import before_uninstall as remove_vat


def before_uninstall():
    try:
        remove_vat()

    except Exception as e:
        click.secho(
            f"Uninstall for Vietnam Compliance failed. Report at {BUG_REPORT_URL}",
            fg="yellow",
        )
        raise e

    click.secho("Vietnam Compliance uninstalled.", fg="green")


def before_app_uninstall(app_name):
    pass
