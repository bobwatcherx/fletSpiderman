from flet import *
from pocketbase import PocketBase 

client = PocketBase('https://boundless-nail.pockethost.io')

def main(page:Page):
	page.window_width = 300
	page.scroll = "auto"
	productList = Column()

	mysnack = SnackBar(content=Text())


	# GET ALL LIST PRODUCT
	def getproductlist():
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
					Text(x.collection_id['category'],size=10,weight="bold"),

					],alignment="spaceBetween"),
					Row([
					Text(x.collection_id['description'])					
						],wrap=True)
					])
					)
				)
		page.update()
	

	# LOAD DATA

	getproductlist()


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
		productList
		
		)

flet.app(target=main)
