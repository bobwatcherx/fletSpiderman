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
	mysnack = SnackBar(content=Text())


	def submitnewinvoice(e):
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
		update_id = dialogaddincoming.content.controls[0].value
		newupdate = {
			"stock":int(dialogaddincoming.content.controls[1].value) + int(dialogaddincoming.content.controls[2].controls[1].value)
		}
		try:
			res = client.collection("col_stock").update(update_id,newupdate)
			mysnack.content = Text("Success Add Stock",size=30)
			mysnack.bgcolor = "green"
			page.snack_bar  = mysnack
			dialogaddincoming.open = False
			mysnack.open = True
			getforincoming()
			getforoutgoing()
			getproductlist()
			dialogaddincoming.content.controls[1].value = ""

			page.update()
		except Exception as e:
			print(e)
	def submitaddoutcoming(e):
		update_id = dialogaddoutgoing.content.controls[0].value
		print("#######",int(dialogaddoutgoing.content.controls[2].controls[1].value),int(dialogaddoutgoing.content.controls[1].value))
		newupdate = {
			"stock":int(dialogaddoutgoing.content.controls[2].controls[1].value) - int(dialogaddoutgoing.content.controls[1].value)
		}
		try:
			res = client.collection("col_stock").update(update_id,newupdate)
			mysnack.content = Text("Success Out Stock",size=30)
			mysnack.bgcolor = "red"
			page.snack_bar  = mysnack
			dialogaddoutgoing.open = False
			mysnack.open = True
			getforoutgoing()
			getforincoming()
			getproductlist()
			dialogaddoutgoing.content.controls[1].value = ""
			page.update()
		except Exception as e:
			print(e)

	dialogaddincoming = AlertDialog(
		title=Text("Input Stok Incoming",weight="bold"),
		content=Column([
			TextField(label="Id Data",disabled=True),
			TextField(label="Input add Stock",border_color="green"),
			Row([
			Text("last stock"),
			Text(0)	
				])
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
			Text("last stock"),
			Text(0)	
				])
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
		data = e.control.data
		dialogaddincoming.content.controls[0].value = data['id']
		dialogaddincoming.content.controls[2].controls[1].value = data['stock']
		page.dialog = dialogaddincoming
		dialogaddincoming.open = True
		page.update()
	def addoutgoing(e):
		data = e.control.data
		dialogaddoutgoing.content.controls[0].value = data['id']
		dialogaddoutgoing.content.controls[2].controls[1].value = data['stock']
		page.dialog = dialogaddoutgoing
		dialogaddoutgoing.open = True
		page.update()
	# get all data for incoming
	def getforoutgoing():
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

	# get all data for incoming
	def getforincoming():
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
		productList.controls.clear()
		getdata = client.collection("col_stock").get_list()
		for x in getdata.items:
			productList.controls.append(
				Container(
					bgcolor="yellow100",
					padding=10,
				content=Column([
					Image(src=x.collection_id['image']),
					Row([
					Text(x.collection_id['name_br'],size=25,
						weight="bold"
						),
					Text(f"{x.collection_id['stock']} Pcs",
				color="green" if x.collection_id['stock'] > 5 else "red",
				weight="bold"
						)
						],alignment="spaceBetween"),
					Row([
					Text(x.collection_id['price'],size=20,weight="bold"),
					Text(x.collection_id['category'],
						size=10,weight="bold",
					color="green" if x.collection_id['category'] == "New product" else "blue"
						),

					],alignment="spaceBetween"),
					Row([
					Text(x.collection_id['description'])					
						],wrap=True),
					Row([
						ElevatedButton("Create Invoice",
						bgcolor="green",color="white",
						data=x.collection_id,
						on_click=createnewinvoice
							)
						],alignment="end")
					])
					)
				)
		page.update()
	

	# LOAD DATA

	getproductlist()
	getinvoicedata()
	getforincoming()
	getforoutgoing()


	def addnewdata(e):
		try:
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
			title=Text("Add Data",weight="bold"),
			content=Column([
				TextField(label="image Link"),
				TextField(label="name"),
				Row([
					Text("Category"),
					Dropdown(
					width=100,
					options=[
						dropdown.Option("New product"),
						dropdown.Option("Old product"),
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




	closewindow = IconButton(icon="close",icon_size=30,
				icon_color="red",
				on_click=backtohome
				)


	listinvoice = Column(scroll="auto",visible=False,
		controls=[
		Row([
			Text("Invoice Daily",size=25,weight="bold"),
			closewindow
			],alignment="spaceBetween"),
		datainvoice
		]
		)
	listmasukin = Column(scroll="auto",visible=False,
		controls=[
		Row([
			Text("Incoming",size=25,weight="bold",color="green"),
			closewindow
			],alignment="spaceBetween"),
		barangmasuklist
		]
		)
	listkeluar = Column(scroll="auto",visible=False,
		controls=[
		Row([
			Text("Outgoing",size=25,weight="bold",color="red"),
			closewindow
			],alignment="spaceBetween"),
		barangkeluarout
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

	page.add(
		AppBar(
		title=Text("Inventory App",size=30,weight="bold",
			),
		bgcolor="yellow",
		actions=[
		IconButton(icon="library_add",icon_size=30,
			on_click=btndialogadnew
			),
		]
			),
		Row([
		ElevatedButton("Invoice",
			bgcolor="blue",color="white",
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
		
		)

flet.app(target=main)
