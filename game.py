import os


def main():
	try:
    	from lib.SuperTTT import *
	except ImportError:
		out = os.system('sudo apt-get install python-qt4')
	    if out != 0:
	    	print "######## ERROR #########"
	    	print "##  EXECUTE WITH SUDO ##"
	    	print "########################"
	    	raise EOFError

	    from lib.SuperTTT import *

    app = QtGui.QApplication(sys.argv)
    SuperTTT = SuperTicTacToe()
    sys.exit(app.exec_())

main()
