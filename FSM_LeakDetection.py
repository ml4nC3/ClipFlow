# coding=utf-8
import logging

logger = logging.getLogger(__name__)    # Récupération du logger créé dans le module


class LeakDetection:
    """Machine à état assurant la gestion du comportement de comptage"""
    def __init__(self):

        # Initialisation de la machine à état
        self._state = 'INIT'
        self._handlers = {'INIT': self.on_state_init,            # Etat d'initialisation de la machine
                          'IDLE': self.on_state_idle,            # Etat de repos (débit nul ou instable)
                          'DETECTING': self.on_state_detecting,  # Détection de débit stable = comptage volume
                          'ALARM': self.on_state_alarm}          # Fuite détectée et volume ou débit limite dépasssé
        self._config = {'VOL_HIGH': 300,
                        'VOL_LOW': 50,
                        'FLOW_HIGH': 2000,
                        'FLOW_LOW': 10,
                        'FLOW_MAX': 2500}
        self._leak_time = 0
        self._current_volume = 0
        self._slope = 0
        self._y_intercept = 0
        self._stable_flow = 0
        self._null_flow = 0
        self._previous_flow = 0

    def get_state(self):
        return self._state

    def on_state_init(self, current_flow):
        # Calcul des paramètres permettant de déterminer le vol limite pour un débit donné
        volume_spread = self._config['VOL_HIGH'] - self._config['VOL_LOW']
        flow_spread = self._config['FLOW_HIGH'] - self._config['FLOW_LOW']
        # Coefficient directeur
        self._slope = volume_spread / flow_spread
        # Ordonnée à l'origine
        self._y_intercept = self._config['VOL_HIGH'] - self._slope * self._config['FLOW_HIGH']

        logger.debug(f'FSM initialized with slope {self._slope} and y0 {self._y_intercept}')
        return 'IDLE'   # La fin de l'initialisation se termine forcément sur l'état repos

    def on_state_idle(self, current_flow):
        self._leak_time = 0
        self._current_volume = 0
        if current_flow > 0:    # TODO rassembler la gestion du flow state dans une fonction commune ?
            self._null_flow = 0
            if self._previous_flow == current_flow:
                self._previous_flow = current_flow
                self._stable_flow = 1
                logger.info('Leack detection switching to DETECTING')
                return 'DETECTING'
            else:
                self._stable_flow = 0
        else:
            self._null_flow = 1
        self._previous_flow = current_flow
        logger.debug(f"""Leack detection still on IDLE with 
                    null_flow = {self._null_flow} and stable_flow = {self._stable_flow}""")
        return 'IDLE'

    def on_state_detecting(self, current_flow):
        if current_flow > 0:
            pass
        return 'IDLE'

    def on_state_alarm(self, current_flow):
        return 'ALARM'

    def run(self, current_flow):
        handle = self._handlers[self._state]
        self._state = handle(current_flow)
