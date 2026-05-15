from std_msgs.msg import String


class CLIHandler:
    """Subscribes to /expression_command and dispatches to state machine."""

    def __init__(self, node, state_machine):
        self.state_machine = state_machine
        self.sub = node.create_subscription(
            String, '/expression_command', self._on_command, 10)

    def _on_command(self, msg):
        cmd = msg.data.strip().lower()
        if cmd in ('talking_start', 'talking_on'):
            self.state_machine.start_talking()
        elif cmd in ('talking_stop', 'talking_off'):
            self.state_machine.stop_talking()
        else:
            self.state_machine.request(cmd)
