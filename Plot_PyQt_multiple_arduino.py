import sys
import serial
import numpy as np
import pandas as pd
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import struct
import time

class RealTimePlot(QMainWindow):
    def __init__(self, command_port, data_ports, baud_rate=115200, num_signals=8, num_points=100, update_interval=10):
        super().__init__()

        # Serial port settings
        self.command_port = command_port
        self.data_ports = data_ports
        self.baud_rate = baud_rate
        self.num_signals = num_signals
        self.num_points = num_points
        self.update_interval = update_interval  # ms
        self.paused = False
        self.data = np.zeros((self.num_signals, self.num_points))
        self.log_data = []

        # Open serial connections
        self.command_serial = self.open_serial_port(self.command_port)
        self.data_serials = [self.open_serial_port(port) for port in self.data_ports]
        time.sleep(2)

        # Create CSV file with timestamp
        self.csv_filename = f"data_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # Set up UI
        self.init_ui()

        # Set up timer for real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(self.update_interval)
        self.timer.setInterval(max(self.update_interval - 1, 1))

        self.end_timer = QTimer()
        self.end_timer.timeout.connect(self.close)
        self.end_timer.start(60000)

    def open_serial_port(self, port):
        """Open a serial port and return the Serial object."""
        try:
            ser = serial.Serial(port, self.baud_rate, timeout=0.5)
            return ser
        except Exception as e:
            print(f"⚠️ Error opening {port}: {e}")
            return None

    def send_command(self, command):
        """Send a command to the command Arduino (before receiving data)."""
        if self.command_serial:
            try:
                self.command_serial.write(str(command).encode('utf-8'))
            except Exception as e:
                print(f"!!! Failed to send command: {e}")

    def read_serial_data(self):
        """Read data from multiple Arduino devices."""
        new_data = np.zeros(self.num_signals)
        for i, ser in enumerate(self.data_serials):
            if i == 0 :
                try:
                    if ser and ser.in_waiting >= 8:
                        new_data[i * 4:(i + 1) * 4] = [(v/1000.0) - 10 for v in struct.unpack('<HHHH', ser.read(8))]
                except Exception as e:
                    print(f"⚠️ Serial read error: {e}")
            elif i == 1 :
                try:
                    if ser and ser.in_waiting >= 8:
                        new_data[i * 4:(i + 1) * 4] = [(v/1000.0) - 10 for v in struct.unpack('<HHHH', ser.read(8))]
                except Exception as e:
                    print(f"!!! Serial read error: {e}")
        return new_data

    def update_plot(self):
        """Update the plot with new data and save it automatically."""
        if self.paused:
            return

        whole_data = np.zeros(self.num_signals)
        for i in range(1,3) :
            # Send Command to turn on LED
            self.send_command(i)

            # 5ms delay
            init_time = time.perf_counter()
            while (time.perf_counter() - init_time) <= 0.005 :
                pass

            # Receive data
            whole_data[(i-1)*4:i*4] = self.read_serial_data()[(i-1)*4:i*4]

            # Send command to turn off LED
            self.send_command(i)

            # 5ms delay
            init_time = time.perf_counter()
            while (time.perf_counter() - init_time) <= 0.005 :
                pass

        # Shift and update data
        self.data = np.roll(self.data, -1, axis=1)
        self.data[:, -1] = whole_data

        # Update plots
        self.line_1_1[0].setData(np.arange(self.data.shape[1]) * self.update_interval / 1000, self.data[0])
        self.line_1_2[0].setData(np.arange(self.data.shape[1]) * self.update_interval / 1000, self.data[1])
        self.line_1_3[0].setData(np.arange(self.data.shape[1]) * self.update_interval / 1000, self.data[2])
        self.line_1_4[0].setData(np.arange(self.data.shape[1]) * self.update_interval / 1000, self.data[3])

        self.line_2_1[0].setData(np.arange(self.data.shape[1]) * self.update_interval / 1000, self.data[4])
        self.line_2_2[0].setData(np.arange(self.data.shape[1]) * self.update_interval / 1000, self.data[5])
        self.line_2_3[0].setData(np.arange(self.data.shape[1]) * self.update_interval / 1000, self.data[6])
        self.line_2_4[0].setData(np.arange(self.data.shape[1]) * self.update_interval / 1000, self.data[7])

        # Log data
        self.log_data.append([time.perf_counter()] + whole_data.tolist())

        if time.perf_counter() >= 60 :
            self.close()

    def toggle_pause(self):
        """Pause or resume plotting."""
        self.paused = not self.paused
        self.pause_btn.setText("Resume" if self.paused else "Pause")

    def init_ui(self):
        """Initialize PyQt UI."""
        self.setWindowTitle("Real-Time Arduino Data Plot")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # PyQtGraph plot
        self.pd_1_1 = pg.PlotWidget(title="1-1")
        self.pd_1_2 = pg.PlotWidget(title="1-2")
        self.pd_1_3 = pg.PlotWidget(title="1-3")
        self.pd_1_4 = pg.PlotWidget(title="1-4")

        self.pd_2_1 = pg.PlotWidget(title="2-1")
        self.pd_2_2 = pg.PlotWidget(title="2-2")
        self.pd_2_3 = pg.PlotWidget(title="2-3")
        self.pd_2_4 = pg.PlotWidget(title="2-4")

        grid_layout.addWidget(self.pd_1_1, 0, 0)
        grid_layout.addWidget(self.pd_1_2, 1, 0)
        grid_layout.addWidget(self.pd_1_3, 2, 0)
        grid_layout.addWidget(self.pd_1_4, 3, 0)
        grid_layout.addWidget(self.pd_2_1, 0, 1)
        grid_layout.addWidget(self.pd_2_2, 1, 1)
        grid_layout.addWidget(self.pd_2_3, 2, 1)
        grid_layout.addWidget(self.pd_2_4, 3, 1)

        layout.addLayout(grid_layout)

        self.line_1_1 = [self.pd_1_1.plot(pen=pg.intColor(0, 4))]
        self.line_1_2 = [self.pd_1_2.plot(pen=pg.intColor(1, 4))]
        self.line_1_3 = [self.pd_1_3.plot(pen=pg.intColor(2, 4))]
        self.line_1_4 = [self.pd_1_4.plot(pen=pg.intColor(3, 4))]
        
        self.line_2_1 = [self.pd_2_1.plot(pen=pg.intColor(0, 4))]
        self.line_2_2 = [self.pd_2_2.plot(pen=pg.intColor(1, 4))]
        self.line_2_3 = [self.pd_2_3.plot(pen=pg.intColor(2, 4))]
        self.line_2_4 = [self.pd_2_4.plot(pen=pg.intColor(3, 4))]

        # Buttons
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.toggle_pause)
        layout.addWidget(self.pause_btn)

        # Set main widget
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def closeEvent(self, event):
        """Close serial connections on exit."""
        df = pd.DataFrame(self.log_data, columns=["Time[s]"] + [f"Signal_{i+1}" for i in range(self.num_signals)])
        df.to_csv(self.csv_filename, index=False)
        print(f'Data is saved in {self.csv_filename}')

        if self.command_serial:
            self.command_serial.close()
        for ser in self.data_serials:
            if ser:
                ser.close()
        event.accept()

if __name__ == "__main__":
    command_port = "COM3"
    data_ports = ["COM4", "COM8"]

    app = QApplication(sys.argv)
    window = RealTimePlot(command_port, data_ports)
    window.show()
    sys.exit(app.exec_())
