#!/usr/bin/python
#-*-coding:utf-8-*-
#- usb-rubber-ducky-manager Class

#- Copyright (C) 2014 GoldraK & Interhack 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 
# You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>


class add(object):
	#- @output.[option](default, error)(text) -> printed by stdout
	#- @translate.[option](init('nameTranslate')) -> initializes the translation file
	#- @log.[option](write)(text,*1) -> 1 is error -> saves information in the logs
	#- @installer -> module for install dependencies -> nonoperating

	def __init__(self, output, translate, log, installer,options):
		#- imports necessary
		import sys, os, ConfigParser
		from teco import color, style
		sys.path.append('modules/usb-rubber-ducky-manager/Encoder')
		from Encoder import Encoder

		self.directories = []
		self.files = []
		self.dir_before = []
		#- Operations
		#- Example:
		output.default('Usb Rubber Ducky Manager')
		def __menu__(path = ''):
			root_path = 'modules/usb-rubber-ducky-manager/apps/'
			self.directories,self.files = list_dir_file(root_path+path)
			c = 1
			for d in self.directories:
				print color('magenta', str(c)+" - "+d)
				c+=1
			for f in self.files:
				print color('azul', str(c)+" - "+f) 
				c+=1



		def list_dir_file(root_path):
			files = []
			directories = []
			for f in os.listdir(root_path):
				check = root_path+"/"+f
				if os.path.isfile(check):
					files.append(f)
				elif os.path.isdir(check):
					directories.append(f)
			return directories, files


		def option1():
			output.default('Has seleccionado la opcion 1')
		
		def option2():
			output.default('Has seleccionado la opcion 2')
		
		__menu__()

		control = True
		while control == True:
			options.set_completer(help.complete)
			cadena = ""
			for x in self.dir_before:
				cadena = cadena+" "+x
			sentencia = raw_input("Usb Rubber Ducky Manager "+cadena+" >> ")
			if sentencia == 'exit':
				sys.exit()
			elif sentencia == 'version':
				output.default(help.version())
			elif sentencia == 'menu' or sentencia == 'ls':
				dir_extend = ""
				for d in self.dir_before:
					dir_extend = dir_extend + d + "/"
				__menu__(dir_extend)
			elif sentencia == 'help':
				output.default(help.help())
			elif int(sentencia) == 0:
				dir_extend = ""
				if len(self.dir_before) != 0:
					self.dir_before.remove(self.dir_before[-1])
					for j in self.dir_before:
						dir_extend = dir_extend + j + "/" 
				__menu__(dir_extend)	
			elif (int(sentencia) <= len(self.directories)) and (int(sentencia)>0):
				self.dir_before.append(self.directories[int(sentencia)-1])
				dir_extend = ""
				for d in self.dir_before:
					dir_extend = dir_extend + d + "/"
				__menu__(dir_extend)
			elif (int(sentencia) > len(self.directories)) and (int(sentencia) <= (len(self.directories)+len(self.files))):
				dir_extend = ""
				for d in self.dir_before:
					dir_extend = dir_extend + d + "/"
				print 'modules/usb-rubber-ducky-manager/apps/'+dir_extend+self.files[int(sentencia)-len(self.directories)-1]
				duck_path = 'modules/usb-rubber-ducky-manager/apps/'+dir_extend+self.files[int(sentencia)-len(self.directories)-1]
				config = ConfigParser.ConfigParser()
				if not config.read(duck_path):
					output.default("No existe el archivo de instalación")
					sys.exit()
				else:
					print color('magenta', "1 - Information Script")
					print color('azul', "2 - Compile Script")
					option = raw_input("Usb Rubber Ducky Manager >> ")
					while option == "":
						option = raw_input("Usb Rubber Ducky Manager >> ")
					if option == "1":
						title = config.get('info','title')
						description = config.get('info','description')
						print color('rojo', "Title:")
						print title
						print color('rojo', "Description:")
						print description
					elif option == "2":
						delimiter = config.get('delimiter','key')
						duck_script = config.get('script_command','cuak')
						data = config.items('data')
						for x in data:
							new_string = raw_input("usb-rubber-ducky-manager - "+x[1]+" >> ")
							old_string =delimiter+x[0]+delimiter
							duck_script = duck_script.replace(old_string,new_string)
						print duck_script
						commands = duck_script.split('\n')
						path = 'modules/usb-rubber-ducky-manager/precompile/apps/'+dir_extend
						path_compile = 'modules/usb-rubber-ducky-manager/compile/apps/'+dir_extend
						file_save = path+self.files[int(sentencia)-len(self.directories)-1]
						file_save_compile = path_compile+self.files[int(sentencia)-len(self.directories)-1].split(".")[0]+".bin"
						if not os.path.exists(path):
							os.makedirs(path)
						if not os.path.exists(path_compile):
							os.makedirs(path_compile)
						log = open(file_save, 'w')
						for x in commands:
							log.write(x)
							log.write("\n")
						log.close()
						encoder_rubber = Encoder()
						encoder_rubber.compile(['encoder','-i',file_save,'-o',file_save_compile])
					else:
						output.default('No ha seleccionado una opcion correcta')	
			else:
				output.default('No ha seleccionado una opcion correcta')

class help(object):
	#- Commands default
	@staticmethod
	def complete(text, state):
		possibilities = ["exit", "version", "help"]
		results = [x for x in possibilities if x.startswith(text)] + [None]
		return results[state]

	#- Help for menu
	@staticmethod
	def help(translate=''):
		return "Help Module"

	@staticmethod
	def version(translate=''):
		return "Version 0.1"

	@staticmethod
	#- @translate.[option](init('nameTranslate')) -> initializes the translation file
	def info(translate):
		return 'NewModule Example Hello World'

	@staticmethod
	#- Especificamos si necesita el modulo paquetes adicionales.
	def package():
		#- List of extra dependencies needed by the module
		additionalPackage = []
		return additionalPackage