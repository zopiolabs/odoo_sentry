# Copyright 2016-2017 Versada <https://versada.eu/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import collections
import logging

from sentry_sdk import HttpTransport
from sentry_sdk.consts import DEFAULT_OPTIONS
from sentry_sdk.integrations.logging import LoggingIntegration

import odoo.loglevels


def split_multiple(string, delimiter=",", strip_chars=None):
    """Splits :param:`string` and strips :param:`strip_chars` from values."""
    if not string:
        return []
    return [v.strip(strip_chars) for v in string.split(delimiter)]


def to_int_if_defined(value):
    if value == "" or value is None:
        return
    return int(value)


def to_float_if_defined(value):
    if value == "" or value is None:
        return
    return float(value)


SentryOption = collections.namedtuple("SentryOption", ["key", "default", "converter"])

# Mapping of Odoo logging level -> Python stdlib logging library log level.
LOG_LEVEL_MAP = {
    getattr(odoo.loglevels, "LOG_%s" % x): getattr(logging, x)
    for x in ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET")
}
DEFAULT_LOG_LEVEL = "warn"

ODOO_USER_EXCEPTIONS = [
    "odoo.exceptions.AccessDenied",
    "odoo.exceptions.AccessError",
    "odoo.exceptions.DeferredException",
    "odoo.exceptions.MissingError",
    "odoo.exceptions.RedirectWarning",
    "odoo.exceptions.UserError",
    "odoo.exceptions.ValidationError",
    "odoo.exceptions.Warning",
    "odoo.exceptions.except_orm",
]
DEFAULT_IGNORED_EXCEPTIONS = ",".join(ODOO_USER_EXCEPTIONS)

EXCLUDE_LOGGERS = ("werkzeug",)
DEFAULT_EXCLUDE_LOGGERS = ",".join(EXCLUDE_LOGGERS)

DEFAULT_ENVIRONMENT = "develop"

DEFAULT_TRANSPORT = "threaded"


def select_transport(name=DEFAULT_TRANSPORT):
    return {
        "threaded": HttpTransport,
    }.get(name, HttpTransport)


def get_sentry_logging(level=DEFAULT_LOG_LEVEL):
    if level not in LOG_LEVEL_MAP:
        level = DEFAULT_LOG_LEVEL

    return LoggingIntegration(
        # Gather warnings into breadcrumbs regardless of actual logging level
        level=logging.WARNING,
        event_level=LOG_LEVEL_MAP[level],
    )


def get_sentry_options():
    res = [
        SentryOption("dsn", "", str.strip),
        SentryOption("transport", DEFAULT_OPTIONS.get("transport", HttpTransport), select_transport),
        SentryOption("logging_level", DEFAULT_LOG_LEVEL, get_sentry_logging),
        SentryOption("with_locals", DEFAULT_OPTIONS.get("with_locals", True), None),
        SentryOption(
            "max_breadcrumbs", DEFAULT_OPTIONS.get("max_breadcrumbs", 100), to_int_if_defined
        ),
        SentryOption("release", DEFAULT_OPTIONS.get("release", None), None),
        SentryOption("environment", DEFAULT_OPTIONS.get("environment", None), None),
        SentryOption("server_name", DEFAULT_OPTIONS.get("server_name", None), None),
        SentryOption("shutdown_timeout", DEFAULT_OPTIONS.get("shutdown_timeout", None), None),
        SentryOption("integrations", DEFAULT_OPTIONS.get("integrations", None), None),
        SentryOption(
            "in_app_include", DEFAULT_OPTIONS.get("in_app_include", []), split_multiple
        ),
        SentryOption(
            "in_app_exclude", DEFAULT_OPTIONS.get("in_app_exclude", []), split_multiple
        ),
        SentryOption(
            "default_integrations", DEFAULT_OPTIONS.get("default_integrations", True), None
        ),
        SentryOption("dist", DEFAULT_OPTIONS.get("dist", None), None),
        SentryOption(
            "sample_rate", DEFAULT_OPTIONS.get("sample_rate", 1.0), to_float_if_defined
        ),
        SentryOption("send_default_pii", DEFAULT_OPTIONS.get("send_default_pii", False), None),
        SentryOption("http_proxy", DEFAULT_OPTIONS.get("http_proxy", None), None),
        SentryOption("https_proxy", DEFAULT_OPTIONS.get("https_proxy", None), None),
        SentryOption("ignore_exceptions", DEFAULT_IGNORED_EXCEPTIONS, split_multiple),
        SentryOption("request_bodies", DEFAULT_OPTIONS.get("request_bodies", "medium"), None),
        SentryOption("attach_stacktrace", DEFAULT_OPTIONS.get("attach_stacktrace", False), None),
        SentryOption("ca_certs", DEFAULT_OPTIONS.get("ca_certs", None), None),
        SentryOption("propagate_traces", DEFAULT_OPTIONS.get("propagate_traces", True), None),
        SentryOption(
            "traces_sample_rate",
            DEFAULT_OPTIONS.get("traces_sample_rate", None),
            to_float_if_defined,
        ),
    ]

    if "auto_enabling_integrations" in DEFAULT_OPTIONS:
        res.append(
            SentryOption(
                "auto_enabling_integrations",
                DEFAULT_OPTIONS["auto_enabling_integrations"],
                None,
            )
        )

    return res
