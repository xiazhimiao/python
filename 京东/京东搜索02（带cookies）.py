import requests

url = 'https://api.m.jd.com/?appid=search-pc-java&functionId=pc_search_s_new&client=pc&clientVersion=1.0.0&t=1728182560118&body=%7B%22keyword%22%3A%22%E8%AE%A1%E7%AE%97%E6%9C%BA%22%2C%22pvid%22%3A%22911b7ac7527a4c74afbce1e112d8b7e3%22%2C%22isList%22%3A0%2C%22page%22%3A%225%22%2C%22s%22%3A%22116%22%2C%22click%22%3A%220%22%2C%22log_id%22%3A%221728182561100.9785%22%2C%22show_items%22%3A%22%22%7D&loginType=3&uuid=143920055.1727785786646135020273.1727785787.1728133983.1728179539.4&area=9_644_24071_61762&h5st=20241006104240120%3Bcroocx1b2ksodd83%3Bf06cc%3Btk03wa2211cbe18n13XfIe7M1PyEEi3l6Vw7zljSpegX3nXsI4saGI-0sqwWTH8HwwghyBgdSz4ebzJXZkd6mgHXL_Sl%3B57a0fd7e13dca2b6bac73742c4cee95d302a235a39effc82f514d94331fa2b6d%3B4.8%3B1728182560120%3BTKmWZt2Oj2T9yZg6rNz_l2f_nZw6zNUOcOU6wNUO2uWLmOTOcO07zJwO2W0UqOE_f_QJjSD_l6DJxxjKhGzKlGwJxxT9iKz9y9jJj6zKlOUOcOU6Qlg90Bg50WUOMm0OiKDJhKDKzJAI0BTKh2TKh_DImyj_z9DKdGA_g_Q9h2zO2uzOjRw5oRg_0WUOMm0OleUIoGz53BQ7t9g-h2wO2uzOgNUO2uWL0SCKuhABxBv8mKTC0W0I0ig7ydA_kNUO2uWL0OjKoxgB0W0I0_Q60WUOMmE32W0UmW0I02D50NUO2WUOMm0O0W0I06D50NUO2WUOMm0KiW0I0_D50NUO2WUOMmUK2uzOhCv_0WUO2W0UqWTOcOUJhNwO2WUO2uWLfKTOcOkKhNwO2WUO2uWLliUOcO0KhNwO2WUO2uWL0_zLleUK0W0I0SD50NUO2WUOMmUK2uzOr5vO2WUO2uWLhW0I0KP70WUO2W0UqWTOcOU70WUO2W0UqWTOcOU9fNUO2WUOMqPOcOU9oBQ5eBwO2W0UqiPO2u2OG1x4Jxg71JAFMhi_3Fw80W0I0OT60WUO2W0UbV0I0WP60WUOMm0Oi_T42qTJgeA8-VkImeUKlWUBIVk6fZQ9oxgB0W0I0SA5jNUO2um4%3Bfed859bbc5d04841e609db32fcd12a5bbac2d1f842e00580fd8be52b4d555244&x-api-eid-token=jdd03VL2YPRJSQU7EXMWKUSZEQKMU3RUO3VFU7ZZ2IOZSINVEXHWWEZQNOEYTJZFVFFSAOJVQZ4C5HQWSBTITDDIYHSRSC4AAAAMSL62KWLAAAAAACCKAFEJDZ3E2FUX'

print(requests.get(url).text)


'''

https://api.m.jd.com/?
appid=search-pc-java
&functionId=pc_search_s_new
&client=pc
&clientVersion=1.0.0
&t=1728185333314
&body=%7B%22keyword%22%3A%22%E8%AE%A1%E7%AE%97%E6%9C%BA%22%2C%22suggest%22%3A%221.his.0.0%22%2C%22wq%22%3A%22%E8%AE%A1%E7%AE%97%E6%9C%BA%22%2C%22pvid%22%3A%228f53f34d36c648bfb2e84b61a0d0bf7c%22%2C%22page%22%3A%222%22%2C%22s%22%3A%2226%22%2C%22scrolling%22%3A%22y%22%2C%22log_id%22%3A%221728185249494.9372%22%2C%22tpl%22%3A%221_M%22%2C%22isList%22%3A0%2C%22show_items%22%3A%22%22%7D
&loginType=3
&uuid=143920055.1727785786646135020273.1727785787.1728179539.1728185218.5
&area=9_644_24071_61762
&h5st=20241006112853323%3Bcroocx1b2ksodd83%3Bf06cc%3Btk03wa2211cbe18n13XfIe7M1PyEEi3l6Vw7zljSpegX3nXsI4saGI-0sqwWTH8HwwghyBgdSz4ebzJXZkd6mgHXL_Sl%3Bedc53bc54f6bac9d95d39b9ac1c7abd30d5ddd08bc1850b1e1a5b3308a81e6bd%3B4.8%3B1728185333323%3BTKmWZt2Oj2T9yZg6rNz_l2f_nZw6zNUOcOU6wNUO2uWLmOTOcO07zJwO2W0UqOE_f_QJjSD_l6DJxxjKhGzKlGwJxxT9iKz9y9jJj6zKlOUOcOU6Qlg90Bg50WUOMm0OiKDJhKDKzJAI0BTKh2TKh_DImyj_z9DKdGA_g_Q9h2zO2uzOjRw5oRg_0WUOMm0OleUIoGz53BQ7t9g-h2wO2uzOgNUO2uWL0_DIn1C__NyCsB-B0W0I0ig7ydA_kNUO2uWL0OjKoxgB0W0I0_Q60WUOMmE32W0UmW0I02D50NUO2WUOMm0O0W0I06D50NUO2WUOMmEKiW0I0_D50NUO2WUOMmUK2uzOhCv_0WUO2W0UqWTOcOUJhNwO2WUO2uWLfKTOcOkKhNwO2WUO2uWLliUOcO0KhNwO2WUO2uWL0_zLleUK0W0I0SD50NUO2WUOMmUK2uzOr5vO2WUO2uWLhW0I0KP70WUO2W0UqWTOcOU70WUO2W0UqWTOcOU9fNUO2WUOMqPOcOU9oBQ5eBwO2W0UqiPO2u2OG1x4Jxg71JAFMhi_3Fw80W0I0OT60WUO2W0UbV0I0WP60WUOMm0Oi_T42qTJgeA8-VkImeUKlWUBIVk6fZQ9oxgB0W0I0SA5jNUO2um4%3B50fba9f9047d4490849b83df0b63d231bea9769958362ffc0b81da5537bf232e
&x-api-eid-token=jdd03VL2YPRJSQU7EXMWKUSZEQKMU3RUO3VFU7ZZ2IOZSINVEXHWWEZQNOEYTJZFVFFSAOJVQZ4C5HQWSBTITDDIYHSRSC4AAAAMSL7O5I6QAAAAAC4ODBPYKUFR2RAX


https://api.m.jd.com/?body=%7B%22keyword%22%3A%22%E8%AE%A1%E7%AE%97%E6%9C%BA%22%2C%22suggest%22%3A%221.his.0.0%22%2C%22wq%22%3A%22%E8%AE%A1%E7%AE%97%E6%9C%BA%22%2C%22pvid%22%3A%228f53f34d36c648bfb2e84b61a0d0bf7c%22%2C%22page%22%3A%222%22%2C%22s%22%3A%2226%22%2C%22scrolling%22%3A%22y%22%2C%22log_id%22%3A%221728185249494.9372%22%2C%22tpl%22%3A%221_M%22%2C%22isList%22%3A0%2C%22show_items%22%3A%22%22%7D



'''