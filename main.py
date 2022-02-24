import glob
from datetime import datetime
from pathlib import Path
import pandas

import numpy as np
# import tabloo


from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
# from yad2 import df
from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import tabloo

Window.clearcolor = (1, 1, 1, 1)

Builder.load_file('my.kv')
df = pandas.read_csv('SampleData.csv')


def time_int(time):
    time_lst = [int(s) for s in time.split() if s.isdigit()]
    if (len(time_lst)) == 1:
        return time_lst[0]
    else:
        return time_lst[0] * 60 + time_lst[1]


def floor_int(vari):
    try:
        return int(vari)
    except:
        return 0

def price_int(vari):
    try:
        vari=vari.replace(',','')
        return int(vari)
    except:
        return 1000000
def room_int(vari):
    try:
        return int(vari)
    except:
        return 0



class MainScreen(Screen):
    pass

    # def sign_up(self):
    #     self.manager.current = "sign_up_screen"
    #
    def search(self, area, max_price, room, floor, dist):
        if floor == '':
            floor = 100
        if dist == '':
            dist = 1000000
        if room == '':
            room = 0
        if max_price== '':
            max_price = 1000000

        df_result = df[df['Time from universty'].apply(time_int) < int(dist)]
        df_result = df_result[df_result['Floor'].apply(floor_int) <= int(floor)]
        df_result = df_result[df_result['Price'].apply(price_int) <= int(max_price)]
        if room != 0:
            df_result = df_result[df_result['Rooms'].apply(room_int) == int(room)]

        tabloo.show(df_result)

    # def run(self):
    #     create_df()
    #     print('finish')
    #     tabloo.show(df)

        # print(type(dist), type(floor))

        # table = MDDataTable(column_data=[
        #     ('Address', dp(30)),
        #      ('Zone', dp(30)),
        #     ('Price', dp(30))
        #     ],
        #     row_data=[("דפנה 1",' סיגליות','3800')])
        # self.add_widget(table)

        # self.manager.current = 'search_success'

        # print(df['Time from universty'].apply(convert_to_int) < int(dist)df['Floor'].apply((floor_to_int)) < int(floor))
        # print(rooms,type(rooms))
        # print(dist,room)
        # print((df.loc[df['Rooms'] == int(room)]),df['Time from universty'].apply(convert_to_int) <float(dist))
        # #print(df['Time from universty'].apply(convert_to_int))
        # #print(df.loc[df['Time from universty'] =='21 mins'])


class SearchSuccess(Screen):
    def prin(self):
        for i in range(len(df.columns)):
            print(i)
        # self.ids.quote.text = df.to_string()


class RootWidget(ScreenManager):
    pass


# class SignUpScreen(Screen):
#     def add_user(self, uname, pword):
#         with open("users.json") as file:
#             users = json.load(file)
#
#         users[uname] = {'username': uname, 'password': pword,
#                         'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
#         # print(users)
#         with open('users.json', 'w') as file:
#             json.dump(users, file)
#         self.manager.current = "sign_up_screen_success"
#
#
# class SignUpScreenSuccess(Screen):
#     def to_login_page(self):
#         self.manager.current = "login_screen"
#
#
# class LoginScreenSuccess(Screen):
#     def log_out(self):
#         self.manager.transition.direction = "right"
#         self.manager.current = "login_screen"
#
#     def get_qoute(self, feel):
#         feel = feel.lower()
#         available_feelings = glob.glob("quotes/*txt")
#         available_feelings = [Path(filename).stem for filename
#                               in available_feelings]
#         if feel in available_feelings:
#             with open(f"quotes/{feel}.txt",encoding="utf8") as file:
#                 quotes = file.readlines()
#             self.ids.quote.text = random.choice(quotes)
#         else:
#             self.ids.quote.text = "Try another feeling"
#
# class ImageButton(ButtonBehavior,HoverBehavior,Image):
#     pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
