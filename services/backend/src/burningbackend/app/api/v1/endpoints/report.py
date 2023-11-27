from burningbackend.app.models.history import History
from burningbackend.app.models.movie import Movie
import burningbackend.app.api.v1.endpoints.history as history

from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side

import pandas as pd
from io import BytesIO

from fastapi import APIRouter
from fastapi import HTTPException
from starlette.responses import StreamingResponse

router = APIRouter()

@router.get("/report.xlsx", response_description="Excel report retrieved")
async def get_report(movie: str):
    selected_movie = await Movie.find_one({"name": movie})
    data_sold = await History.find({"movie": movie, "cancellation": False, "isTeam": False}).to_list()
    team_data = await History.find({"movie": movie, "cancellation": False, "isTeam": True}).to_list()

    products_sold = [j for i in data_sold for j in i.products]
    team_products = [j for i in team_data for j in i.products]

    print(products_sold)
    print(team_products)

    total_sold = await history.get_total(movie, False, False, True)
    total_sold_team = await history.get_total(movie, True, False, True)

    wb = Workbook()
    ws = wb.active

    
    def summarize_products(orders):
        product_summary = {}

        for order in orders:
            for product in order['products']:
                name = product['name']
                amount = product['amount']
                price = product['price']
                total_price = price * amount

                if name in product_summary:
                    product_summary[name]['amount'] += amount
                    product_summary[name]['total'] += total_price
                else:
                    product_summary[name] = {
                        'amount': amount,
                        'total': total_price,
                        'price': price
                    }

        return product_summary
    
    def get_dict_info(dict, key, type):
        if key in dict:
            return dict[key][type]
        else:
            return 0

    products_dict = summarize_products(products_sold)
    team_products_dict = summarize_products(team_products)

    print("Product dic:" )
    print(products_dict)
    print("Team product dic:")
    print(team_products_dict)
    print("Products sold:")
    print(products_sold)
    print("Data sold:")
    print(data_sold)

    wb = Workbook()
    ws = wb.active

    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 20

    bold_font = Font(name='Calibri', bold=True)
    normal_font = Font(name='Calibri')

    thin_border = Border(top=Side(style='thin'))

    # Movie information
    ws.cell(row=1, column=1, value="Movie:").font = bold_font
    ws.cell(row=1, column=2, value=selected_movie.name).font = normal_font
    ws.cell(row=1, column=3, value=selected_movie.datetime).font = normal_font
    ws.cell(row=1, column=4, value=selected_movie.room).font = normal_font

    # Calc information
    ws.cell(row=3, column=1, value="Calc:").font = bold_font
    ws.cell(row=4, column=1, value="Products sold:").font = normal_font
    ws.cell(row=4, column=2, value=total_sold).font = normal_font
    ws.cell(row=5, column=1, value="Tickets sold:").font = normal_font
    ws.cell(row=5, column=2, value=get_dict_info(products_dict, "Ticket", "total")).font = normal_font
    ws.cell(row=6, column=1, value="Pfand sold:").font = normal_font
    ws.cell(row=6, column=2, value=get_dict_info(products_dict, "Pfand", "total")).font = normal_font
    ws.cell(row=7, column=1, value="Total sold:").font = normal_font
    ws.cell(row=7, column=2, value=total_sold).font = normal_font

    ws.cell(row=9, column=1, value="Pfand Rück:").font = normal_font
    ws.cell(row=9, column=2, value=get_dict_info(products_dict, "Pfand Rück", "total")).font = normal_font
    ws.cell(row=10, column=1, value="Total:").font = normal_font
    ws.cell(row=10, column=2, value=total_sold + get_dict_info(products_dict, "Pfand Rück", "total")).font = normal_font

    # Calc team information
    ws.cell(row=3, column=4, value="Calc team").font = bold_font
    ws.cell(row=4, column=4, value="Products team:").font = normal_font
    ws.cell(row=4, column=5, value=total_sold_team).font = normal_font
    ws.cell(row=5, column=4, value="Total team:").font = normal_font
    ws.cell(row=5, column=5, value=total_sold_team).font = normal_font


    # Tickets information
    ws.cell(row=12, column=1, value="Tickets:").font = bold_font
    ws.cell(row=13, column=1, value="Tickets amount:").font = normal_font
    ws.cell(row=13, column=2, value=get_dict_info(products_dict, "Ticket", "amount")).font = normal_font
    ws.cell(row=14, column=1, value="Freitickets amount:").font = normal_font
    ws.cell(row=14, column=2, value=get_dict_info(products_dict, "Freiticket", "amount")).font = normal_font
    ws.cell(row=15, column=1, value="Total amount:").font = normal_font
    ws.cell(row=15, column=2, value=get_dict_info(products_dict, "Ticket", "ammount") + get_dict_info(products_dict, "Freiticket", "amount")).font = normal_font


    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = f"attachment; filename={selected_movie.name}.xlsx"

    return response