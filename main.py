from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import base64

app = FastAPI()

# ⚠️ ВСТАВЬ СЮДА СВОИ СЕРВЕРА (VLESS/VMess), каждый с новой строки
RAW_SERVERS = """
vless://408c51e8-9246-483d-ba73-34ab4e202eb9@88.218.92.41:24694?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=kaPztgo_2b2CKxytGWXzn6EauyNKr6Ho8xerGpSS-SQ&security=reality&sid=58301280&sni=metrika.yandex.ru&type=tcp#%F0%9F%87%A6%F0%9F%87%B2%20Armenia%20%E2%80%94%20%23302
vless://b6e5dc56-836f-48c1-9163-b0b0b43b647d@178.172.227.228:10444?type=tcp&security=reality&flow=xtls-rprx-vision&fp=safari&pbk=0oTkcqwLTUNLnSOP-VUWErmy6usAIg-biBE6ioZO-Vo&sid=8debcf36f1cc69ff&sni=ads.x5.ru&encryption=none#%F0%9F%87%A7%F0%9F%87%BE%20Belarus%20%E2%80%94%20%23199
vless://2f35965a-9a9b-45fd-ba32-987296dfb6be@45.9.156.27:443?encryption=none&fp=firefox&pbk=XBfCioniAKXgKYBUVnvBXu80AIaIa4SpAB3w8qeF7Gk&security=reality&serviceName=home.v1.ApiService&sid=1be1bd931c98c84a&sni=bg3.univesalsrv.com&type=grpc#%F0%9F%87%A7%F0%9F%87%AC%20Bulgaria%20%E2%80%94%20%23248
vless://12af3df8-2ffe-48fe-9b60-376f015ea4f8@51.161.72.153:37765?type=grpc&headerType=none&security=reality&encryption=none&sni=www.semiconductor.samsung.com&fp=firefox&pbk=g-4UVtgbojoxQaglMCttyLme4xjtTqomqxdZaVsruQ4&sid=defda00d613c&serviceName=grpc_common1&mode=gun#%F0%9F%87%A8%F0%9F%87%A6%20Canada%20%E2%80%94%20%23179
vless://605dea9b-b485-45c9-af9b-cc2b0195023c@194.26.141.223:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=Su5ULcRQKF-0DJIHZeTNEnXHBpyQtizmUrcNIYhZI0E&security=reality&sid=afee962d&sni=ee1.mycloud1.org&type=tcp#%F0%9F%87%AA%F0%9F%87%AA%20Estonia%20%E2%80%94%20%23299
vless://fe551942-d6e5-4361-ae5c-1f2e9077cd79@83.219.97.18:443?security=reality&encryption=none&sni=fi5.silalink.sbs&fp=firefox&pbk=32XFmS-ifqooBFY89KNP3ZrqgSBOd3vel9GlNinL6yw&sid=03&flow=xtls-rprx-vision&spx=%2F7243432879c33c9&type=tcp#%F0%9F%87%AB%F0%9F%87%AE%20Finland%20%E2%80%94%20%23197
vless://48ff2b70-e180-582f-8866-d9a2edeed5f5@62.210.91.2:23576?encryption=none&security=reality&type=tcp&sni=fuck.rkn&flow=xtls-rprx-vision&fp=chrome&pbk=1y5h2FGWKXTJ9xLPCqPo6Mw7RxoZzh6fGkEQKNxpZ3s&sid=01#%F0%9F%87%AB%F0%9F%87%B7%20France%20%E2%80%94%20%23134
vless://6c713691-3ca2-4446-ad25-113d1bed6b03@78.17.178.125:443?type=raw&security=reality&flow=xtls-rprx-vision&fp=ios&pbk=jcp4Lj_qYzxtkalm_XFjrmvqEMGRG7sb19yMwLe16WE&sid=e0215064d8d1fd7c&sni=cdn.tbank.ru#%F0%9F%87%A9%F0%9F%87%AA%20Germany%20%E2%80%94%20%2374
vless://968c71ab-c205-409b-9b2d-3b44f758adf2@103.24.207.42:8443?flow=xtls-rprx-vision&security=reality&sni=edge-fr.extazy.net&pbk=ygxQyBcJzlLgpSl3MCRDDiFET4TT-3wxa4GdG1obkCY&fp=firefox#%F0%9F%87%AF%F0%9F%87%B5%20Japan%20%E2%80%94%20%2372
vless://11aabba0-5fd1-4f15-8068-74c1a466cefc@193.163.203.170:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=GCCZ1ZZjB_nj7yxqFi22bIIWWr_G6rnWUzDcssN_40o&security=reality&sid=b28db60d77c50b4f&sni=yandex.ru&type=tcp#%F0%9F%87%B1%F0%9F%87%BB%20Latvia%20%E2%80%94%20%23227
vless://f259a2e5-fd8d-4db9-a3ac-6b26322cffa9@pl-cfe6b10b7f.shamanapp.online:34451?type=xhttp&headerType=none&security=tls&encryption=none&sni=pl-cfe6b10b7f.shamanapp.online&fp=firefox&path=%2FShamanXHTTP2026&host=pl-cfe6b10b7f.shamanapp.online&mode=stream-up#%F0%9F%87%B5%F0%9F%87%B1%20Poland%20%E2%80%94%20%23740
vless://41e9280c-818c-4939-b5d6-332bf4d872e6@213.152.165.204:2092?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=zeyIqmHylDrPbbtdG9BleBt0-fqKCHpZ0OZ9OY2_WUI&security=reality&sid=716b7eba38125f3a&sni=www.apple.com&type=tcp#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%E2%80%94%20%23228
vless://a346c521-7a7f-452b-9356-a4893feb5982@62.133.63.45:8444?encryption=none&fp=firefox&pbk=FWitre1jinQR7qz5HQ0q2Q4Gg9xA9B0SyizCziN7Ch0&security=reality&serviceName=GunService&sid=457fab2ac885dbe0&sni=github.com&type=grpc#%F0%9F%87%B9%F0%9F%87%B7%20T%C3%BCrkiye%20%E2%80%94%20%23422
vless://b9bfa54d-bc44-4592-a6d6-89a9665d286f@163.245.42.48:443?security=reality&sni=mother-earth.fyi&fp=firefox&pbk=SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc&type=tcp&flow=xtls-rprx-vision&packetEncoding=xudp&encryption=none#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%20%E2%80%94%20%2353
vless://689a62e4-37e7-41de-9e6a-f2a56368c9e2@185.105.108.176:443?encryption=none&flow=xtls-rprx-vision&headerType=none&pbk=U9O1sbuPwoTowF3Ka7CIgUZlRjokulxSwsYohEGCLA8&security=reality&sid=0d87fec579&sni=www.google.co.uk&type=tcp&fp=safari#%F0%9F%87%B7%F0%9F%87%B8%20Serbia%20%E2%80%94%20%23519
vless://2f35965a-9a9b-45fd-ba32-987296dfb6be@89.35.14.33:443?encryption=none&fp=firefox&pbk=TZVMqglhHzteJ6t34mtku75LKzXNq0CB6glKYMAH6zg&security=reality&serviceName=hub.v1.ApiService&sid=8e07337954f9823f&sni=md4.univesalsrv.com&type=grpc#%F0%9F%87%B2%F0%9F%87%A9%20Moldova%20%E2%80%94%20%23399
vless://3cd95e58-9f0a-47e1-9937-64a58e949aa5@176.12.79.242:443?type=raw&security=reality&flow=xtls-rprx-vision&fp=firefox&pbk=6eN2NciEaZis5J4muRRqpfLQ1OglI3A8lNSTmAGo6Do&sid=3c6fc84d&sni=stats.vk-portal.net#%F0%9F%87%B0%F0%9F%87%BF%20Kazakhstan%20%E2%80%94%20%23524
"""

@app.get("/sub/{user_token}")
async def get_subscription(user_token: str, request: Request):
    user_agent = request.headers.get("user-agent", "").lower()
    
    # 1. Если это браузер -> отдаем твой index.html
    if "mozilla" in user_agent:
        return FileResponse("index.html", media_type="text/html")
    
    # 2. Если это Happ/v2ray -> отдаем сервера
    else:
        clean_servers = "\n".join([line.strip() for line in RAW_SERVERS.strip().split("\n") if line.strip()])
        encoded_servers = base64.b64encode(clean_servers.encode('utf-8')).decode('utf-8')
        
        headers = {
            "Hide-Settings": "1",        # Скрывает настройки в Happ
            "Content-Type": "text/plain; charset=utf-8",
            "Profile-Title": "PaysyVPN"  # Название подписки в приложении
        }
        return Response(content=encoded_servers, headers=headers)

# Health check для Render
@app.get("/")
async def health_check():
    return {"status": "ok"}
