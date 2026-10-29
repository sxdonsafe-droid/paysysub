from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import base64

app = FastAPI()

# ⚠️ ВСТАВЬ СЮДА СВОИ СЕРВЕРА (VLESS/VMess), каждый с новой строки
RAW_SERVERS = """
vless://f667a096-5231-4cfb-8759-92bb32473139@77.91.68.70:55983?encryption=none&fp=chrome&pbk=nWQ7b9l9X6N3PrXLgIzOvMM8iSYrqjVHEb9ikWxqYSg&security=reality&sid=0e&sni=yahoo.com&type=tcp#%F0%9F%87%A6%F0%9F%87%B2%20Armenia%20%E2%80%94%20%23498
vless://e9a8144e-5237-488a-afb1-9ca3d8d54c80@149.28.169.149:35652?encryption=none&fp=firefox&security=tls&sni=au001.zestapp778.com&type=tcp#%F0%9F%87%A6%F0%9F%87%BA%20Australia%20%E2%80%94%20%2372
vless://e0216964-ffa1-4d39-82c4-0e40879a470d@151.242.144.212:8443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=9p1Pr_KAsgtg31YUPPZ_LlsNmNd48FjHdML8x9SDeA8&security=reality&sid=296ba5bd68d56a8d&sni=khv.nullo.pro&type=tcp#%F0%9F%87%A6%F0%9F%87%B9%20Austria%20%E2%80%94%20%23601
vless://6c713691-3ca2-4446-ad25-113d1bed6b03@46.243.183.2:443?&security=reality&flow=xtls-rprx-vision&pbk=lrbP-ePUk7nbeLS8vBLbP5yyld7ZLmTB4_VQWRO31T8&sid=8a68df3a93c63ac8&fp=chrome&sni=stream.indigo.ru&type=tcp&headerType=none&host=stream.indigo.ru&path=%2F#%F0%9F%87%A7%F0%9F%87%BE%20Belarus%20%E2%80%94%20%2384
vless://706bce83-91db-4260-b175-cba29145cd56@93.152.223.244:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=yKwDGqOdkC_nEPOQHMvAQLPcPK8YHskv_opYoY66Yk8&security=reality&sni=ddk5-ger.newagetechnologies.live&type=tcp#%F0%9F%87%A7%F0%9F%87%AC%20Bulgaria%20%E2%80%94%20%23220
vless://e9a8144e-5237-488a-afb1-9ca3d8d54c80@216.128.185.90:32355?encryption=none&fp=firefox&security=tls&sni=ca001.zestapp778.com&type=tcp#%F0%9F%87%A8%F0%9F%87%A6%20Canada%20%E2%80%94%20%23218
vless://5d9fb46f-c4bc-4d6e-9a26-a4d5f51abd28@ee-2e06d85dc0.shamanapp.online:34451?type=xhttp&security=tls&fp=chrome&sni=ee-2e06d85dc0.shamanapp.online&path=/ShamanXHTTP2026&host=ee-2e06d85dc0.shamanapp.online&mode=stream-up&extra={#%F0%9F%87%AA%F0%9F%87%AA%20Estonia%20%E2%80%94%20%23592
vless://48d9a277-776b-4ab8-a357-88a1958beed8@78.17.27.137:8443?encryption=none&fp=firefox&pbk=DZ0BYEIHEe9KmJzM_j5EAN0t3_BTcfO63P7x6SRCeQM&security=reality&sid=a05ccbf2edb5ebd1&sni=www.aalto.fi&type=tcp#%F0%9F%87%AB%F0%9F%87%AE%20Finland%20%E2%80%94%20%2348
vless://48ff2b70-e180-582f-8866-d9a2edeed5f5@62.210.91.2:23576?type=tcp&encryption=none&flow=xtls-rprx-vision&sni=fuck.rkn&fp=chrome&security=reality&pbk=1y5h2FGWKXTJ9xLPCqPo6Mw7RxoZzh6fGkEQKNxpZ3s&sid=01#%F0%9F%87%AB%F0%9F%87%B7%20France%20%E2%80%94%20%23178
vless://76ef5ab3-7075-4e23-b445-f3b1bd05d431@87.120.126.43:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&security=tls&sni=gr.connect-qik.uk&type=tcp#%F0%9F%87%A9%F0%9F%87%AA%20Germany%20%E2%80%94%20%238
vless://d342d11e-d224-4463-b982-532309285094@141.11.139.215:443?security=tls&type=ws&path=%2F&host=ccc.010304.xyz&packetEncoding=xudp&sni=ccc.010304.xyz&fp=chrome#%F0%9F%87%AF%F0%9F%87%B5%20Japan%20%E2%80%94%20%23314
vless://11aabba0-5fd1-4f15-8068-74c1a466cefc@193.163.203.170:443?flow=xtls-rprx-vision&fp=safari&host=%2F%3Ftelegram--marambashi--marambashi&pbk=GCCZ1ZZjB_nj7yxqFi22bIIWWr_G6rnWUzDcssN_40o&security=reality&sid=b28db60d77c50b4f&sni=yandex.ru&type=tcp#%F0%9F%87%B1%F0%9F%87%BB%20Latvia%20%E2%80%94%20%23214
vless://e0216964-ffa1-4d39-82c4-0e40879a470d@185.32.6.26:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=XYkuP_Keu-yL7EQ8xZc4RTmcVAfp06Z1onV2ZNrlsHM&security=reality&sid=c31f187b&sni=stable.nullo.pro&type=tcp#%F0%9F%87%B5%F0%9F%87%B1%20Poland%20%E2%80%94%20%23186
vless://fafc7c16-f890-45ee-a856-02df225172dd@196.245.52.164:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=qF1f5MNrOiov0tyPftS96_Osal5sWTL4keXlW32UtV8&security=reality&sid=f06b6d8a57f5fd8f&sni=898305t.es4.h1clayd.click&type=tcp#%F0%9F%87%AA%F0%9F%87%B8%20Spain%20%E2%80%94%20%23278
vless://3f044365-9592-4301-8291-f2d93fcc2570@87.121.221.103:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=Su5ULcRQKF-0DJIHZeTNEnXHBpyQtizmUrcNIYhZI0E&security=reality&sid=afee962d&sni=nl004.launch.tel&type=tcp#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%E2%80%94%20%2364
vless://50a87e21-f0e2-4b53-a787-91adfe748f63@201.58.186.175:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=EEL-yDPBfol_fiEEM8Pd0zue7SSz5MtZlXEePVak2jc&security=reality&sni=hollandlanzerotte.xyz&type=tcp#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%20%E2%80%94%20%2318
vless://fafc7c16-f890-45ee-a856-02df225172dd@196.245.52.164:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=qF1f5MNrOiov0tyPftS96_Osal5sWTL4keXlW32UtV8&security=reality&sid=f06b6d8a57f5fd8f&sni=898305t.es4.h1clayd.click&type=tcp#%F0%9F%87%AA%F0%9F%87%B8%20Spain%20%E2%80%94%20%23278
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
