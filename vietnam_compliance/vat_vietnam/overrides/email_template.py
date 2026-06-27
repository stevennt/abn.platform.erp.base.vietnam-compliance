from vietnam_compliance.vat_vietnam.setup import update_default_email_template


def after_rename(doc, method=None, *args, **kwargs):
    old_name = args[0]
    new_name = args[1]

    update_default_email_template(old_name, new_name)


def on_trash(doc, method=None):
    update_default_email_template(doc.name, None)
