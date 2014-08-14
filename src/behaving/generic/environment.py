from behaving.generic.reporter import LoggerReporter


def before_all(context):
    context.config.reporters.append(LoggerReporter(context.config))
    pass


def before_feature(context, feature):
    context.behaving_log = []


def before_scenario(context, scenario):
    pass


def after_feature(context, feature):
    if context.behaving_log:
        feature.behaving_log = context.behaving_log


def after_scenario(context, scenario):
    pass


def after_all(context):
    pass
