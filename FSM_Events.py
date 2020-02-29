# coding=utf-8
import logging
from timeit import default_timer as timer

logger = logging.getLogger(__name__)    # Récupération du logger créé dans le module


class FlowEvent:
    def __init__(self, durations, flow_max):
        self._phases = [(self._flow_raise_phase, durations[0]),
                        (self._flow_stable_phase, durations[1]),
                        (self._flow_reduce_phase, durations[2])]
        self._phase = 0
        self._total_duration = durations[0] + durations[1] + durations[2]
        self._flow_max = flow_max
        self._current_flow = 0
        self.start_time = timer()

    def _flow_raise_phase(self, current_flow):
        flow_step = int(self._flow_max / self._phases[0][1])
        current_flow += flow_step
        current_duration = int(timer() - self.start_time)
        if current_duration >= self._phases[0][1]:
            self._phase = 1
        if current_flow == 0:
            return 1
        return current_flow, self._total_duration - current_duration

    def _flow_stable_phase(self, current_flow):
        current_duration = int(timer() - self.start_time)
        if current_duration >= self._phases[0][1] + self._phases[1][1]:
            self._phase = 2
        return self._flow_max, self._total_duration - current_duration

    def _flow_reduce_phase(self, current_flow):
        flow_step = int(self._flow_max / self._phases[0][1])
        current_flow += flow_step
        current_duration = int(timer() - self.start_time)
        if current_duration >= self._phases[0][1] + self._phases[1][1]:
            return 0, 0
        return current_flow, self._total_duration - current_duration

    def run(self, current_flow):
        handler = self._phases[self._phase][0]
        return handler(current_flow)
