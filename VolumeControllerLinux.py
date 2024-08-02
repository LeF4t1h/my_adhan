import pulsectl


class VolumeController:
    def __init__(self):
        self.pulse = pulsectl.Pulse('volume-controller')
        self.sink = self.get_default_sink()
        self.muted = self.sink.mute

    def toggle_mute(self):
        # Toggle mute state
        self.muted = not self.muted
        self.pulse.mute(self.sink, self.muted)
        return self.muted