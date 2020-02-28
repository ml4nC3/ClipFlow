# coding=utf-8
import sys
import serial
from timeit import default_timer as timer
import logging

# Import des bibliothèques de Qt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer

# Import de la définition de l'interface
from Ui_MainWin import Ui_MainWindow
# Interface créée avec Qt Creator au format .ui et convertie en classe python avec la commande :
# pyuic5 mainwindow.ui -o Ui_MainWin.py

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

        # Création des objets nécessaires au fonctionnement
        self.flow_meter = None
        self._off_time_pressed = None
        self._timer = QTimer()  # Création du timer de cadencement du jeu
        self.serial_com = None  # Création de l'attribut destiné à l'objet série
        self._serial_settings = {'PORT': 'COM2', 'BAUDRATE': 9600, 'TIMEOUT': 1}  # Paramètres liaison série
        self._starter_time = None

        # Définition des couleurs du levier
        self._lever_styles = {'Baissé': 'background-color: rgb(85, 170, 127);\ncolor: rgb(240, 240, 240);',
                              'Levé': 'background-color: rgb(170, 0, 0);\ncolor: rgb(240, 240, 240);'}

        # Création des caractéristiques de la LED verte
        self._green_led_last_blink = None       # Timestamp de la dernière séquence de cligno (évite un timer supp)
        self._green_led_state = False           # Etat actuel de la LED (False = éteinte / True = allumée)
        self._green_led_count = 0               # Nombre de changement d'état restants à réaliser
        self._green_led_blink_timer = QTimer()  # Timer pour gérer les clignotements
        self._green_led_styles = {True: 'background-color: rgb(85, 255, 127);',
                                  False: 'background-color: rgb(0, 60, 0);'} # Couleurs de fond des objets label

        # Création des caractéristiques de la LED rouge
        self._flag_3_red_blinks = False     # Flag pour éviter la répétition des 3 blinks (voir on_timer_top)
        self._red_led_last_blink = None
        self._red_led_state = False
        self._red_led_count = 0
        self._red_led_blink_timer = QTimer()
        self._red_led_styles = {True: 'background-color: rgb(255, 0, 0);',
                                False: 'background-color: rgb(120, 0, 0);'}

        # Connexion des signaux de l'interface avec les méthodes correspondantes
        self.ui.btn_off.pressed.connect(self.on_btn_off_pressed)
        self.ui.btn_off.released.connect(self.on_btn_off_released)
        self.ui.btn_lever.clicked.connect(self.on_button_lever_click)
        self.ui.lineEdit_com_port.editingFinished.connect(self.on_serial_parameter_change)
        self.ui.spinBox_baudrate.valueChanged.connect(self.on_serial_parameter_change)

        # Signaux des Timers
        self._timer.timeout.connect(self.on_timer_top)
        self._green_led_blink_timer.timeout.connect(self.green_led_blink)
        self._red_led_blink_timer.timeout.connect(self.red_led_blink)

    def on_button_lever_click(self):
        # Démarrage de la liaison série
        try:
            self.serial_com = serial.Serial(self._serial_settings['PORT'],
                                            baudrate=self._serial_settings['BAUDRATE'],
                                            timeout=self._serial_settings['TIMEOUT'])
            logging.info("COM port created: " + str(self.serial_com))
        except Exception as error:
            self.ui.lbl_com_status_text.setText("Erreur port série")
            self.ui.lbl_com_status_text.setStyleSheet('background-color: rgb(255, 231, 232);')
            logging.error("Failed to start COM port: " + str(error))

        # Création/paramétrage des objets
        self.flow_meter = FlowMeter()
        self._starter_time = timer()
        self._green_led_last_blink = self._starter_time

        # Paramétrage de l'interface
        self.ui.btn_lever.setEnabled(False)
        self.ui.lbl_lever.setText('Baissé')
        self.ui.lbl_lever.setStyleSheet(self._lever_styles['Baissé'])
        # TODO : voir si la modification de la stylesheet est bien la méthode préconisée pour changer la couleur
        self._timer.start(1000)

    def on_timer_top(self):
        """Méthode appelée à chaque top du Timer"""
        simulation_duration = int(timer() - self._starter_time)

        # Détection de l'appui long sur le bouton OFF
        if self._off_time_pressed is not None:
            current_duration = int(timer() - self._off_time_pressed)
            self.ui.lbl_time_count.setText(str(current_duration))
            if current_duration >= 8 and not self._flag_3_red_blinks:
                self._flag_3_red_blinks = True
                self._red_led_count = 6
                self._red_led_blink_timer.start(300)
        else:
            self.ui.lbl_time_count.setText('')

        # Clignotement LED verte pendant 4 minutes
        if simulation_duration < 240:
            last_green_blink = timer() - self._green_led_last_blink
            if last_green_blink >= 5:
                self._green_led_count = 2  # La LED doit faire 1 cligno donc 2 changements d'état
                self._green_led_last_blink = timer()
                self._green_led_blink_timer.start(300)

        current_flow = self.flow_meter.flow_measure()
        if current_flow > 0:
            logging.debug(f"current flowrate measure : {str(current_flow)}")

    def on_btn_off_pressed(self):
        self._off_time_pressed = timer()

    def on_btn_off_released(self):
        released_time = timer()
        off_pressed_duration = released_time - self._off_time_pressed
        self._off_time_pressed = None
        logging.debug(f"OFF button released at {str(released_time)} with duration {str(off_pressed_duration)}")
        # Comportement en fonction du temps d'appui du bouton
        if int(off_pressed_duration) >= 8:
            self.lever_trigger()

    def on_serial_parameter_change(self):
        self._serial_settings['PORT'] = self.ui.lineEdit_com_port.text()
        self._serial_settings['BAUDRATE'] = self.ui.spinBox_baudrate.value()

    def green_led_blink(self):
        self._green_led_state = not self._green_led_state
        self.ui.lbl_green_led.setStyleSheet(self._green_led_styles[self._green_led_state])
        self._green_led_count -= 1
        if self._green_led_count <= 0:
            self._green_led_blink_timer.stop()

    def red_led_blink(self):
        self._red_led_state = not self._red_led_state
        self.ui.lbl_red_led.setStyleSheet(self._red_led_styles[self._red_led_state])
        self._red_led_count -= 1
        if self._red_led_count <= 0:
            self._red_led_blink_timer.stop()

    def lever_trigger(self):
        logging.debug("Triggering lever")
        self._timer.stop()
        # TODO détruire flowmeter
        if self.serial_com is not None and self.serial_com.isOpen():
            self.serial_com.stop()

        # Réinitialisation des paramètres
        self._flag_3_red_blinks = False

        # Mise à jour de l'interface
        self.ui.btn_lever.setEnabled(True)
        self.ui.lbl_lever.setText('Levé')
        self.ui.lbl_lever.setStyleSheet(self._lever_styles['Levé'])
        self.ui.lbl_com_status_text.setStyleSheet('background-color: rgb(240, 240, 240);')
        self.ui.lbl_com_status_text.setText('Déconnecté')

    def show(self):
        self.main_win.show()


class FlowMeter:
    def __init__(self):
        self._flowrate = 0

    def flow_measure(self):
        return self._flowrate


if __name__ == "__main__":
    logging.info("Starting Application")
    app = QApplication(sys.argv)

    # Création de l'application
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
