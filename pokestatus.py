from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject as gobject

from bs4 import BeautifulSoup

import signal, os
import thread
import requests

class PokemonGoIndicator:
	APPINDICATOR_ID = 'myappindicator'
	indicator = None
	icon = 'icons/w/pokedown.png'

	def __init__(self, indicator_id='myappindicator'):
		self.APPINDICATOR_ID = indicator_id

		self.indicator = appindicator.Indicator.new( self.APPINDICATOR_ID, 'whatever', appindicator.IndicatorCategory.SYSTEM_SERVICES)
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

		# Set Menu
		menu = gtk.Menu()
		item_quit = gtk.MenuItem('Quit')
		item_quit.connect('activate', self.quit)
		menu.show_all()
		self.indicator.set_menu( menu )


		self.update_server_status_icon()

		signal.signal( signal.SIGINT, signal.SIG_DFL )

		gtk.main()

	def set_icon(self, icon_path):
		self.icon = os.path.dirname(os.path.realpath(__file__)) + '/' + icon_path

	def get_icon(self):
		print self.icon
		return self.icon

	def quit(self, source):
		gtk.main_quit()

	def update_server_status_icon(self):
		URL = 'http://cmmcd.com/PokemonGo/'

		try:
			r = requests.get( URL )
			soup = BeautifulSoup( r.text, 'html.parser' )
			status = soup.body.header.h2.font.text
		except:
			status = False

		if status == 'Online!':
			self.set_icon( 'icons/w/pokeok.png' )
		elif status == 'Unstable!':
			self.set_icon( 'icons/w/pokeunstable.png' )
		elif status == 'Offline!':
			self.set_icon( 'icons/w/pokedown.png' )

		self.change_app_icon()

	def change_app_icon(self):
		self.indicator.set_icon( self.get_icon() )
		gobject.timeout_add_seconds( 60, self.update_server_status_icon )

if __name__ == '__main__':
	ap = PokemonGoIndicator('pokemongoindicator')
