# Copyright 2016-2017 Versada <https://versada.eu/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Zopio Sentry",
    "summary": "Report Odoo errors to Sentry (Zopio fork for bug fixing and internal usage)",
    "version": "15.0.3.0.2",
    "category": "Extra Tools",
    "website": "https://github.com/zopiolabs/odoo_sentry",
    "author": "Zopio,"
    "Mohammed Barsi,"
    "Versada,"
    "Nicolas JEUDY,"
    "Odoo Community Association (OCA),"
    "Vauxoo",
    "maintainers": ["zopiolabs"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [
            "sentry_sdk<=1.9.0",
        ]
    },
    "depends": [
        "base",
    ],
    "post_load": "post_load",
}
