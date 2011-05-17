#!/usr/bin/python
import os
import wx
import sms
import Contacts
import sys
homedir = os.getenv("HOME")
if os.path.isdir(homedir + "/.smss")==False:
	os.system("mkdir " + homedir + "/.smss")
cli_args = sys.argv[1:]
class AddressBook(wx.Frame):
	def __init__(self):
		self.val = ''
		self.uname=''
		self.passw=''
		self.string = ''
		Contacts.read()
		self.contacts = [('','')]
		try:
			self.contacts = Contacts.t.contacts
			self.getgcred()
		except IOError:
			pass
		wx.Frame.__init__(self,None,-1,"Address Book",size=(400,400))
		self.panel = wx.Panel(self)
		wx.StaticText(self.panel,-1,"This is your address Google Address book.\nTo get started, click on File>>'Change Google User' (to import your google contacts). To refresh them, click on File>>Refresh List",pos=(10,10),size=(380,80))
		
		#set_up_ac = wx.Button(self.panel,-1,'Set up account', pos = (150,90), size = (150,30))
		#self.Bind(wx.EVT_BUTTON,self.get,set_up_ac)
		
		#refresh_button = wx.Button(self.panel,-1,"Refresh",pos = (310,90), size = (80,30))
		#self.Bind(wx.EVT_BUTTON,self.cget,refresh_button)
		
		self.clist = wx.CheckListBox(self.panel,-1,(10,130),(380,200),self.lister())
		self.clist.SetSelection(0)
		
		select = wx.Button(self.panel,-1,'OK',pos=(180,340),size=(100,27))
		self.Bind(wx.EVT_BUTTON,self.sel, select)
		
		canc = wx.Button(self.panel,-1,'Cancel',pos=(290,340),size=(100,27))
		self.Bind(wx.EVT_BUTTON,self.exit,canc)
		
		select_all = wx.Button(self.panel,-1,'Select All',pos=(180,100), size = (100,25))
		self.Bind(wx.EVT_BUTTON,self.selectall,select_all)
		
		select_none = wx.Button(self.panel,-1,'Select None',pos = (290,100), size = (100,25))
		self.Bind(wx.EVT_BUTTON,self.selectnone,select_none)
		
		self.clist.Bind(wx.EVT_KEY_DOWN,self.key_press)
		
		self.search_text = wx.StaticText(self.panel,-1,'',pos=(10,350),size=(100,30))
		
		self.Bind(wx.EVT_CLOSE,self.close_event)
		
		##Menubar##:
		self.menubar = wx.MenuBar()
		
		#FileMenu
		self.filemenu = wx.Menu()
		
		#Refresh
		refresh_menuitem = self.filemenu.Append(-1,"Refresh List","Refresh your Google contacts list from your Google account")
		self.Bind(wx.EVT_MENU,self.cget,refresh_menuitem)
		
		#Set up account
		sua_menuitem = self.filemenu.Append(-1,"Change Google user","Set up Google contacts sync account")
		self.Bind(wx.EVT_MENU,self.get,sua_menuitem)
		
		self.menubar.Append(self.filemenu,"File")
		self.SetMenuBar(self.menubar)
		
		self.set_checked()
	def selectall(self,ev):
		x = 0
		while x < len(self.contacts):
			self.clist.Check(x,True)
			x += 1
	def selectnone(self,ev):
		x = 0
		while x < len(self.contacts):
			self.clist.Check(x,False)
			x += 1
	def set_checked(self):
		tstring = fframe.recipent.GetValue()
		print tstring
		if len(tstring) == 0:
			return
		if tstring[-1]==',':
			tstring = tstring[:-1]
		tstring2 = tstring.split(",")
		for x in tstring2:
			x = x[x.find(")")+1:]
			no = 0
			no2 = 0
			while no < len(self.contacts):
				y = self.contacts[no][1]
				yy = ""
				for a in y:
					if a in "1234567890":
						yy += a
				if x in yy:
					no = len(self.contacts)
				else:
					no += 1
					no2 += 1
			self.clist.Check(no2,True)
	def close_event(self,ev):
		self.MakeModal(False)
		self.Destroy()
	def key_press(self,ev):
		self.keylist = ['']
		print "hey pressed!!"
		keycode = ev.GetKeyCode()
		if keycode==wx.WXK_DOWN:
			self.clist.SetSelection(self.clist.GetSelection()+1)
			return
		elif keycode==wx.WXK_UP:
			if self.clist.GetSelection()>0:
				self.clist.SetSelection(self.clist.GetSelection()-1)
			return
		elif keycode==wx.WXK_HOME or keycode == wx.WXK_NUMPAD_HOME:
			self.clist.SetSelection(0)
			return
		elif keycode==wx.WXK_END or keycode == wx.WXK_NUMPAD_END:
			self.clist.SetSelection(len(self.contacts)-1)
			return
		elif keycode==wx.WXK_ESCAPE:
			self.val = ''
			self.search_text.SetLabel(self.val)
			return
		elif keycode==wx.WXK_SPACE:
			if self.clist.IsChecked(self.clist.GetSelection()):
				self.clist.Check(self.clist.GetSelection(),False)
			else:
				self.clist.Check(self.clist.GetSelection(),True)
			return
		elif keycode==wx.WXK_BACK:
			self.val=self.val[0:-1]
			self.search_text.SetLabel(self.val)
			return
		elif keycode==wx.WXK_RETURN or keycode==wx.WXK_NUMPAD_ENTER:
			self.sel(1)
		if keycode >= 65 and keycode <= 91:
			self.keylist = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
			keycode -= 65
			print self.keylist[keycode]
		elif keycode >= 48 and keycode <= 57:
			keycode -= 48
			self.keylist = ['0','1','2','3','4','5','6','7','8','9']
		else:
			return
		x = self.keylist[keycode]
		y = 0
		b = False
		self.val += x
		self.search_text.SetLabel(self.val)
		while y < len(self.contacts):
			if self.contacts[y][0].capitalize().find(self.val.capitalize())==0:
				self.clist.SetSelection(y,True)
				return
#			else:
#				self.SetSelection(y,False)
			y +=1
	def storegcred(self):
		if os.path.exists(homedir+"/.smss/gcred")==False:
			f = open(homedir+"/.smss/gcred","a")
			f.close()
		f = open(homedir + "/.smss/gcred","w")
		f.writelines([self.uname + '\n',self.passw])
		f.close()
	def getgcred(self):
		if os.path.exists(homedir + "/.smss/gcred") == False:
			self.uname = ''
			self.passw = ''
		else:
			f = open("" + homedir + "/.smss/gcred","r")
			a = f.readlines()
			a[0].replace('\n','')
			if len(a) < 2:
				return
			self.uname = a[0]
			self.passw = a[1]
	def sel(self,ev):
		x = self.clist.GetChecked()
		print x
		self.string = ''
		for y in x:
			if len(self.string)>0:
				self.string += ','
			temp = self.clist.GetString(y).split(":\t")
			temp2 = temp[1]
			if temp2[0]=='0':
				temp2 = temp2[1:]
			if '+91' in temp2:
				temp2 = temp2[3:]
			temp3 = ''
			for c in temp2:
				if c in ['1','2','3','4','5','6','7','8','9','0']:
					temp3 += c	
			temp3 = temp3[len(temp3)-10:]
			self.string += '(' + temp[0] + ')' + temp3
		print self.string
		fframe.ref()
		self.exit(1)
	def getstr(self):
		return self.string
	def exit(self,ev):
		self.close_event(1)
		return
	def lister(self):
		a = ['']
		for x in self.contacts:
			if a[0] == '':
				a = [x[0]+ ":\t" + x[1]]
			else:
				a += [x[0] + ":\t" + x[1]]
		return a
	def get(self,evt):
		uname = ''
		while len(uname) == 0:
			tdlg = wx.TextEntryDialog(None,"Enter your google email (for eg: someone@something.com)","Enter email","")
			if tdlg.ShowModal()<>wx.ID_OK:
				return False
			uname = tdlg.GetValue()
			tdlg.Destroy()
		passw = ''
		while len(passw) == 0:
			tdlg = wx.TextEntryDialog(None,"Enter your passowrd","Password","",style= wx.TE_PASSWORD | wx.OK | wx.CANCEL)
			if tdlg.ShowModal()<>wx.ID_OK:
				return False
			passw = tdlg.GetValue()
			tdlg.Destroy()
		self.uname = uname
		self.passw = passw
		self.cget(1)
		cdlg = wx.MessageDialog(None,"Do you want to store google " + homedir + "/.smss/credentials?","Save " + homedir + "/.smss/credentials?",style=wx.YES_NO)
		if cdlg.ShowModal()==wx.ID_YES:
			self.storegcred()
	def cget(self,ev):
		Contacts.get(self.uname,self.passw)
		Contacts.write()
		self.contacts = Contacts.t.contacts
		self.clist.Clear()
		self.clist.InsertItems(self.lister(),0)
class MyFrame(wx.Frame):
	def __init__(self):
		self.temp2 = False
		yy = ['','']
		try:
			self.unlock()
			f = open(homedir + "/.smss/cred","r")
			yy = f.readlines()
			yy[0] = yy[0].replace('\n','')
			yy[1] = yy[1].replace('\n','')
			self.lock()
		except Exception:
			yy = ['','']
		wx.Frame.__init__(self,None,-1,"sms-bot",size=(400,370))
		panel = wx.Panel(self)
		wx.StaticText(panel,-1,"Your Number:",pos=(10,10))
		self.user = wx.TextCtrl(panel,-1,yy[0],size=(210,30),pos=(180,5))
		
		wx.StaticText(panel,-1,"Your password:",pos=(10,70))
		self.password = wx.TextCtrl(panel,-1,yy[1],size=(210,30),pos=(180,65),style=wx.TE_PASSWORD)
		
		wx.StaticText(panel,-1,"Recipents Number:",pos=(10,130))
		self.recipent = wx.TextCtrl(panel,-1,"",size=(210,30),pos=(180,125))
		
		wx.StaticText(panel,-1,'Message:',pos=(10,190))
		self.message = wx.TextCtrl(panel,-1,"",size=(210,100),pos=(180,185),style=wx.TE_MULTILINE)
		
		#wx.StaticText(panel,-1,'Number of messages to send:',pos=(10,270))
		
		#self.number_of_times = wx.SpinCtrl(panel,-1,pos=(295,265), min=1, max=20)
		
		ok = wx.Button(panel,-1,"SEND",pos=(10,310),size=(80,30))
		cancel = wx.Button(panel,-1,"CANCEL",pos=(315,310),size=(75,30))
		
		add_book = wx.Button(panel,-1,"Choose from address book", pos = (97,310), size = (211,30))
		
		self.Bind(wx.EVT_TEXT,self.setlimit,self.message)
		self.Bind(wx.EVT_BUTTON,self.sendmsg,ok)
		self.Bind(wx.EVT_BUTTON,self.exit,cancel)
		self.Bind(wx.EVT_BUTTON,self.address_book,add_book)
		self.Bind(wx.EVT_MIDDLE_DCLICK, self.refresh)
		self.Show()
		
		#Condenser
		self.exceed = wx.StaticText(panel,-1,"Character Limit Exceeded",pos=(10,220),size=(150,30))
		self.exclamation_button = wx.Button(panel,-1,"?",pos=(153,215),size=(20,25))
		self.Bind(wx.EVT_BUTTON,self.oh_no,self.exclamation_button)
		self.exclamation_button.Hide()
		self.exceed.Hide()
		#Click to condense text
		self.condense_button = wx.Button(panel,-1,"Condense",pos=(10,255),size=(163,30))
		self.Bind(wx.EVT_BUTTON,self.condense_text,self.condense_button)
		self.condense_button.Hide()
		
		
		#Menubar
		self.menubar = wx.MenuBar()
		
		#FileMenu
		file_menu = wx.Menu()
		
		#GlobalMenuSupport_MenuItem
		gmsupport_menuitem = file_menu.Append(-1,"Global Menu Support","Enable/Disable Global menu support")
		self.Bind(wx.EVT_MENU,self.global_menu_support,gmsupport_menuitem)
		
		#ResetMenuItem
		reset_menuitem = file_menu.Append(-1,"Reset All Settings","Reset all settings to their defaults. This includes saved password and contacts")
		self.Bind(wx.EVT_MENU,self.reset,reset_menuitem)
		
		#ExitMenuItem
		exit_menuitem = file_menu.Append(-1,"Exit","Exit this application")
		self.Bind(wx.EVT_MENU,self.exit,exit_menuitem)
		
		self.menubar.Append(file_menu,"File")
		
		#Help Menu
		help_menu = wx.Menu()
		
		#About
		about_menuitem = help_menu.Append(-1,"About","About this application")
		
		self.menubar.Append(help_menu, "Help")
		self.Bind(wx.EVT_MENU,self.about,about_menuitem)
		self.SetMenuBar(self.menubar)
		self.menubar.Hide()
		
		if os.path.exists(homedir+"/.smss/.gmsupport") == False:
			f = open(homedir+"/.smss/.gmsupport","a")
			f.close()
			self.global_menu_support(1)
		else:
			f = open(homedir+"/.smss/.gmsupport","r")
			if f.read()=="yes":
				self.SetSize((400,350))
			f.close()
		try:
			self.SetIcon(wx.Icon("/usr/share/pixmaps/smss.png",wx.BITMAP_TYPE_PNG))
		except:
			pass
	def about(self,ev):
		license = """ Copyright (C) 2011  Rishav Thakker

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

For more information, see http://www.gnu.org/licenses """
		info = wx.AboutDialogInfo()
		info.SetName("SMSS")
		info.SetVersion("0.2")
		info.SetDescription("A simple application to send free SMSs via the Way2SMS Portal.")
		info.SetCopyright("(c) Rishav Thakker")
		info.SetLicence(license)
		info.SetWebSite("http://rishavt.github.com/smss")
		info.AddDeveloper("Rishav Thakker")
		try:
			info.SetIcon(wx.Icon("/usr/share/smss/icon.png", wx.BITMAP_TYPE_PNG))
		except:
			pass
		wx.AboutBox(info)
	def global_menu_support(self,ev):
		f = open(homedir+"/.smss/.gmsupport","r")
		x = f.read()
		f.close()
		if x <> "yes":
			msg = wx.MessageDialog(None,"Global menu support is disabled. Do you want to enable it? (If you're using Unity, select yes)","Global Menu support",wx.YES_NO)
			if msg.ShowModal() == wx.ID_YES:
				f = open(homedir+"/.smss/.gmsupport","w")
				f.write("yes")
				f.close()
				self.SetSize((400,350))
		else:
			msg = wx.MessageDialog(None,"Global menu support is enabled. Do you want to disable it?","Global Menu support",wx.YES_NO)
			if msg.ShowModal() <> wx.ID_NO:
				f = open(homedir+"/.smss/.gmsupport","w")
				f.write("no")
				f.close()
				self.SetSize((400,370))
		
	def reset(self,ev):
		msg = wx.MessageDialog(None,"Are you sure you want to reset all settings? This will delete all saved password and contacts.","Are you sure")
		if msg.ShowModal()==wx.ID_OK:
			msg.Destroy()
			os.system("rm -R ~/.smss")
			self.Hide()
			wx.Yield()
			os.system("smss")
			self.Destroy()
		else:
			msg.Destroy()
	def exit(self,ev):
		self.Destroy()
	def oh_no(self,ev):
		msg = wx.MessageDialog(None,"Character limit of 140 exceeded! Click 'Condense' to condense the text. If you send a message exceeding the character limit, it will be sent as 2 messages","Note")
		msg.ShowModal()
		msg.Destroy()
	def condense_text(self,ev):
		text = self.message.GetValue()
		f = open(homedir+"/.smss/.abbreviations","r")
		temp = f.read().split("\n")
		arr = [("","")]
		for x in temp:
			y = x.split(" ")
			if len(y)>1:
				if len(arr)==1:
					arr = [(y[0],y[1])]
				else:
					arr += [(y[0],y[1])]
		f.close()
		f = open(homedir + "/.smss/.num_abbreviations","r")
		temp = f.read().split("\n")
		num_arr = [("","")]
		for x in temp:
			y = x.split(" ")
			if len(y)>1:
				if len(num_arr)==1:
					num_arr = [(y[0],y[1])]
				else:
					num_arr += [(y[0],y[1])]
#		arr = [('and','&'),('to','2'),('for','4'),('this','dis'),('how','hw'),('. ','.'),(', ',','),('! ','!'),('= ','='),('plus','+'),('once','1ce'),('wonder','1der'),('thanks','thnx'),('tomorrow','2mrw'),('tonight','2nite'),('from','frm'),('what','wat'),('thank you','thnq'),('between','b/w'),('by the way','btw'),('without','w/o'),('anyone','any1'),('you','u'),('see','c'),('come on','cmon'),('love','luv'),('am','m'),('for your information','FYI'),('the','d')]
#		num_arr = [('two','twenty'),('three','thirty'),('four','forty'),('five','fifty'),('six','sixty'),('seven','seventy'),('eight','eighty'),('nine','ninety')]
		text = text.replace('one','1')
		y = 1
		for x in num_arr:
			y += 1
			print x[0]
			text=text.replace(x[0],str(y))
		for x,y in arr:
			text = text.replace(x,y)
		te = wx.TextEntryDialog(None,"Your text has been condensed to the following (Still " + str(len(text)-140) + " characters over limit). Press OK to confirm","Confirm",str(text),style=wx.TE_MULTILINE|wx.TE_READONLY|wx.OK|wx.CANCEL)
		if te.ShowModal() == wx.ID_OK:
			self.message.SetValue(text)
		te.Destroy()
	def refresh(self,ev):
		self.temp2 = False
		print "reset\n"
	def address_book(self,ev):
		self.adb = AddressBook()
		self.adb.Show()
		self.adb.MakeModal(True)
	def ref(self):
		self.recipent.SetValue(self.adb.getstr())
	def setlimit(self,ev):
		s = self.message.GetValue()
		if len(s) > 140:
			self.exclamation_button.Show()
			self.exceed.Show()
			self.condense_button.Show()
		else:
			self.exclamation_button.Hide()
			self.exceed.Hide()
			self.condense_button.Hide()
	def sendmsg(self,ev):
		if os.path.exists(homedir + "/.smss/cred") == False:
			a = wx.MessageDialog(None,"Do you want us to remember your way2sms number + password?","Remember " + homedir + "/.smss/credentials")
			if a.ShowModal()==wx.ID_OK:
				self.unlock()
				if os.path.exists(homedir+"/.smss/cred")==False:
					f = open(homedir+"/.smss/cred","a")
					f.write("")
					f.close()
				f = open(homedir + "/.smss/cred","w")
				f.write(self.user.GetValue() + "\n" + self.password.GetValue())
				f.close()
				self.lock()
		true = 0
		false = 0
		
		templist = self.recipent.GetValue().split(',')
		for xy in templist:
			if xy[0]=='(':
				xy = xy[xy.find(')')+1:]
			print "..." + xy
			if self.temp2 == False:
				self.temp2 = sms.login(self.user.GetValue(),self.password.GetValue())
			message=[""]
			message_body = self.message.GetValue()
			while len(message_body)>0:
				message += [message_body[:140]]
				message_body = message_body[140:]
			for x in message:
				if x <> "":
					temp = sms.send(xy,x,self.temp2)
			if temp:
				true+=1
			else:
				false+=1
		a = wx.MessageDialog(None,"Sent " + str(true) + " out of " + str(false+true),"Sent",wx.OK)
		a.ShowModal()
		a.Destroy()
		self.temp2=False
	def lock(self):
		pass
	def unlock(self):
		pass
	def exit(self,ev):
		self.Destroy()
		wx.Exit()
if __name__=='__main__':
	if os.path.exists(homedir + "/.smss/.abbreviations") == False or os.path.exists(homedir + "/.smss/.num_abbreviations") ==False:
		os.system("cp /usr/share/smss/.*abbreviations " + homedir + "/.smss")
	app = wx.PySimpleApp()
	fframe = MyFrame()
	app.MainLoop()
