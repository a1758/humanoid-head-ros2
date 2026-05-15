"""Expression engine with PD effort control via Gazebo's ApplyJointEffort."""

import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from gazebo_msgs.srv import ApplyJointEffort

from .state_machine import StateMachine
from .cli_handler import CLIHandler

CONTROLLED_JOINTS = [
    'left_eyelid_joint',
    'right_eyelid_joint',
    'jaw_joint',
    'left_smile_joint',
    'right_smile_joint',
]

KP = 5.0  # proportional gain
KD = 0.3  # derivative gain (small, only applied when velocity is valid)


class ExpressionEngine(Node):

    def __init__(self):
        super().__init__('expression_engine')

        self.state_machine = StateMachine(self)
        self.cli_handler = CLIHandler(self, self.state_machine)

        self.current_pos = {j: 0.0 for j in CONTROLLED_JOINTS}
        self.current_vel = {j: 0.0 for j in CONTROLLED_JOINTS}

        self.js_sub = self.create_subscription(
            JointState, '/joint_states', self._on_joint_states, 10)

        self.effort_cli = self.create_client(ApplyJointEffort, '/apply_joint_effort')
        while not self.effort_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /apply_joint_effort ...')

        # 50 Hz PD control loop
        self.ctrl_timer = self.create_timer(0.02, self._control_loop)

        self.get_logger().info('Expression engine started '
                               '(PD effort control on /apply_joint_effort)')

    def _on_joint_states(self, msg):
        for i, name in enumerate(msg.name):
            if name in self.current_pos:
                self.current_pos[name] = msg.position[i]
                if i < len(msg.velocity) and not math.isnan(msg.velocity[i]):
                    self.current_vel[name] = msg.velocity[i]

    def _control_loop(self):
        targets = self.state_machine.get_positions()
        for i, joint in enumerate(CONTROLLED_JOINTS):
            err = targets[i] - self.current_pos[joint]
            vel = self.current_vel.get(joint, 0.0)
            effort = KP * err - KD * vel
            effort = max(-5.0, min(5.0, effort))
            self._send_effort(joint, effort)

    def _send_effort(self, joint_name, effort):
        req = ApplyJointEffort.Request()
        req.joint_name = joint_name
        req.effort = effort
        req.start_time.sec = 0
        req.start_time.nanosec = 0
        req.duration.sec = -1
        req.duration.nanosec = 0
        self.effort_cli.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    node = ExpressionEngine()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
