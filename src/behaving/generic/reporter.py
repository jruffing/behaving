import sys
from behave.reporter.base import Reporter


class LoggerReporter(Reporter):
    output_stream_name = "stdout"

    def __init__(self, config):
        super(LoggerReporter, self).__init__(config)
        self.stream = getattr(sys, self.output_stream_name, sys.stderr)

    def feature(self, feature):
        self.stream.write('\nBehaving log for: %s\n' % feature.name)
        for line in feature.behaving_log:
            self.stream.write(line)
            self.stream.write('\n')

    def end(self):
        self.stream.write('end')
