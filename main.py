from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import base64

app = FastAPI()

# ⚠️ ВСТАВЬ СЮДА СВОИ СЕРВЕРА (VLESS/VMess), каждый с новой строки
RAW_SERVERS = """
vless://4ad3dbf5-2005-4d96-b56c-a0ca9905cab6@88.218.92.41:24694?type=tcp&security=reality&flow=xtls-rprx-vision&fp=firefox&pbk=kaPztgo_2b2CKxytGWXzn6EauyNKr6Ho8xerGpSS-SQ&sid=58301280&sni=metrika.yandex.ru#%F0%9F%87%A6%F0%9F%87%B2%20Armenia%20%E2%80%94%20%23280
vless://501a2da5-cb22-4a3f-915e-e3b821d1d62d@87.199.205.28:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=W-9zyiOq287RtXVTZlTFbSDJ0Mx8joyBLJoA7ZE7eBw&security=reality&sid=b7cd177731793b1e&sni=vkvd754.okcdn.ru&type=tcp#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%E2%80%94%20%2391
vless://30572b57-f5ab-4eb8-82d4-a24d399b99f6@83.168.69.15:56229?type=grpc&headerType=none&security=reality&encryption=none&sni=github.com&fp=firefox&pbk=PQLbmvCHSAwuq_Ka1W-6gQxQA_vIjItozo3Jbqkg9Xk&sid=a411cc#%F0%9F%87%B5%F0%9F%87%B1%20Poland%20%E2%80%94%20%23291
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@138.186.140.8:443?&security=tls&fp=chrome&sni=snip.edgeoneai.cc.cd&type=ws&headerType=none&host=snip.edgeoneai.cc.cd&path=%2F#%F0%9F%87%B2%F0%9F%87%BD%20Mexico%20%E2%80%94%20%23411
vless://11aabba0-5fd1-4f15-8068-74c1a466cefc@193.163.203.170:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=yandex.ru&fp=chrome&pbk=GCCZ1ZZjB_nj7yxqFi22bIIWWr_G6rnWUzDcssN_40o&sid=b28db60d77c50b4f&type=tcp&headerType=none#%F0%9F%87%B1%F0%9F%87%BB%20Latvia%20%E2%80%94%20%2374
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@69.8.128.249:8443?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2F&sni=snip.edgeoneai.cc.cd&fp=chrome#%F0%9F%87%AF%F0%9F%87%B5%20Japan%20%E2%80%94%20%2326
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@45.157.233.109:2087?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2F&sni=snip.edgeoneai.cc.cd&fp=chrome#%F0%9F%87%A9%F0%9F%87%AA%20Germany%20%E2%80%94%20%2358
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@57.131.153.153:2053?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40public-vpn-200.opengw.net%3A443&sni=snip.edgeoneai.cc.cd&fp=chrome#%F0%9F%87%AB%F0%9F%87%B7%20France%20%E2%80%94%20%23160
vless://fe551942-d6e5-4361-ae5c-1f2e9077cd79@83.219.97.18:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&headerType=none&pbk=32XFmS-ifqooBFY89KNP3ZrqgSBOd3vel9GlNinL6yw&security=reality&sid=03&sni=fi5.silalink.sbs&type=tcp#%F0%9F%87%AB%F0%9F%87%AE%20Finland%20%E2%80%94%20%2343
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@114.129.9.132:8443?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2F&sni=snip.edgeoneai.cc.cd&fp=chrome#%F0%9F%87%AA%F0%9F%87%AA%20Estonia%20%E2%80%94%20%23116
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@103.85.25.226:8443?&security=tls&fp=chrome&sni=snip.edgeoneai.cc.cd&type=ws&headerType=none&host=snip.edgeoneai.cc.cd&path=%2F#%F0%9F%87%A8%F0%9F%87%B3%20China%20%E2%80%94%20%23378
vless://12af3df8-2ffe-48fe-9b60-376f015ea4f8@51.161.72.153:37765?encryption=none&fp=chrome&pbk=g-4UVtgbojoxQaglMCttyLme4xjtTqomqxdZaVsruQ4&security=reality&serviceName=grpc_common1&sid=defda00d613c&sni=www.semiconductor.samsung.com&spx=%2Ffe82b9833f962d8&type=grpc#%F0%9F%87%A8%F0%9F%87%A6%20Canada%20%E2%80%94%20%23375
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@185.179.82.246:443?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40public-vpn-200.opengw.net%3A443fp%3Dchrome&sni=snip.edgeoneai.cc.cd#%F0%9F%87%A7%F0%9F%87%BE%20Belarus%20%E2%80%94%20%2339
vless://2f35965a-9a9b-45fd-ba32-987296dfb6be@45.9.156.42:443?security=reality&encryption=none&pbk=RDWvDEygSk1eyAQhIK95H9EteFbrS2d9JEjBrco54Bw&fp=random&spx=%2FHesarWeb&type=grpc&serviceName=gw.v2.RelayService&sni=bg5.univesalsrv.com&sid=1a3102bb8e51399e#%F0%9F%87%A7%F0%9F%87%AC%20Bulgaria%20%E2%80%94%20%23365
vless://36e89875-9c53-482b-bc41-d3890e9da176@51.161.204.244:443?flow=xtls-rprx-vision&fp=random&pbk=gCAazs5uxNuMZIxfDdw8wPE0nwKY4QfBfBkQveKAkEk&security=reality&sid=0ad08b47f498efd2&sni=www.cloudflare.com&type=tcp#%F0%9F%87%A6%F0%9F%87%BA%20Australia%20%E2%80%94%20%23246
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@103.107.53.42:443?&security=tls&fp=chrome&sni=snip.edgeoneai.cc.cd&type=ws&headerType=none&host=snip.edgeoneai.cc.cd&path=%2F#%F0%9F%87%B9%F0%9F%87%AD%20Thailand%20%E2%80%94%20%23426
vless://15397019-2fda-406a-9012-4b219a27bc88@96.62.71.250:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=Su5ULcRQKF-0DJIHZeTNEnXHBpyQtizmUrcNIYhZI0E&security=reality&sid=afee962d&sni=us2.launch.tel&type=tcp#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%20%E2%80%94%20%2320
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