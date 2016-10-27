# ライブラリ読み込み
from PIL import Image
from PIL.ExifTags import TAGS

# 関数の定義 01
def get_exif_of_image(file):
    """Get EXIF of an image if exists.

    指定した画像のEXIFデータを取り出す関数
    @return exif_table Exif データを格納した辞書
    """
    im = Image.open(file)

    # Exif データを取得
    # 存在しなければそのまま終了 空の辞書を返す
    try:
        exif = im._getexif()
    except AttributeError:
        return {}

    # タグIDそのままでは人が読めないのでデコードして
    # テーブルに格納する
    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value

    return exif_table

def get_date_of_image(file):
    """Get date date of an image if exists

    指定した画像の Exif データのうち日付データを取り出す関数
    @return yyyy:mm:dd HH:MM:SS 形式の文字列
    """

    # get_exif_of_imageの戻り値のうち
    # 日付データのみを取得して返す
    exif_table = get_exif_of_image(file)
    return exif_table.get("DateTimeOriginal")

print (get_date_of_image("image/theta04.jpg"))
