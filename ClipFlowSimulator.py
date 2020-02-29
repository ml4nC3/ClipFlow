# coding=utf-8
# Import des librairies externes
import sys
import serial
from timeit import default_timer as timer
import logging

# Import des bibliothèques de Qt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTreeWidgetItemIterator
from PyQt5.QtCore import QTimer

# Import de la définition de l'interface
from Ui_MainWin import Ui_MainWindow
# Interface créée avec Qt Creator au format .ui et convertie en classe python avec la commande :
# pyuic5 mainwindow.ui -o Ui_MainWin.py

# Import des modules
import FSM_LeakDetection as FsmLD
import FSM_Events as FsmEv

# Couleurs à utiliser :
# vert_baissé = rgb(85, 170, 127)
# vert foncé =  rgb(0, 85, 0)
# vert clair =  rgb(85, 255, 127)
# rouge foncé = rgb(170, 0, 0)
# rouge clair = rgb(255, 0, 0)
# gris clair = rgb(240, 240, 240);

logging.basicConfig(filename='clipflow.log',
                    level=logging.DEBUG,
                    format='%(asctime)s|%(levelname)s|%(name)s|%(threadName)s|%(message)s')


class MainWindow:
    """Classe de la fenêtre principale de l'application"""

    def __init__(self):
        """Constructeur de la classe MainWindow"""
        logging.info('Creating MainWindow instance.')

        # Initialisation de l'interface graphique
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        # TODO Ajouter dialog de crédit

        # Création des objets nécessaires au fonctionnement
        self.flow_meter = None
        self.leak_detection = None
        self._off_time_pressed = None
        self._timer = QTimer()  # Création du timer de cadencement du jeu
        self.serial_com = None  # Création de l'attribut destiné à l'objet série
        self._serial_settings = {'PORT': 'COM2', 'BAUDRATE': 9600, 'TIMEOUT': 1}  # Paramètres liaison série
        self._starter_time = None
        self._battery_voltage = 5000
        self._state = 'NORMAL'               # Détermine le mode de comportement de l'interface

        # Initialisation des évènements de consomation
        flush = dict(NAME="Chasse d'eau",
                     DURATIONS=[2, 100, 70],
                     MAX_FLOW=100)
        shower = dict(NAME="Douche",
                      DURATIONS=[5, 420, 3],
                      MAX_FLOW=540)
        bath = dict(NAME="Bain",
                    DURATIONS=[2, 500, 2],
                    MAX_FLOW=828)
        hand_wash = dict(NAME="Lavage de mains",
                         DURATIONS=[2, 10, 2],
                         MAX_FLOW=375)
        self.events_list = [flush, hand_wash, shower, bath]
        self.ui.cmbx_event_selector.addItem(None)
        for event in self.events_list:
            self.ui.cmbx_event_selector.addItem(event["NAME"])
        self.events_list.insert(0, None)
        self._tree_object_items = []

        # Définition des couleurs du levier
        self._lever_styles = {'Baissé': 'background-color: rgb(85, 170, 127);\ncolor: rgb(240, 240, 240);',
                              'Levé': 'background-color: rgb(170, 0, 0);\ncolor: rgb(240, 240, 240);'}

        # TODO envisager de créer les LED en tant qu'objet à part
        # Création des caractéristiques de la LED verte
        self._green_led_last_blink = None       # Timestamp de la dernière séquence de cligno (évite un timer supp)

        self._green_led_state = False           # Etat actuel de la LED (False = éteinte / True = allumée)
        self._green_led_count = 0               # Nombre de changement d'état restants à réaliser
        self._green_led_blink_timer = QTimer()  # Timer pour gérer les clignotements
        self._green_led_styles = {True: 'background-color: rgb(85, 255, 127);',
                                  False: 'background-color: rgb(0, 60, 0);'}  # Couleurs de fond des objets label

        # Création des caractéristiques de la LED rouge
        self._flag_3_red_blinks = False         # Flag pour éviter la répétition des 3 blinks (voir on_timer_top)
        self._red_led_mode = ''
        self._red_led_last_blink = None
        self._red_led_state = False
        self._red_led_count = 0
        self._red_led_blink_timer = QTimer()
        self._red_led_alarm_timer = QTimer()    # Timer spécifique à la LED rouge pour clignoter après coupure
        self._red_led_styles = {True: 'background-color: rgb(255, 0, 0);',
                                False: 'background-color: rgb(120, 0, 0);'}

        # Connexion des signaux de l'interface avec les méthodes correspondantes
        self.ui.btn_off.pressed.connect(self._on_btn_off_pressed)
        self.ui.btn_off.released.connect(self._on_btn_off_released)
        self.ui.btn_lever.clicked.connect(self._on_button_lever_click)
        self.ui.lineEdit_com_port.editingFinished.connect(self._on_serial_parameter_change)
        self.ui.spinBox_baudrate.valueChanged.connect(self._on_serial_parameter_change)
        self.ui.vslider_battery.valueChanged.connect(self._on_voltage_changed)
        self.ui.vslider_battery.sliderReleased.connect(self._on_voltage_slider_release)
        self.ui.cmbx_event_selector.currentIndexChanged.connect(self.on_event_selection)
        self.ui.btn_event_start.clicked.connect(self.on_start_event)

        # Signaux des Timers
        self._timer.timeout.connect(self._on_timer_top)
        self._green_led_blink_timer.timeout.connect(self._green_led_blink_signal)
        self._red_led_blink_timer.timeout.connect(self._red_led_blink_signal)

    def _on_button_lever_click(self):
        # Démarrage de la liaison série
        try:
            self.serial_com = serial.Serial(self._serial_settings['PORT'],
                                            baudrate=self._serial_settings['BAUDRATE'],
                                            timeout=self._serial_settings['TIMEOUT'])
            logging.info("COM port created: " + str(self.serial_com))
            self.ui.lbl_com_status_text.setText(f"Connecté sur {self._serial_settings['PORT']} "
                                                f"à {self._serial_settings['BAUDRATE']} bauds")
        except Exception as error:
            self.ui.lbl_com_status_text.setText("Erreur port série")
            self.ui.lbl_com_status_text.setStyleSheet('background-color: rgb(255, 231, 232);')
            logging.error("Failed to start COM port: " + str(error))

        # Création/paramétrage des objets
        self.flow_meter = FlowMeter()
        self.leak_detection = FsmLD.LeakDetection()
        self._starter_time = timer()
        self._green_led_last_blink = self._starter_time
        if self._red_led_alarm_timer.isActive():
            self._red_led_alarm_timer.stop()

        # Paramétrage de l'interface
        self.ui.btn_lever.setEnabled(False)
        self.ui.lbl_lever.setText('Baissé')
        self.ui.lbl_lever.setStyleSheet(self._lever_styles['Baissé'])
        # TODO : voir si la modification de la stylesheet est bien la méthode préconisée pour changer la couleur
        self.ui.lineEdit_com_port.setEnabled(False)     # |
        self.ui.spinBox_baudrate.setEnabled(False)      # Désactive les champs de paramétrage de la liaison série.
        self.green_led_blink(1)  # Déclenche un premier blink de la LED verte. Les suivants sont gérés par on_timer_top.

        # Démarrage du timer principal
        self._timer.start(1000)

    def _on_timer_top(self):
        """Méthode appelée à chaque top du Timer"""
        simulation_duration = int(timer() - self._starter_time)

        # Détection de l'appui long sur le bouton OFF
        if self._off_time_pressed is not None:
            current_duration = int(timer() - self._off_time_pressed)
            self.ui.lbl_time_count.setText(str(current_duration))
            if current_duration >= 8 and not self._flag_3_red_blinks:
                self._flag_3_red_blinks = True
                self._red_led_count = 6
                self._red_led_blink_timer.start(200)
        else:
            self.ui.lbl_time_count.setText('')

        # -----------------------------------------------------------------------------------------
        if self._state == 'INHIBIT':     # Toutes les actions ci-dessous doivent être inhibées
            return None                     # lorsque l'appareil est en mode inhibition
        # -----------------------------------------------------------------------------------------

        # Clignotement LED verte
        last_green_blink = timer() - self._green_led_last_blink
        if (self.leak_detection.get_state() == 'DETECTING' or self._state == 'INHIBIT')\
                and last_green_blink >= 8:
            self.green_led_blink(2)
        elif self.leak_detection.get_state() == 'IDLE' \
                and simulation_duration < 240 \
                and self._battery_voltage > 1500 \
                and last_green_blink >= 5:
            self.green_led_blink(1)

        current_flow = self.flow_meter.flow_measure(self._tree_object_items)
        if current_flow > 0:
            logging.debug(f"current flowrate measure : {str(current_flow)}")
        # Exécution de la machine à état
        self.leak_detection.run(current_flow)

    def _on_btn_off_pressed(self):
        self._off_time_pressed = timer()

    def _on_btn_off_released(self):
        self.ui.lbl_time_count.setText('')
        released_time = timer()
        off_pressed_duration = released_time - self._off_time_pressed
        self._off_time_pressed = None
        logging.debug(f"OFF button released at {str(released_time)} with duration {str(off_pressed_duration)}")
        # Comportement en fonction du temps d'appui du bouton
        if int(off_pressed_duration) >= 8:
            self.lever_trigger()
        elif int(off_pressed_duration) >= 4:
            self._state = 'INHIBIT'
            self.green_led_blink(2)

    def _on_voltage_changed(self):
        self.ui.lbl_battery_voltage.setText(f'{self.ui.vslider_battery.value()/1000}V')
        # TODO battery voltage : afficher seulement 1 ou 2 chiffres après la virgule

    def _on_voltage_slider_release(self):
        self._battery_voltage = self.ui.vslider_battery.value()
        if self._battery_voltage < 1500 and self._starter_time is not None:
            self.lever_trigger()

    def _on_serial_parameter_change(self):
        self._serial_settings['PORT'] = self.ui.lineEdit_com_port.text()
        self._serial_settings['BAUDRATE'] = self.ui.spinBox_baudrate.value()

    def green_led_blink(self, count):
        """Démarrer une séquence de clignotement de la LED verte"""
        self._green_led_count = count * 2       # Pour chaque blink il faut 2 changements d'état
        self._green_led_last_blink = timer()    #
        self._green_led_blink_timer.start(200)  #

    def _green_led_blink_signal(self):
        self._green_led_state = not self._green_led_state
        self.ui.lbl_green_led.setStyleSheet(self._green_led_styles[self._green_led_state])
        self._green_led_count -= 1
        if self._green_led_count <= 0:
            self._green_led_blink_timer.stop()

    def red_led_blink(self, count):
        """Démarrer une séquence de clignotement de la LED rouge"""
        self._red_led_count = count * 2
        self._red_led_last_blink = timer()
        self._red_led_blink_timer.start(200)

    def _red_led_blink_signal(self):
        self._red_led_state = not self._red_led_state
        self.ui.lbl_red_led.setStyleSheet(self._red_led_styles[self._red_led_state])
        self._red_led_count -= 1
        if self._red_led_count <= 0:
            self._red_led_blink_timer.stop()

    def on_event_selection(self):
        if self.ui.cmbx_event_selector.currentIndex() == 0:
            self.ui.btn_event_start.setEnabled(False)
        else:
            self.ui.btn_event_start.setEnabled(True)

    def on_start_event(self):
        selected = self.ui.cmbx_event_selector.currentIndex()
        tree_item = self.flow_meter.start_flow_event(self.ui.tree_events, selected, self.events_list)
        self.ui.cmbx_event_selector.setCurrentIndex(0)
        self._tree_object_items.append(tree_item)

    def lever_trigger(self):
        """Déclencher la coupure de l'arrivée d'eau"""
        logging.info("Triggering lever")
        self._timer.stop()
        # TODO détruire flowmeter
        # TODO détruire leak_detection
        if self.serial_com is not None and self.serial_com.isOpen():
            self.serial_com.close()

        # Réinitialisation des paramètres
        self._flag_3_red_blinks = False
        self._starter_time = None
        self._green_led_last_blink = None
        # TODO : vérifier la bonne réinitialisation de tous les paramètres de simulation ici

        # Mise à jour de l'interface
        self.ui.btn_lever.setEnabled(True)
        self.ui.lbl_lever.setText('Levé')
        self.ui.lbl_lever.setStyleSheet(self._lever_styles['Levé'])
        self.ui.lbl_com_status_text.setStyleSheet('background-color: rgb(240, 240, 240);')
        self.ui.lbl_com_status_text.setText('Déconnecté')
        self.ui.lineEdit_com_port.setEnabled(True)
        self.ui.spinBox_baudrate.setEnabled(True)

    def show(self):
        self.main_win.show()


class FlowMeter:
    def __init__(self):
        self._flowrate = 0

    def flow_measure(self, tree_object_items):
        # Décrémentation du délai restant des évènements
        for item in tree_object_items:
            new_flow, reamining_time = item[1].run(int(item[0].text(1)))
            # reamining_time = int(item[0].text(2))
            # reamining_time -= 1
            item[0].setText(1, str(new_flow))
            item[0].setText(2, str(reamining_time))

        # TODO ajouter ici le calcul de la somme des débit de tous les évènements
        return self._flowrate

    def start_flow_event(self, tree_object, selected, events_list):
        # Création d'un nouvel objet event
        event_object = FsmEv.FlowEvent(events_list[selected]["DURATIONS"], events_list[selected]["MAX_FLOW"])
        # Création de la ligne dans l'interface
        name = events_list[selected]["NAME"]
        durations = events_list[selected]["DURATIONS"]
        duration = durations[0] + durations[1] + durations[2]
        item = QtWidgets.QTreeWidgetItem(tree_object, [name, str(0), str(duration)])
        return item, event_object


if __name__ == "__main__":
    logging.info("Starting Application")
    app = QApplication(sys.argv)

    # Création de l'application
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
