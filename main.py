import threading
import _Framework
from _Framework.ControlSurface import ControlSurface
from log import log
from threading import Thread, RLock
from server import Server


class Mixdown(ControlSurface, Server):
    def _initialize_audio_tracks(self):
        i = 1
        tracks = self.song().tracks
        for index, track in enumerate(tracks):
            if track.has_midi_input:
                self.song().create_audio_track(index + i)
                i += 1 # needed to exponentialy grow

    def _index_and_set_tracks(self):
        self._tracks = []
        self._audio_tracks = []
        self._midi_tracks = []
        tracks = self.song().tracks
        for index, track in enumerate(tracks):
            track.index = index
            setattr(track.view, 'is_collapsed',  not track.has_midi_input)
            if track.has_midi_input:
                self._midi_tracks.append(track)
            else:
                self._audio_tracks.append(track)
            self._tracks.append(track)

    def _transfer_vsts(self):
        song = self.song()
        for track in self._midi_tracks:
            for device in track.devices:
                # Possible types are: 0 = undefined, 1 = instrument, 2 = audio_effect, 3 = midi_effect.
                if not device.can_have_drum_pads and device.type == 2:
                    # move all effects to the neighbouring audio track
                    neighbor = self._get_neighbor(track.index)
                    song.move_device(device, neighbor, len(neighbor.devices)) # append at the end always so its in order)

    def _get_neighbor(self, index):
        return self._tracks[index + 1]

    def handle_initialize(self):
        self._initialize_audio_tracks()
        self.schedule_message(1, self._index_and_set_tracks)
        self.schedule_message(1, self._transfer_vsts)
        log('Done Initializing!')

    def handle_revert(self):
        i = 1
        song = self.song()
        for track in self._midi_tracks:
            neighbor = self._get_neighbor(track.index)
            for device in neighbor.devices:
                song.move_device(device, track, len(track.devices))
            if track.index == 0:
                _index = track.index + 1
            elif track.index < 4:
                _index = track.index
            else:
                _index = track.index - i
                # needed to exponentialy decrease as indexes are set manually,
                # and removing them from the list doesnt update their proerties
                i += 1
            song.delete_track(_index)
        log('Done Reverting!')

    def disconnect(self):
        log('Disconnecting!')
        self.stop()

    def __init__(self, c_instance):
        super(Mixdown, self).__init__(c_instance)
        self.lock = RLock()
        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()
