import click
import frappe

from vietnam_compliance.audit_trail.setup import setup_fixtures as setup_audit_trail
from vietnam_compliance.vat_vietnam.constants import BUG_REPORT_URL
from vietnam_compliance.vat_vietnam.setup import after_install as setup_vat


def after_install():
    try:
        setup_audit_trail()

        print("Setting up VAT Vietnam...")
        setup_vat()

        click.secho("Vietnam Compliance installed successfully!", fg="green")

    except Exception as e:
        click.secho(
            f"Installation for Vietnam Compliance failed. Report at {BUG_REPORT_URL}",
            fg="bright_red",
        )
        raise e


def after_app_install(app_name):
    from vietnam_compliance.vat_vietnam.setup import (
        create_education_custom_fields,
        create_healthcare_custom_fields,
        create_hrms_custom_fields,
    )

    if app_name == "hrms":
        create_hrms_custom_fields()

    if app_name == "education":
        create_education_custom_fields()

    if app_name == "healthcare":
        create_healthcare_custom_fields()
