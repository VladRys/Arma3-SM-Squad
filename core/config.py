import os
from dotenv import load_dotenv

load_dotenv()

TEST_MODE = True
MODE = "TEST" if TEST_MODE else "PROD"

TVT_DATES = ["Четверг, 20:00 МСК", "Пятница, 20:00 МСК", "Суббота, 16:00 МСК", "Суббота, 20:00 МСК"]

# === Paths ===
SLOTS_FILE_PATH = os.getenv('SLOTS_FILE_PATH')
DB_FILE_PATH = os.getenv('DB_FILE_PATH')

# === Telegram ===
TOKEN_TELEGAM = os.getenv('TELEGRAM_TOKEN')
TEST_TOKEN_TELEGRAM = os.getenv('TELEGRAM_TEST_TOKEN')

MAIN_TOKEN_TELEGRAM = TEST_TOKEN_TELEGRAM if TEST_MODE else TOKEN_TELEGAM

ADMIN_IDS = os.getenv('ADMIN_IDS')
ADMINS = ADMIN_IDS.split()

# === Discord ===
TOKEN_DISCORD = os.getenv('TOKEN_DISCORD')

EVERYONE_ROLE_ID = 1009471127812321331
MODERATOR_ROLE_ID = 1010609592608235560

GUILD_ID = 960961865528250368

ANN_CHANNEL_ID = 1008819635879166052
BOT_CHANNEL_ID = 1265343421862907916
TICKET_CHANNEL_ID = 1112457350004101170
END_OF_TICKET_CHANNEL_ID = 1386367411317641278



EMBED_COLOR = 0xFF0000 

IMAGES_FOR_EMBED = [
    "https://cdn.discordapp.com/attachments/960961865528250368/1282814668716380194/202409072017431_1.png?ex=66e94b82&is=66e7fa02&hm=410c0ac2d91f17caaf682672fa28ed6fcdac74ed7b5aa9d26d1067dc30e1526c&",
    "https://media.discordvapp.net/attachments/960961865528250368/1282424569239437362/SSOKGBSOVOK.png?ex=66e931b3&is=66e7e033&hm=8b6ebcefc1881ac1473ae3db02c94f343adc619febccb93ff616fd720019f1b9&=&format=webp&quality=lossless&width=1199&height=676",
    "https://cdn.discordapp.com/attachments/960961865528250368/1280617361157656646/ArmA_3_SGSGSG_-_20.png?ex=66e9361b&is=66e7e49b&hm=906db30b8e330635bdcb57afb936a9f1ca5430d504dd8f4521af8199d0071b9b&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1278046609124364328/image.png?ex=66e9bf28&is=66e86da8&hm=51d58dff25c6cf71fa5ed89ab6976779b33bd87fe0807db3b4d62c63aad8b93f&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1267104969958625341/image.png?ex=66e97df6&is=66e82c76&hm=71a4dcf5d6525637f934d97ad2b0da0f8d7e670a7f79c79f6077a0202e5012a8&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1263925242146066463/ssosex.png?ex=66e9ca1c&is=66e8789c&hm=0fb079f3c8e225ee7c89b08be02ca345bed94f99308431f52ff0af6926dae717&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1262389353460793466/Arma3_x64_2024-07-15_13-38-39-Recovered.png?ex=66e979b3&is=66e82833&hm=18fb468a1eb17fddababe29a2ac7871bbfeaf3e7ed4bb8dd35c45229a1c79801&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1259113914474434580/ArmA_3_Screenshot_2024.07.06_-_13.58.08.87.png?ex=66e96cb6&is=66e81b36&hm=1f7705d138dbd4570d9d3c9002d13fce5671d4752f838de63848961b3527870f&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1258779418508267632/2024-07-05_163643.png?ex=66e986b0&is=66e83530&hm=c420e9ba2106f06af1cb139a104afc0c563c141d2f283b1693f3aa6925478112&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1257406425966186598/Arma3_x64_2024-07-01_20-49-19.png?ex=66e9cdfd&is=66e87c7d&hm=b9eb32a7364b14e86b4a66d48e442c7f037072f1f7dbeb828093cc9728567fe1&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1257310300156199022/ArmGJ-_14.29.48_edited.jpg?ex=66e97477&is=66e822f7&hm=d74f61dc76d8f7f0a97614b328e527adfe814431d14899651148f7a70dbeeef2&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1255654717602660362/image.png?ex=66e95d55&is=66e80bd5&hm=8adc028b881da9ff3552bd5c9450cff61f67164a1890579339542004da9720f6&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1288859862276640909/FIRSTchechenWar2var.png?ex=66fff249&is=66fea0c9&hm=4d81f8459a6c36589b2a0d4e38d92dd98d22f02bdd2c33a7605ea5746c659990&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1288790131582701578/A4rmA_3_Screenshot_2024.png?ex=66ffb157&is=66fe5fd7&hm=7e30b6301bf35baeddeb5f92d04f081501c2e1c31aa840abf4de097e8d119e11&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1288866589889794141/kavkaz.png?ex=66fff88d&is=66fea70d&hm=667a65decff7a30c6b74cbc8d3884c3ac1a86b4342d2da0e758c51f22fac0cc8&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1290058215870169190/20240930025407_1-gigapixel-scale-2_00x.png?ex=66ffb116&is=66fe5f96&hm=316e5808b877353e38ae04484ee59197067559fe22e13f0a316e8445620fb5e9&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1288302215823364158/villagepatrol.png?ex=66ffe52f&is=66fe93af&hm=3c5bdf3f8b8d80745a2e99519ea2ee52c7afe56974ad0cf475c7a91285d300ca&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1288525202552127519/FSBcopy.png?ex=67000c1b&is=66feba9b&hm=5e4f51958dd15ef458548e840e4e80667497744bf0a4ed2100130ec0cd135590&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1290086067487379496/fsb_caucas.png?ex=66ffcb07&is=66fe7987&hm=b20ac3ff2d6c1e2bf043498986c5ab0d7c104e1510e2463493110d2b98e8fab5&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1290684254979620955/snow2.png?ex=66fffde2&is=66feac62&hm=9f04d21678e8420a208d350823fa3436d46b7b27c63e9cbfa2f8949b7aa44e16&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1287162664304513104/usmc.png?ex=66ffb465&is=66fe62e5&hm=01ce0b9d5f2c5b2b4591325c5178effa566b16c5abd116ee05f840e7a517985d&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1286438750448128010/ArmA_3_Screenshot_2024.09.20_-_00.26.20.94.png?ex=66ffb532&is=66fe63b2&hm=22f350708fa6be5a667838f7d05a843686c9b20eb2c5d05b358954053ace6b68&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1285715884232409129/Arma3_x64_2024-09-17_17-04-16_.png?ex=66ffb6fa&is=66fe657a&hm=90d03c7aeb2afa3760132d135a265c4a246abcfad01c931ec1406bdafc2e5af1&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1283833436296970361/20240912184656_1.jpg?ex=67001e0f&is=66fecc8f&hm=7673c609660fe184538a5590e130492e6973d04490c038e6cef2c9f969e7e063&",
	"https://cdn.discordapp.com/attachments/960961865528250368/1282814668716380194/202409072017431_1.png?ex=66ffb502&is=66fe6382&hm=6c978c3a64cb0b044ad55c4cace5ffc0cf67ca8d18033956ee8365784ee191d3&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1300448075893968956/Arma3_x64_2024-10-28_15-48-53_.png?ex=6724d4a6&is=67238326&hm=f5ce6ef45a81b4bc5b5248f4111110e359cd6de580ee0a4bba4870e7b98b2f41&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1298247772620980284/IMG_20241022_143218_213.jpg?ex=67256535&is=672413b5&hm=84c92ab537200fb9b8bfc82a10f33a36236981139d0fec61afbb1c02bc179687&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1296787080302563409/ArmA_3_Screenshot_2024.10.18_-_13.12.23.09.png?ex=67255ad5&is=67240955&hm=0a13bded94c2b94f8057c0286e1adb8387be8d8e13c04082a06d8336ca4fffe3&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1292432949358362654/ARCTIC_VIEWS2.png?ex=672555bb&is=6724043b&hm=0e1989a80cfd5a97490b2a4c09e77df8aa700288a63c72b0ac3182a4b40b000d&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1288790131582701578/A4rmA_3_Screenshot_2024.png?ex=67254417&is=6723f297&hm=760cfc1e73d3efa5c78727d2d043ae1f575360a10e217ff17d7593063a391d14&",	
    "https://cdn.discordapp.com/attachments/960961865528250368/1288302215823364158/villagepatrol.png?ex=6724cf2f&is=67237daf&hm=0321ace0a9eb8341f2ec9ca662976f02d07ed887417458b73b4265f8018239d0&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1282316059432718346/5135135.png?ex=6724c8e4&is=67237764&hm=9527e725ba337e4dfcab7cf84f13c859a37f0929500a69d418a256825c8b65f7&",
    "https://cdn.discordapp.com/attachments/976906515309023252/1295755831941271663/333333111111.png?ex=6724e628&is=672394a8&hm=9308e3a78687de14ee445e542f90ca542a9c28380c0e1420665edf8dbce79b14&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1382412907912106085/Arma3_x64_2025-06-11_19-47-42.png?ex=68544a59&is=6852f8d9&hm=acb758202c54e25724abb99cecf80e99c056eb360d44f36bb8fbbc09811b7255",
    "https://cdn.discordapp.com/attachments/960961865528250368/1381274559528964126/ArmA_3_Screenshot_2025.06.08_-_17.09.23.64.png?ex=6854c36d&is=685371ed&hm=f59cd9838057eac46233267d7f831324e1cc665f16c6efe49575bdf557e1b7c2&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1377084908345884682/Arma3_x64_2025-05-22_23-32-15_925.png?ex=6854aec3&is=68535d43&hm=80b66e88a1bb5a5fe3d6ec3903d93a18db058acae3bdb2894e1e8542611e0991&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1375260211820105748/mich1112.png?ex=6854a2e1&is=68535161&hm=423b9139e8d007a752b4c36b809a2909bd334f11161281ec2723f12fd203f9f0&",
    "https://cdn.discordapp.com/attachments/960961865528250368/1374355592164020234/russin_fsb_syria.png?ex=6854a423&is=685352a3&hm=05a02ad16efbf843b10ea9b3d151bd99c517e32be2141c5410795c6d88ff23c9&",
    "https://media.discordapp.net/attachments/960961865528250368/1369458045544960051/mountains.png?ex=68549f31&is=68534db1&hm=f56ef434bde544665dad5ee59c5273bee4abe3375243b7225f679af498d61cc8&=&format=webp&quality=lossless&width=1536&height=864",
    "https://cdn.discordapp.com/attachments/960961865528250368/1367883242350579722/20250501204152_1.jpg?ex=6854d34b&is=685381cb&hm=34e07d271c07a75f0bac9dd7b5dbc6aaa5cdfc320fe1dfb74d37789193459002&"
]