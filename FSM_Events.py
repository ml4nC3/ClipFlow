# coding=utf-8
import logging
from timeit import default_timer as timer

logger = logging.getLogger(__name__)    # Récupération du logger créé dans le module


class FlowEvent:
    def __init__(self, durations, flow_max):
        # Paramètres généraux
        self._current_flow = 0
        self.start_time = timer()
        self._phases = [(self._flow_raise_phase, durations[0]),
                        (self._flow_stable_phase, durations[1]),
                        (self._flow_reduce_phase, durations[2])]
        self._phase = 0
        self._flow_max = flow_max
        # Calcul des durées
        self._total_duration = durations[0] + durations[1] + durations[2]
        self._stable_end_time = self._phases[0][1] + self._phases[1][1]
        # Calcul des pas de débit pour chaque seconde de montée et descente
        self._raise_flow_step = int(self._flow_max / self._phases[0][1])
        self._reduce_flow_step = int(self._flow_max / self._phases[2][1])

    def _flow_raise_phase(self, current_flow):
        current_flow += self._raise_flow_step
        if current_flow > self._flow_max:
            current_flow = self._flow_max
        current_duration = int(timer() - self.start_time)
        if current_duration >= self._phases[0][1]:
            self._phase = 1
        if current_flow == 0:
            return 1, self._total_duration - current_duration
        return current_flow, self._total_duration - current_duration

    def _flow_stable_phase(self, current_flow):
        current_duration = int(timer() - self.start_time)
        if current_duration >= self._stable_end_time:
            self._phase = 2
        return self._flow_max, self._total_duration - current_duration

    def _flow_reduce_phase(self, current_flow):
        current_flow -= self._reduce_flow_step
        current_duration = int(timer() - self.start_time)
        if current_duration >= self._total_duration:
            return 0, 0
        return current_flow, self._total_duration - current_duration

    def run(self, current_flow):
        handler = self._phases[self._phase][0]
        return handler(current_flow)

    def __del__(self):
        # Afin de vérifier que les objets sont bien détruits
        logger.info("Event terminated")


class Leak:
    def __init__(self, leak_flow):
        self._leak_flow = leak_flow

    def run(self, current_flow):
        return self._leak_flow, 1000
