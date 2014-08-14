from behave import step


@step(u'I log "{expression}"')
def log(context, expression):
    context.behaving_log.append(expression)
