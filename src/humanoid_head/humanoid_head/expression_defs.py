"""Joint position presets for each expression state.

Joint order (matching head_controllers.yaml):
  [left_eyelid, right_eyelid, jaw, left_smile, right_smile]
"""

EXPRESSIONS = {
    'neutral':    [0.0,  0.0,  0.0,  0.0,  0.0],
    'blink':      [1.5,  1.5,  0.0,  0.0,  0.0],
    'wink_left':  [1.5,  0.0,  0.0,  0.0,  0.0],
    'wink_right': [0.0,  1.5,  0.0,  0.0,  0.0],
    'smile':      [0.0,  0.0,  0.0,  0.3,  0.3],
    'mouth_open': [0.0,  0.0,  0.4,  0.0,  0.0],
    'surprise':   [0.0,  0.0,  0.35, 0.0,  0.0],
    'frown':      [0.0,  0.0,  0.0, -0.3, -0.3],
}

# How long each expression holds before auto-returning to neutral (seconds)
EXPRESSION_DURATION = {
    'blink': 0.15,
    'wink_left': 0.3,
    'wink_right': 0.3,
    'smile': 3.0,
    'mouth_open': 2.0,
    'surprise': 2.0,
    'frown': 3.0,
    'neutral': 0.0,
}

# Blink timing range (seconds)
BLINK_INTERVAL_MIN = 3.0
BLINK_INTERVAL_MAX = 6.0
BLINK_DURATION = 0.15
