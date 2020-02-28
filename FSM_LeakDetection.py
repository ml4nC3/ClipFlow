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
        self._stable_flow = False
        self._null_flow = True
        self._previous_flow = 0

    def get_state(self):
        return self._state

    def _update_flow_flags(self, current_flow):
        if current_flow > 0:
            self._null_flow = False
            if self._previous_flow == current_flow:
                self._stable_flow = True
            else:
                self._stable_flow = False
        else:
            self._null_flow = True
        self._previous_flow = current_flow
        # TODO envisager de convertir les attributs null & stable en variables passées en paramètres

    def on_state_init(self, current_flow):
        # Calcul des paramètres permettant de déterminer le vol limite pour un débit donné
        volume_spread = self._config['VOL_HIGH'] - self._config['VOL_LOW']
        flow_spread = self._config['FLOW_HIGH'] - self._config['FLOW_LOW']
        # Coefficient directeur
        self._slope = volume_spread / flow_spread
        # Ordonnée à l'origine
        self._y_intercept = self._config['VOL_HIGH'] - self._slope * self._config['FLOW_HIGH']
        self._y_intercept = int(self._y_intercept * 1000)  # Conversion en mL
        logger.debug(f'FSM initialized with slope {self._slope} and y0 {self._y_intercept}')
        return 'IDLE'   # La fin de l'initialisation se termine forcément sur l'état repos

    def on_state_idle(self, current_flow):
        self._leak_time = 0
        self._current_volume = 0
        if not self._null_flow and self._stable_flow:
            logger.info('Leack detection switching to DETECTING')
            return 'DETECTING'
        else:
            logger.debug(f"Leack detection still on IDLE with"
                         f"null_flow={self._null_flow} and stable_flow={self._stable_flow}")
            return 'IDLE'

    def on_state_detecting(self, current_flow):
        if self._null_flow or not self._stable_flow:
            logger.info('Leack detection switching to IDLE')
            return 'IDLE'
        else:
            self._leak_time += 1
            self._current_volume = int(current_flow * self._leak_time / 3.6)  # Result in mL
            logger.debug(f'leak time = {self._current_volume} and current vol = {self._leak_time}')
            # Détection des dépassements de limite soit du max soit du volume limite fonction du débit
            vol_max_exceeded = self._current_volume > self._config['VOL_HIGH'] * 1000
            vol_limit_exceeded = self._current_volume >= self._slope * current_flow + self._y_intercept
            if vol_max_exceeded or vol_limit_exceeded:
                logger.info(f'Leak detected with limit={vol_limit_exceeded} and max={vol_max_exceeded}')
                return 'ALARM'
            logger.info('Leack detection still on DETECTING')
            return 'DETECTING'

    def on_state_alarm(self, current_flow):
        return 'ALARM'

    def run(self, current_flow):
        self._update_flow_flags(current_flow)
        handle = self._handlers[self._state]
        self._state = handle(current_flow)
