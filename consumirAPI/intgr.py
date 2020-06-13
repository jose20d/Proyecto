from gi.repository import Gtk
import configparser
import consapi

def buscaDir(buttom):
	txtCodB = builder.get_object("txtCodB")
	lblDir = builder.get_object("lblDir")
	direc = consapi.buscadir(config["URL"]["codpostal"], txtCodB.get_text())
	lblDir.set_text(direc)

def agreProv():	
	cbxPro = builder.get_object("cbxPro")
	listaC = Gtk.ListStore(str)
	lista = consapi.listapro(config["URL"]["provincias"])
	for i in range(len(lista)):
		listaC.append([lista[i]])
	cbxPro.set_model(listaC)
	render = Gtk.CellRendererText()
	cbxPro.pack_start(render, True)
	cbxPro.add_attribute(render, "text", 0)

def cbxProC(combo):
	lblDir = builder.get_object("lblDir")
	cbxPro = builder.get_object("cbxPro")
	model = cbxPro.get_model()
	pro = cbxPro.get_active()
	lblDir.set_text(model[pro][0])
	nom = (model[pro][0])
	#codpro = consapi.buscadir(config["URL"]["codpro"], nom)
	#return(codpro)

config = configparser.ConfigParser()
config.read('consapi.ini')

builder = Gtk.Builder()
builder.add_from_file("intCons.glade")
handlers = {
	"end_app": Gtk.main_quit,
	"on_btnBuscarDir_clicked":buscaDir,
	"on_cbxPro_changed":cbxProC
}

builder.connect_signals(handlers)
window = builder.get_object("frmPadron")
window.show_all()
agreProv()

Gtk.main()
