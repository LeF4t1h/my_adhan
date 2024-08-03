import pulsectl


class VolumeController:
    def __init__(self):
        self.pulse = pulsectl.Pulse("volume-controller")
        self.sink = self.get_default_sink()
        self.muted = self.sink.mute

    def get_default_sink(self):
        # Get the default sink (output device)
        return self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)

    def toggle_mute(self):
        # Toggle mute state
        self.muted = not self.muted
        self.pulse.mute(self.sink, self.muted)
        return self.muted
