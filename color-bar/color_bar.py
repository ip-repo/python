from random import choice, randint
from time import sleep
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import QRunnable, Slot, QThreadPool
from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThreadPool

class WorkerSignals(QObject):
	change_color = Signal(int)
	

class Worker(QRunnable):
	def __init__(self, sleep_time, *args, **kwargs):
		super(Worker, self).__init__()
		self.signals = WorkerSignals()
		self.sleep_time = sleep_time

	@Slot()
	def run(self):
		while True:
			sleep(self.sleep_time)
			self.signals.change_color.emit(1)

	
class ColorBar(QWidget):
	def __init__(self,colors_list=[], max_labels=10,background_color="white",sleep_time=0.2) -> None:
		super().__init__()
		if sleep_time < 0.0:
			self.sleep_time = 0.2
		else:
			self.sleep_time = sleep_time
		if max_labels < 1:
			max_labels = 1
		self.max_labels = max_labels
		if colors_list:
			self.colors_list = colors_list
		else:
			self.colors_list = ["red","orange","yellow","green","blue","black","white"]
		self.setWindowTitle("Color Bar")
		self.init_ui()
		self.setStyleSheet("background-color: {};".format(background_color))

		
	def init_ui(self):
		self.thread_pool = QThreadPool()
		self.labels = []
		self.la = QVBoxLayout()
		for label_counter in range(self.max_labels):
			new_label = QLabel()
			new_label.setStyleSheet("background-color: {}".format(choice(self.colors_list)))
			self.labels.append(new_label)
			self.la.addWidget(new_label, label_counter)
		self.setLayout(self.la)
		self.worker = Worker(self.sleep_time)
		self.worker.signals.change_color.connect(self.change_labels_colors)
		self.thread_pool.start(self.worker)

	
		
	def change_labels_colors(self,*args):
		for label in self.labels:
			label.setStyleSheet("background-color: {}".format(choice(self.colors_list)))
		
if __name__ == "__main__":
	colors_list = ["red","orange","yellow","green","blue","black","white","cyan"]
	background_color = "red"
	max_labels = 20
	sleep_time = 0.02
	app = QApplication()
	color_bar = ColorBar(colors_list=colors_list,max_labels=max_labels,background_color=background_color,sleep_time=sleep_time)
	color_bar.show()
	app.exec()
