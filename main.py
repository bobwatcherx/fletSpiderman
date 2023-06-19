from flet import *
from pocketbase import PocketBase 
import random
from datetime import datetime

client = PocketBase('https://boundless-nail.pockethost.io')

def main(page:Page):
	page.window_width = 300
	page.scroll = "auto"
	productList = Column(visible=True)
	datainvoice = Column(scroll="auto")
	barangmasuklist = Column(scroll="auto")
	barangkeluarout = Column(scroll="auto")
	seelistinhistory = Column(visible=False)
	seelistouthistory = Column(visible=False)
	page.client_storage.remove("userlog")
	mysnack = SnackBar(content=Text())


	def changeregister(e):
		if e.control.value == True:
			ct_login.content.controls[0].controls[0].value = "Register Now"
			ct_login.content.controls[2].visible = True
			ct_login.content.controls[4].visible = False
			ct_login.content.controls[5].visible = True
		else:
			ct_login.content.controls[0].controls[0].value = "Login User"
			ct_login.content.controls[2].visible = False
			ct_login.content.controls[4].visible = True
			ct_login.content.controls[5].visible = False
		page.update()

	def registernow(e):
		print("3231",ct_login.content.controls[1].value)
		try:
			data = {
				"username": ct_login.content.controls[1].value,
			    "email": ct_login.content.controls[2].value,
			    "emailVisibility": True,
			    "password": ct_login.content.controls[3].value,
			    "passwordConfirm": ct_login.content.controls[3].value,
			    "name": ct_login.content.controls[1].value
			}
			res = client.collection("users").create(data)
			page.snack_bar = SnackBar(
				content=Text("User Created",size=20,color="white"),
				bgcolor="green"
				)
			page.snack_bar.open = True
			ct_login.content.controls[1].value = ""
			ct_login.content.controls[2].value = ""
			ct_login.content.controls[3].value = ""
			ct_login.content.controls[0].controls[0].value = "Login User"
			ct_login.content.controls[2].visible = False
			ct_login.content.controls[4].visible = True
			ct_login.content.controls[5].visible = False
			ct_login.content.controls[6].value = False
		except Exception as e:
			print(e)
			page.snack_bar = SnackBar(
				content=Text(e,size=20,color="white"),
				bgcolor="red"
				)
			page.snack_bar.open = True
		page.update()

	def loginnow(e):
		try:
			login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
			page.snack_bar = SnackBar(
				content=Text("Success Login",size=25,color="white"),
				bgcolor="green"
				)
			ct_login.visible = False
			ct_dashboard.visible = True
			page.snack_bar.open = True
			setkey = page.client_storage.set("userlog", ct_login.content.controls[1].value)
			# LOAD DATA
			getproductlist()
			getinvoicedata()
			getforincoming()
			getforoutgoing()
			getlisthistoryin()
			getlisthistoryout()
		except Exception as e:
			print(e)
			page.snack_bar = SnackBar(
				content=Text(e,size=25,color="white"),
				bgcolor="red"
				)
			page.snack_bar.open = True

		page.update()

	ct_login = Container(
		width=page.window_width,
		content=Column([
			Row([
				Text("Login User",size=25,weight="bold")
				]),
			TextField(label="username"),
			TextField(label="Email",visible=False),
			TextField(label="password",
				password=True, can_reveal_password=True
				),
			ElevatedButton("Login",
				bgcolor="orange",
				color="white",
				on_click=loginnow,
				visible=True
				),
			ElevatedButton("Register",
				bgcolor="green",
				color="white",
				on_click=registernow,
				visible=False
				),
			Checkbox(label="No Have Account ? , register now",
				value=False,
				on_change=changeregister
				)
			])
		)

	def submitnewinvoice(e):
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		totalprice = int(dialogcreateinvoice.content.controls[3].value) * int(dialogcreateinvoice.content.controls[4].controls[1].value)
		print(totalprice)
		try:
			res = client.collection("col_report").create({
			"id_report": dialogcreateinvoice.content.controls[0].value,
	    "image": dialogcreateinvoice.content.controls[1].src,
	    "name_br":dialogcreateinvoice.content.controls[2].value ,
	    "total_price": totalprice,
	    "total_pcs": dialogcreateinvoice.content.controls[4].controls[1].value,
	    "note": dialogcreateinvoice.content.controls[5].value,
	    "message_description": dialogcreateinvoice.content.controls[6].value,
	    "urgent": dialogcreateinvoice.content.controls[7].value,
				})
			mysnack.content= Text("Success created",size=20,color="white")
			mysnack.bgcolor = "green"
			dialogcreateinvoice.open = False
			page.snack_bar = mysnack
			mysnack.open = True
			getinvoicedata()
		except Exception as e:
			print(e)
			page.snack_bar = mysnack
			mysnack.content= Text(e,size=20,color="white")
			mysnack.bgcolor = "red"
			mysnack.open = True
		page.update()


	dialogcreateinvoice = AlertDialog(
		title=Text("New Invoice",size=25,weight="bold"),
		content=Column([
			TextField(label="id Report",disabled=True,
				),
			Image(src=False),
			TextField(label="Name",disabled=True),
			TextField(label="Price /item",disabled=True),
			Row([
			Text("Total Buy"),
			Dropdown(
				width=100,
				options=[
				dropdown.Option(1),
				dropdown.Option(2),
				dropdown.Option(3),
				dropdown.Option(4),
				dropdown.Option(5),
				]
				),
				],alignment="spaceEvenly"),
			TextField(label="Note "),
			TextField(label="Message Description"),
			Switch(label="This Urgent ?",value=False)
			],scroll="always"),
		actions=[
		ElevatedButton("Create Now",
			bgcolor="green",color="white",
			on_click=submitnewinvoice
			)
		],
		actions_alignment="center"
		)


	def createnewinvoice(e):
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		random_number = random.randint(10000000, 99999999)

		# Mendapatkan tanggal dan waktu saat ini
		now = datetime.now()
		tanggal_sekarang = now.strftime("%Y-%m-%d")
		waktu_sekarang = now.strftime("%H-%M-%S")

		getselect = e.control.data
		dialogcreateinvoice.content.controls[0].value = f"{random_number}_{tanggal_sekarang}_{waktu_sekarang}"
		dialogcreateinvoice.content.controls[1].src = getselect['image']
		dialogcreateinvoice.content.controls[2].value = getselect['name_br']
		dialogcreateinvoice.content.controls[3].value = getselect['price']


		page.dialog = dialogcreateinvoice
		dialogcreateinvoice.open = True
		page.update()


	def submitaddincoming(e):
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		update_id = dialogaddincoming.content.controls[0].value
		newupdate = {
			"stock":int(dialogaddincoming.content.controls[1].value) + int(dialogaddincoming.content.controls[2].controls[1].value)
		}
		try:
			res = client.collection("col_stock").update(update_id,newupdate)
			datenow = datetime.now()
			actualinstock = int(dialogaddincoming.content.controls[1].value) + int(dialogaddincoming.content.controls[2].controls[1].value)
			# AND ADD TO INCOMING COLLECT
			datamsg = {
			"message": dialogaddincoming.content.controls[3].value,
		    "name_br": dialogaddincoming.content.controls[4].value,
		    "stock_lates": actualinstock,
		    "get_stock":dialogaddincoming.content.controls[1].value,
		    "time": datenow.strftime("%H:%M"),
		    "date": datenow.strftime("%d%m%y")
			}
			addinputmsg = client.collection("incoming_history").create(datamsg)
			
			mysnack.content = Text("Success Add Stock",size=30)
			mysnack.bgcolor = "green"
			page.snack_bar  = mysnack
			dialogaddincoming.open = False
			mysnack.open = True
			getforincoming()
			getforoutgoing()
			getproductlist()
			dialogaddincoming.content.controls[1].value = ""
			dialogaddincoming.content.controls[3].value = ""

			page.update()
			getlisthistoryin()
		except Exception as e:
			print(e)
	def submitaddoutcoming(e):
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		update_id = dialogaddoutgoing.content.controls[0].value
		print("#######",int(dialogaddoutgoing.content.controls[2].controls[1].value),int(dialogaddoutgoing.content.controls[1].value))
		newupdate = {
			"stock":int(dialogaddoutgoing.content.controls[2].controls[1].value) - int(dialogaddoutgoing.content.controls[1].value)
		}
		try:
			res = client.collection("col_stock").update(update_id,newupdate)
			
			datenow = datetime.now()
			actualstock = int(dialogaddoutgoing.content.controls[2].controls[1].value) - int(dialogaddoutgoing.content.controls[1].value)
			dataoutmsg = {
			"message": dialogaddoutgoing.content.controls[3].value,
		    "name_br": dialogaddoutgoing.content.controls[4].value,
		    "latest_stock": actualstock,
		    "get_stock":dialogaddoutgoing.content.controls[1].value,
		    "time": datenow.strftime("%H:%M"),
		    "date": datenow.strftime("%d%m%y")
			}
			outstockmsg = client.collection("outcoming_history").create(dataoutmsg)
			

			mysnack.content = Text("Success Out Stock",size=30)
			mysnack.bgcolor = "red"
			page.snack_bar  = mysnack
			dialogaddoutgoing.open = False
			mysnack.open = True
			getforoutgoing()
			getforincoming()
			getproductlist()
			getlisthistoryout()
			dialogaddoutgoing.content.controls[1].value = ""
			dialogaddoutgoing.content.controls[3].value = ""
			page.update()
		except Exception as e:
			print(e)

	dialogaddincoming = AlertDialog(
		title=Text("Input Stok Incoming",weight="bold"),
		content=Column([
			TextField(label="Id Data",disabled=True),
			TextField(label="Input add Stock",border_color="green"),
			Row([
			Text("last stock",weight="bold"),
			Text(0)	
				],alignment="center"),
			TextField(label="Add Message For Input Stock"),
			TextField(label="Food Name",disabled=True),
			]),
		actions=[
		ElevatedButton("add new now",bgcolor="green",
			color="white",
			on_click=submitaddincoming
			)
		],
		actions_alignment="end"
		)
	dialogaddoutgoing = AlertDialog(
		title=Text("Input Stok out ",weight="bold"),
		content=Column([
			TextField(label="Id Data",disabled=True),
			TextField(label="Input Out Stock",border_color="red"),
			Row([
			Text("last stock",weight="bold"),
			Text(0)	
				],alignment="center"),
			TextField(label="Add Message For Out Stock"),
			TextField(label="Food Name",disabled=True),
			]),
		actions=[
		ElevatedButton("add out Stok",bgcolor="red",
			color="white",
			on_click=submitaddoutcoming
			)
		],
		actions_alignment="end"
		)
	def addincoming(e):
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		data = e.control.data
		dialogaddincoming.content.controls[0].value = data['id']
		dialogaddincoming.content.controls[2].controls[1].value = data['stock']
		dialogaddincoming.content.controls[4].value = data['name_br']
		page.dialog = dialogaddincoming
		dialogaddincoming.open = True
		page.update()
	def addoutgoing(e):
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		data = e.control.data
		dialogaddoutgoing.content.controls[0].value = data['id']
		dialogaddoutgoing.content.controls[2].controls[1].value = data['stock']
		dialogaddoutgoing.content.controls[4].value = data['name_br']
		page.dialog = dialogaddoutgoing
		dialogaddoutgoing.open = True
		page.update()
	# get all data for incoming
	def getforoutgoing():
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		barangkeluarout.controls.clear()
		getout = client.collection("col_stock").get_list()
		for x in getout.items:
			barangkeluarout.controls.append(
				ListTile(
				title=Text(x.collection_id['name_br'],weight="bold"),
				subtitle=Column([
				Text(f"Created : {x.collection_id['created']}"),
				Text(f"Updated : {x.collection_id['updated']}"),
				Text(f"Last Stock : {x.collection_id['stock']} Pcs",
					weight="bold",
					color="red" if x.collection_id['stock'] <= 5 else "green"
					),
				Row([
				ElevatedButton("add outgoing",
					bgcolor="red",color="white",
					data=x.collection_id,
					on_click=addoutgoing
					)
					],alignment="end")
					])

					)
				)
		page.update()


	# GET LIST HISTORY IN
	def getlisthistoryin():
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		seelistinhistory.controls.clear()
		getlistin = client.collection("incoming_history").get_list()
		for x in getlistin.items:
			seelistinhistory.controls.append(
				Container(
				border_radius=30,
				bgcolor="green",
				padding=15,
				content=Column([
					Text(x.collection_id['name_br'],size=25,weight="bold",
						color="white"
						),
					Row([
					Text(f"Message : {x.collection_id['message']}",color="white"),
						],wrap=True),
					Row([
						Text(f"get Stock : {x.collection_id['get_stock']}",
							color="white",
							),
						Icon(name="arrow_upward",color="white",size=25)
						],alignment="spaceBetween"),
					Row([
						Text(f"Last balance : {x.collection_id['stock_lates']}",
							color="white",
							),
						Icon(name="check_circle",color="white",size=25)
						],alignment="spaceBetween"),
					Column([
						Text(f"created : {x.collection_id['date']}",color="white",
							size=20
							),
						Text(f"Time : {x.collection_id['time']}",color="white",
							size=20
							),
						])
					])
					)
				)
		page.update()

	# GET ALL HUSTORY OUT
	def getlisthistoryout():
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		seelistouthistory.controls.clear()
		getlistout = client.collection("outcoming_history").get_list()
		for x in getlistout.items:
			seelistouthistory.controls.append(
				Container(
				border_radius=30,
				bgcolor="red",
				padding=15,
				content=Column([
					Text(x.collection_id['name_br'],size=25,weight="bold",
						color="white"
						),
					Row([
					Text(f"Message : {x.collection_id['message']}",color="white"),
						],wrap=True),
					Row([
						Text(f"get Stock : {x.collection_id['get_stock']}",
							color="white",
							),
						Icon(name="arrow_downward",color="white",size=25)
						],alignment="spaceBetween"),
					Row([
						Text(f"Last balance : {x.collection_id['latest_stock']}",
							color="white",
							),
						Icon(name="check_circle",color="white",size=25)
						],alignment="spaceBetween"),
					Column([
						Text(f"created : {x.collection_id['date']}",color="white",
							size=20
							),
						Text(f"Time : {x.collection_id['time']}",color="white",
							size=20
							),
						])
					])
					)
				)
		page.update()

	# get all data for incoming
	def getforincoming():
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		barangmasuklist.controls.clear()
		getin = client.collection("col_stock").get_list()
		for x in getin.items:
			barangmasuklist.controls.append(
				ListTile(
				title=Text(x.collection_id['name_br'],weight="bold"),
				subtitle=Column([
				Text(f"Created : {x.collection_id['created']}"),
				Text(f"Updated : {x.collection_id['updated']}"),
				Text(f"Last Stock : {x.collection_id['stock']} Pcs",
					weight="bold",
					color="red" if x.collection_id['stock'] <= 5 else "green"
					),
				Row([
				ElevatedButton("add Incoming",
					bgcolor="green",color="white",
					data=x.collection_id,
					on_click=addincoming
					)
					],alignment="end")
					])

					)
				)
		page.update()


	# get all INVOICE DATA
	def getinvoicedata():
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		datainvoice.controls.clear()
		
		getinv = client.collection("col_report").get_list()
		print(getinv)
		for x in getinv.items:
			datainvoice.controls.append(
				ListTile(
					leading=CircleAvatar(
					foreground_image_url=x.collection_id['image']
						),
					title=Text(x.collection_id['name_br'],weight="bold"),
					subtitle=Column([
					Row([
						Text(f"price : {x.collection_id['total_price']}"),
						Text(f"{x.collection_id['total_pcs']} pcs"),
						Text(f"urgent: {x.collection_id['urgent']}",
							weight="bold",
						color="red" if x.collection_id['urgent'] == "true" else "black"
							),
					])
						])
					)
				)

		page.update()

	# GET ALL LIST PRODUCT
	def getproductlist():
		login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
		productList.controls.clear()
		
		getdata = client.collection("col_stock").get_list()
		for x in getdata.items:
			productList.controls.append(
				Container(
					bgcolor="yellow100",
					padding=10,
				content=Column([
					Image(src=x.collection_id['image'],width=300,height=200),
					Row([
					Text(x.collection_id['name_br'],size=25,
						weight="bold",
						color="blue"
						),
					Text(f"{x.collection_id['stock']} Pcs",
				color="green" if x.collection_id['stock'] > 5 else "red",
				weight="bold"
						)
						],alignment="spaceBetween"),
					Row([
					Text(f"$ {x.collection_id['price']}",size=20,weight="bold",
						color="green"
						),
					Text(x.collection_id['category'],
						size=10,weight="bold",
					color="green" if x.collection_id['category'] == "New product" else "blue"
						),

					],alignment="spaceBetween"),
					Row([
					Text(x.collection_id['description'],
						color="blue"
						)					
						],wrap=True),
					Row([
						ElevatedButton("Order This",
						bgcolor="pink",color="white",
						data=x.collection_id,
						on_click=createnewinvoice
							)
						],alignment="end")
					])
					)
				)
		page.update()
	

	



	def addnewdata(e):
		try:
			login = client.collection("users").auth_with_password(
			ct_login.content.controls[1].value,ct_login.content.controls[3].value
				)
			user_data = client.collection("users").auth_with_password(
  	ct_login.content.controls[1].value, ct_login.content.controls[3].value)
			
			res = client.collection("col_stock").create({
			 "image": dialognewdata.content.controls[0].value,
		    "name_br": dialognewdata.content.controls[1].value,
		    "category":dialognewdata.content.controls[2].controls[1].value,
		    "stock": dialognewdata.content.controls[3].value,
		    "price":dialognewdata.content.controls[4].value,
		    "available":dialognewdata.content.controls[5].value,
		    "description":dialognewdata.content.controls[6].value,

				})
			mysnack.content = Text("Success Add",size=30)
			mysnack.bgcolor = "blue"
			page.snack_bar = mysnack
			mysnack.open = True
			dialognewdata.open = False
		except Exception as e:
			print(e)
		page.update()

	dialognewdata = AlertDialog(
			title=Text("Add Foods",weight="bold"),
			content=Column([
				TextField(label="image Link"),
				TextField(label="name"),
				Row([
					Text("Category"),
					Dropdown(
					width=100,
					options=[
						dropdown.Option("Drinks"),
						dropdown.Option("Snacks"),
						dropdown.Option("Rice"),
						dropdown.Option("Meal"),
					]
					),
					],alignment="spaceBetween"),
				TextField(label="Stock Now",
					keyboard_type=KeyboardType.NUMBER
					),
				TextField(label="Price",
					keyboard_type=KeyboardType.NUMBER

					),
				Switch(label="Availabel Now",value=False),
				TextField(label="Description"),
				],scroll="auto"),
			actions=[
			ElevatedButton("add new",
				bgcolor="green",color="white",
				on_click=addnewdata
				)
			],
			actions_alignment="end"
			)

	def btndialogadnew(e):
		page.dialog = dialognewdata
		dialognewdata.open = True
		page.update()

	def backtohome(e):
		productList.visible = True
		listinvoice.visible = False
		page.update()

	def seehistoryin(e):
		barangmasuklist.visible = False
		seelistinhistory.visible = True
		page.update()


	def backshowincoming(e):
		barangmasuklist.visible = True
		seelistinhistory.visible = False
		page.update()

	def seehistoryout(e):
		barangkeluarout.visible = False
		seelistouthistory.visible = True
		page.update()


	def backshowoutcoming(e):
		barangkeluarout.visible = True
		seelistouthistory.visible = False
		page.update()

	closewindow = IconButton(icon="close",icon_size=30,
				icon_color="red",
				on_click=backtohome
				)


	listinvoice = Column(scroll="auto",visible=False,
		controls=[
		Row([
			Text("Order Daily",size=25,weight="bold"),
			closewindow
			],alignment="spaceBetween"),
		datainvoice
		]
		)
	listmasukin = Column(scroll="auto",visible=False,
		controls=[
		Row([
			Text("Incoming Foods",size=25,weight="bold",color="green"),
			closewindow
			],alignment="spaceBetween"),
		Row([
			TextButton("see History In",
			on_click=seehistoryin
			),
			IconButton(icon="playlist_add_check",icon_color="green",
				on_click=backshowincoming
				)
			],alignment="spaceBetween"),
		barangmasuklist,
		seelistinhistory
		]
		)
	listkeluar = Column(scroll="auto",visible=False,
		controls=[
		Row([
			Text("Outgoing Foods",size=25,weight="bold",color="red"),
			closewindow
			],alignment="spaceBetween"),
		Row([
			ElevatedButton("see History Out",
			color="red",
			on_click=seehistoryout
			),
			IconButton(icon="playlist_add_check",icon_color="green",
				on_click=backshowoutcoming
				)
			],alignment="spaceBetween"),
		barangkeluarout,
		seelistouthistory
		]
		)

	def dialoginvoice(e):
		productList.visible = False
		listinvoice.visible = True
		listmasukin.visible = False
		listkeluar.visible = False
		page.update()

	def dialogbarangin(e):
		productList.visible = False
		listinvoice.visible = False
		listmasukin.visible = True
		listkeluar.visible = False
		page.update()

	def dialogbarangout(e):
		productList.visible = False
		listinvoice.visible = False
		listmasukin.visible = False
		listkeluar.visible = True
		page.update()


	def logoutnow(e):
		page.client_storage.remove("userlog")
		ct_dashboard.visible = False
		ct_login.visible = True
		ct_login.content.controls[1].value = ""
		ct_login.content.controls[2].value = ""
		ct_login.content.controls[3].value = ""
		page.snack_bar = SnackBar(
				content=Text("You Logout",size=20,color="white"),
				bgcolor="red"
				)
		page.snack_bar.open = True
		page.update()
	userlog = page.client_storage.get("userlog")

	ct_dashboard = Container(
		visible=False if userlog == None else True,
		content=Column([
			Row([
			Text(f"Hi {userlog if userlog else 'None'}",
				weight="bold"
				),
			TextButton("Logout",
				on_click=logoutnow
				)
				],alignment="spaceBetween"),
			Row([
		ElevatedButton("Order",
			bgcolor="orange",color="white",
			on_click=dialoginvoice
			),
		ElevatedButton("IN",
			bgcolor="green",color="white",
			on_click=dialogbarangin
			),
		ElevatedButton("OUT",
			bgcolor="red",color="white",
			on_click=dialogbarangout

			),
			],alignment="center"),
		productList,
		listinvoice,
		listmasukin,
		listkeluar
			])
		)

	



	

	
	page.add(
		AppBar(
		title=Text("Food App",size=30,weight="bold",
			color="blue"
			),
		bgcolor="yellow",
		actions=[
		IconButton(icon="library_add",icon_size=30,
			on_click=btndialogadnew
			),
		]
			),
		ct_login,
		ct_dashboard
		
		)

flet.app(target=main)
