from re import sub
from decimal import Decimal
import requests
from bs4 import BeautifulSoup


def get_price_int(prodUrl):
    PRODUCT_URL = prodUrl
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    page = requests.get(url=PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    product_price = soup.find("span", class_="price").get_text()
    product_price = product_price.replace(",", ".")
    product_price_int = Decimal(sub(r"[^\d\-.]", "", product_price))
    return product_price_int


def get_price(prodUrl):
    PRODUCT_URL = prodUrl
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    page = requests.get(url=PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    product_price = soup.find("span", class_="price").get_text()
    product_price = product_price.replace(",", ".")
    return product_price


def get_title(prodUrl):
    PRODUCT_URL = prodUrl

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    page = requests.get(url=PRODUCT_URL, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")

    product_title = soup.find("h1", class_="detail-name").get_text()
    return product_title


# u1 = "https://www.toy.ru/catalog/technic/lego_technic_42126_konstruktor_lego_tekhnik_ford_f_150_raptor/"
# u2 = "https://www.toy.ru/catalog/technic/lego_technic_42125_konstruktor_lego_tekhnik_ferrari_488_gte_af_corse_51/"
# u3 = "https://www.toy.ru/catalog/printsessy_disney/lego_disney_43197_konstruktor_lego_printsessy_disney_ledyanoy_zamok/"
# u4 = "https://www.toy.ru/catalog/super_geroi/lego_super_heroes_76156_konstruktor_lego_super_geroi_vzlyet_domo/"
u5 = "https://www.toy.ru/catalog/star_wars_play_sets/mattel_star_wars_hbx33_zvezdnye_voyny_igrushka_plyushevaya_mandalorets_malysh/"
u6 = "https://www.toy.ru/catalog/star_wars_play_sets/star_wars_bandai_84545_zvezdnye_voyny_yaytso_transformer_dart_veyder/"
u7 = "https://www.toy.ru/catalog/toys-zheleznye-dorogi/eztec_62130_zheleznaya_doroga_north_pole_express_train_set_22_chasti/"
u8 = "https://www.toy.ru/catalog/minifigurki-igrovie/fortnite_fnt0960_mikrofigurka_geroya_dark_voyager_s_aksessuarami_ls/"
u9 = "https://www.toy.ru/catalog/toys-figurki/fortnite_fnt0661_figurka_geroya_oro_s_aksessuarami_ls/"
u10 = "https://www.toy.ru/catalog/igrushki_so_skidkoy/skwooshi_s30003_skvushi_massa_dlya_lepki_v_konteynere_85_g_v_assortimente/"
u11 = "https://www.toy.ru/catalog/toys-nabory-dlya-tvorchestva/stikbot_tst614r_stikbot_3_figurki_stikbot_off_the_grid_raptus/"
u12 = "https://www.toy.ru/catalog/modeli_mashin/welly_43617_velli_model_mashiny_1_34_39_bmw_x6/"
u13 = "https://www.toy.ru/catalog/kiberponedelnik/bunch_o_balloons_z1213_startovyy_nabor_100_sharov_v_assortimente/"
u14 = "https://www.toy.ru/catalog/modeli_mashin/welly_42341_velli_model_vintazhnoy_mashiny_1_34_39_mercedes_benz_300s_1955/"
u15 = "https://www.toy.ru/catalog/toys-figurki/spongebob_eu691004_skvidvard_krasivyy_mem_kollektsiya_20_sm_plastikovyy/"
u16 = "https://www.toy.ru/catalog/lego_juniors/lego_juniors_10766_konstruktor_lego_dzhuniors_istoriya_igrushek_4_vudi_na_mashine/"
u17 = "https://www.toy.ru/catalog/lyubimye_geroi/spin_master_dragons_6045084_lil_myagkaya_igrushka_seriya_drakony_fioletovaya/"
u18 = "https://www.toy.ru/catalog/modeli_mashin/welly_43701_model_mashiny_1_34_39_ford_f_150/"
u19 = "https://www.toy.ru/catalog/toys-nabory-dlya-tvorchestva/magnetic_book_tav033_razvivayushchaya_igra_grimyerka_veselya_79_detaley/"
u20 = "https://www.toy.ru/catalog/toys-figurki/stikbot_tst624_stikbot_megadino/"
u21 = "https://www.toy.ru/catalog/mininabory/paw_patrol_6059295_shchenyachiy_patrul_igrovoy_nabor_dino_smotrovaya_bashnya_dino_missiya/"

# --------------------------------------------------------------------------------


from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime)
    price = Column(String(64))
    price_int = Column(Numeric(10, 2))
    url = Column(String(64))

    def __repr__(self):
        return f"{self.name} | {self.price}"


engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)


def add_price(title, price, price_int, url):
    is_exist = session.query(Price).filter(
        Price.name == title
    ).order_by(Price.datetime.desc()).first()

    if not is_exist:
        session.add(
            Price(
                name=title,
                datetime=datetime.now(),
                price=price,
                price_int=price_int,
                url=url
            )
        )
        session.commit()
    else:
        if is_exist.price_int != price_int:
            session.add(
                Price(
                    name=title,
                    datetime=datetime.now(),
                    price=price,
                    price_int=price_int
                )
            )
            session.commit()


# add_price(get_title(u1), get_price(u1), get_price_int(u1), u1)
# add_price(get_title(u2), get_price(u2), get_price_int(u2), u2)
# add_price(get_title(u3), get_price(u3), get_price_int(u3), u3)
# add_price(get_title(u4), get_price(u4), get_price_int(u4), u4)
add_price(get_title(u5), get_price(u5), get_price_int(u5), u5)
add_price(get_title(u6), get_price(u6), get_price_int(u6), u6)
add_price(get_title(u7), get_price(u7), get_price_int(u7), u7)
add_price(get_title(u8), get_price(u8), get_price_int(u8), u8)
add_price(get_title(u9), get_price(u9), get_price_int(u9), u9)
add_price(get_title(u10), get_price(u10), get_price_int(u10), u10)
add_price(get_title(u11), get_price(u11), get_price_int(u11), u11)
add_price(get_title(u12), get_price(u12), get_price_int(u12), u12)
add_price(get_title(u13), get_price(u13), get_price_int(u13), u13)
add_price(get_title(u14), get_price(u14), get_price_int(u14), u14)
add_price(get_title(u15), get_price(u15), get_price_int(u15), u15)
add_price(get_title(u16), get_price(u16), get_price_int(u16), u16)
add_price(get_title(u17), get_price(u17), get_price_int(u17), u17)
add_price(get_title(u18), get_price(u18), get_price_int(u18), u18)
add_price(get_title(u19), get_price(u19), get_price_int(u19), u19)
add_price(get_title(u20), get_price(u20), get_price_int(u20), u20)
add_price(get_title(u21), get_price(u21), get_price_int(u21), u21)

items = session.query(Price).all()
for item in items:
    print(item)
