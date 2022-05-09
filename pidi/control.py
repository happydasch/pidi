import RPi.GPIO as GPIO

from pkg_resources import iter_entry_points
from .client import ClientMPD


def get_control_types():
    """Enumerate the pidi.plugin.client entry point and return installed client types."""
    control_types = {
        'dummy': ControlDummy,
        'gpiompd': ControlGPIOMPD
    }

    for entry_point in iter_entry_points("pidi.plugin.control"):
        try:
            plugin = entry_point.load()
            control_types[plugin.option_name] = plugin
        except (ModuleNotFoundError, ImportError) as err:
            print("Error loading client plugin {entry_point}: {err}".format(
                entry_point=entry_point,
                err=err
            ))

    return control_types


class ControlDummy():

    def __init__(self, args=None):
        pass

    def add_args(argparse):
        pass

    def set_client(self, client):
        pass

    def update_controls(self):
        pass


class ControlGPIOMPD():

    # The buttons on Pirate Audio are connected to pins 5, 6, 16 and 24
    # Boards prior to 23 January 2020 used 5, 6, 16 and 20
    # try changing 24 to 20 if your Y button doesn't work.
    BUTTONS = [5, 6, 16, 24]

    # These correspond to buttons A, B, X and Y respectively
    LABELS = ['A', 'B', 'X', 'Y']

    """Control buttons on GPIO for mpd."""
    def __init__(self, args=None):
        self._client = None
        # Set up RPi.GPIO with the "BCM" numbering scheme
        GPIO.setmode(GPIO.BCM)
        # Buttons connect to ground when pressed, so we should set them up
        # with a "PULL UP", which weakly pulls the input signal to 3.3V.
        GPIO.setup(self.BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Loop through out buttons and attach the "handle_button" function to each
        # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
        # picking a generous bouncetime of 100ms to smooth out button presses.
        for pin in self.BUTTONS:
            GPIO.add_event_detect(
                pin, GPIO.FALLING,
                self.handle_button,
                bouncetime=100)

    def add_args(argparse):
        pass

    def set_client(self, client):
        if isinstance(client, ClientMPD):
            self._client = client._client
            return
        raise Exception('Client needs to be ClientMPD')

    def update_controls(self):
        pass

    # "handle_button" will be called every time a button is pressed
    # It receives one xargument: the associated input pin.
    def handle_button(self, pin):
        label = self.LABELS[self.BUTTONS.index(pin)]
        if self._client is None:
            print("No client set")
            return
        if pin == self.BUTTONS[0]:    # A
            self._client.pause()
            print("Control pause")
        elif pin == self.BUTTONS[2]:  # X
            self._client.next()
            print("Control next")
        elif pin == self.BUTTONS[1]:  # B
            self._client.volume(-5)
            print("Control voldown")
        elif pin == self.BUTTONS[3]:  # Y
            self._client.volume(5)
            print("Control volup")
        else:
            raise Exception("Unknown pin: {}".format(pin))
