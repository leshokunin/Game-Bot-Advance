from PyQt5 import QtWidgets
import sys
from ScreenshotWidget import ScreenshotWidget

app = QtWidgets.QApplication(sys.argv)
window = ScreenshotWidget()
window.show()
app.aboutToQuit.connect(app.deleteLater)
sys.exit(app.exec_())
