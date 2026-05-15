import random
from .expression_defs import (EXPRESSIONS, EXPRESSION_DURATION,
                              BLINK_INTERVAL_MIN, BLINK_INTERVAL_MAX,
                              BLINK_DURATION)


class StateMachine:
    """Manages facial expression state and automatic transitions."""

    def __init__(self, node):
        self.node = node
        self.current_state = 'neutral'
        self.commanded = list(EXPRESSIONS['neutral'])
        self.expression_timer = None
        self.blink_timer = None
        self._schedule_next_blink()

    def get_positions(self):
        return list(self.commanded)

    def request(self, expression):
        """Request an expression. Cancels any running timed expression."""
        if expression not in EXPRESSIONS:
            self.node.get_logger().warn(f'Unknown expression: {expression}')
            return False

        self._cancel_expression_timer()
        self.current_state = expression
        self.commanded = list(EXPRESSIONS[expression])
        self.node.get_logger().info(f'Expression: {expression} -> {self.commanded}')

        duration = EXPRESSION_DURATION.get(expression, 2.0)
        if duration > 0 and expression != 'neutral':
            self.expression_timer = self.node.create_timer(
                duration, self._on_expression_timeout)

        return True

    def _on_expression_timeout(self):
        self._cancel_expression_timer()
        self.current_state = 'neutral'
        self.commanded = list(EXPRESSIONS['neutral'])

    def _cancel_expression_timer(self):
        if self.expression_timer:
            self.node.destroy_timer(self.expression_timer)
            self.expression_timer = None

    def _schedule_next_blink(self):
        interval = random.uniform(BLINK_INTERVAL_MIN, BLINK_INTERVAL_MAX)
        self.blink_timer = self.node.create_timer(interval, self._do_blink)

    def _do_blink(self):
        self.node.destroy_timer(self.blink_timer)
        # Only blink when in neutral or talking (not overriding other expressions)
        if self.current_state in ('neutral', 'talking'):
            saved = self.current_state
            self.current_state = 'blink'
            self.commanded = list(EXPRESSIONS['blink'])
            # Schedule blink recovery
            self.expression_timer = self.node.create_timer(
                BLINK_DURATION,
                lambda: self._recover_from_blink(saved))
        self._schedule_next_blink()

    def _recover_from_blink(self, previous_state):
        if self.expression_timer:
            self.node.destroy_timer(self.expression_timer)
            self.expression_timer = None
        self.current_state = previous_state
        if previous_state == 'talking':
            self._talking_update()
        else:
            self.commanded = list(EXPRESSIONS['neutral'])

    def start_talking(self):
        self._cancel_expression_timer()
        self.current_state = 'talking'
        self._talking_update()
        self._talking_timer = self.node.create_timer(0.2, self._talking_update)

    def stop_talking(self):
        if hasattr(self, '_talking_timer') and self._talking_timer:
            self.node.destroy_timer(self._talking_timer)
            self._talking_timer = None
        self.current_state = 'neutral'
        self.commanded = list(EXPRESSIONS['neutral'])

    def _talking_update(self):
        jaw = random.uniform(0.05, 0.45)
        self.commanded = [0.0, 0.0, jaw, 0.0, 0.0]
