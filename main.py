from PIL import Image, ImageDraw, ImageFont
from colorama import init, Fore

__version__ = "0.0.1"

init(autoreset=True)
print(Fore.LIGHTCYAN_EX + f"moji2sus {__version__}")
print(Fore.LIGHTCYAN_EX + "https://github.com/sevenc-nanashi/moji2sus")
print("")
print("SUS化するテキストを入力してください。")
print("[]で囲むことにより金ノーツにできます。")
print("また、!ではじめるとテキストを反転できます。")
print("----------------------------------------------------")
text = input("> ")
if text.startswith("!"):
    text = str(reversed(text[1:]))
font = ImageFont.truetype("./JF-Dot-K12.ttf", 12)

img = Image.new("RGB", (12 * len(text), 12))
draw = ImageDraw.Draw(img)

with open("./base.sus", "r") as f:
    base = f.read()
base = base.format(version=__version__)
file = open("./res.sus", "w")
file.write(base)

i = -1
gold = False
for char in text:
    if char == "[":
        gold = True
        continue
    if char == "]":
        gold = False
        continue
    i += 1
    x = 12 * i + 6
    x -= font.getsize(char)[0] / 2
    if gold:
        fill = (255, 255, 0)
    else:
        fill = (255, 0, 0)
    draw.text((x, -1), char, font=font, fill=fill)

img.save("./res.png")

for group_index in range(0, img.width, 12):
    for x in range(group_index, group_index + 12):
        note_data = ""
        for y in reversed(range(img.height)):
            if img.getpixel((x, y)) == (255, 0, 0):
                note_data += "11"
            elif img.getpixel((x, y)) == (255, 255, 0):
                note_data += "21"
            else:
                note_data += "00"
        sus_measure = str(group_index // 12).rjust(3, "0")
        sus_x = "23456789abcd"[x % 12]
        file.write(f"#{sus_measure}1{sus_x}:{note_data}\n")

print(Fore.LIGHTGREEN_EX + "正常に出力しました。")
