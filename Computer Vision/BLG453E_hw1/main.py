import ui
import sys

if __name__ == '__main__':
    app = ui.QApplication(sys.argv)
    ex = ui.UI()
    sys.exit(app.exec_())
    