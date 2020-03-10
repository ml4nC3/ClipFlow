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
        # Configuration par défaut des bornes de déclenchement sur fuite
        self._config = {'VOL_HIGH': 300,
                        'VOL_LOW': 50,
                        'FLOW_HIGH': 2000,
                        'FLOW_LOW': 10,
                        'FLOW_MAX': 2500}
        # Variables de comptage
        self._leak_time = 0
        self._current_volume = 0
        self._index = 0
        # Variables calculées de la droite de déclenchement
        self._slope = 0
        self._y_intercept = 0
        # Caractéristiques du débit
        self._stable_flow = False
        self._null_flow = True
        self._previous_flow = 0

    def get_state(self):
        logger.debug(f'null={self._null_flow}, '
                     f'stable={self._stable_flow}, '
                     f'state={self._state}, '
                     f'leak time={self._leak_time}, '
                     f'leak vol={self._current_volume}'
                     f'index={self._index}')
        # Retour des paramètres internes de la machine à état pour affichage dans l'interface et gestion de l'alarme
        return self._null_flow, self._stable_flow, self._state, self._leak_time, self._current_volume, self._index

    def _update_flow_flags(self, current_flow):
        # Mise à jour des drapeaux de comportement du débit mesuré
        if current_flow > 0:
            # Débit non nul
            self._null_flow = False
            if self._previous_flow == current_flow:
                # Débit stable car identique à la mesure précédente
                self._stable_flow = True
            else:
                self._stable_flow = False
        else:
            # Débit nul
            self._null_flow = True
        self._previous_flow = current_flow

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
        # Etat d'attente de la machine
        # Initialisation des variables de comptage
        self._leak_time = 0
        self._current_volume = 0
        if not self._null_flow and self._stable_flow:
            # Si le débit est non nul ET stable alors la machine passe à l'état de détection
            logger.info('Leak detection switching to DETECTING')
            return 'DETECTING'
        else:
            # Autrement la machine reste à l'état d'attente
            return 'IDLE'

    def on_state_detecting(self, current_flow):
        if self._null_flow or not self._stable_flow:
            # Si le débit redevient instable ou nul : retour à l'état d'attente
            logger.info('Leak detection switching to IDLE')
            return 'IDLE'
        else:
            # Sinon démarrage du comptage
            self._leak_time += 1
            self._current_volume = int(current_flow * self._leak_time / 3.6)  # Resultat en mL
            logger.debug(f'leak time = {self._leak_time} and current vol = {self._current_volume}')

            # Détection des dépassements de limite soit du max soit du volume limite fonction du débit
            vol_max_exceeded = self._current_volume > self._config['VOL_HIGH'] * 1000
            vol_limit_exceeded = self._current_volume >= self._slope * current_flow * 1000 + self._y_intercept
            flow_max_exceeded = current_flow >= self._config['FLOW_MAX']
            # Si l'un des 3 tests ci-dessus est vrai : déclenchement du mode alarme
            if vol_max_exceeded or vol_limit_exceeded or flow_max_exceeded:
                logger.info(f'Leak detected with vol limit={vol_limit_exceeded}, '
                            f'vol max={vol_max_exceeded} and flow={flow_max_exceeded}')
                return 'ALARM'
            # Si aucune limite n'est dépassée la machine continue le comptage
            return 'DETECTING'

    def on_state_alarm(self, current_flow):
        # Le mode alarme ne nécessite aucune action de la part de la machine
        # Cette méthode pourrait donc être supprimée mais je l'aime bien
        return 'ALARM'

    def run(self, current_flow):
        # Gestion de l'exécution de la machine
        # Mise à jour des drapeaux de comportement débit
        self._update_flow_flags(current_flow)
        self._index += int(current_flow / 3.6)  # Incrémentation de l'index de volume total en mL
        # Récupération de la méthode à appeler en fonction de l'état en cours
        handle = self._handlers[self._state]
        # Mise à jour de l'état en fonction de l'exécution de la méthode récupérée
        self._state = handle(current_flow)
