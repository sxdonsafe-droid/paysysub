from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import base64

app = FastAPI()

# ⚠️ ВСТАВЬ СЮДА СВОИ СЕРВЕРА (VLESS/VMess), каждый с новой строки
RAW_SERVERS = """
vless://4ad3dbf5-2005-4d96-b56c-a0ca9905cab6@88.218.92.41:24694?encryption=none&flow=xtls-rprx-vision&type=raw&headerType=none&security=reality&fp=chrome&pbk=kaPztgo_2b2CKxytGWXzn6EauyNKr6Ho8xerGpSS-SQ&sni=metrika.yandex.ru&sid=58301280#%F0%9F%87%A6%F0%9F%87%B2%20Armenia%20%E2%80%94%20%23630
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@130.78.190.134:443?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2F&sni=snip.edgeoneai.cc.cd#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%E2%80%94%20%2360
vless://42a64b9a-ab79-4094-8656-30366a7c2ea3@2.26.224.177:8443?encryption=none&fp=firefox&host=pl.peregrine-sub.net&pbk=PUj1la__ltNjv_ASE5n4HJY7GiRs--N-0aYhkcAApCI&security=reality&sid=7b6803a79bba5c52&sni=pl.peregrine-sub.net&type=xhttp#%F0%9F%87%B5%F0%9F%87%B1%20Poland%20%E2%80%94%20%23397
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@140.115.53.51:443?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2F&sni=snip.edgeoneai.cc.cd&fp=chrome#%F0%9F%87%B9%F0%9F%87%BC%20Taiwan%20%E2%80%94%20%23317
vless://11aabba0-5fd1-4f15-8068-74c1a466cefc@193.163.203.170:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=GCCZ1ZZjB_nj7yxqFi22bIIWWr_G6rnWUzDcssN_40o&security=reality&sid=b28db60d77c50b4f&sni=yandex.ru&type=tcp#%F0%9F%87%B1%F0%9F%87%BB%20Latvia%20%E2%80%94%20%23379
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@45.77.131.33:8443?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffp%3Dchrome&sni=snip.edgeoneai.cc.cd&fp=chrome#%F0%9F%87%AF%F0%9F%87%B5%20Japan%20%E2%80%94%20%23196
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@77.239.120.9:443?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffp%3Dchrome&sni=snip.edgeoneai.cc.cd&fp=chrome#%F0%9F%87%A9%F0%9F%87%AA%20Germany%20%E2%80%94%20%23156
vless://48ff2b70-e180-582f-8866-d9a2edeed5f5@62.210.91.2:23576?type=tcp&encryption=none&flow=xtls-rprx-vision&sni=fuck.rkn&fp=chrome&security=reality&pbk=1y5h2FGWKXTJ9xLPCqPo6Mw7RxoZzh6fGkEQKNxpZ3s&sid=01#%F0%9F%87%AB%F0%9F%87%B7%20France%20%E2%80%94%20%23230
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@91.108.241.242:2053?encryption=none&fp=firefox&host=snip.edgeoneai.cc.cd&security=tls&sni=snip.edgeoneai.cc.cd&type=ws#%F0%9F%87%AB%F0%9F%87%AE%20Finland%20%E2%80%94%20%23479
vless://605dea9b-b485-45c9-af9b-cc2b0195023c@194.26.141.223:443?&security=reality&flow=xtls-rprx-vision&pbk=Su5ULcRQKF-0DJIHZeTNEnXHBpyQtizmUrcNIYhZI0E&sid=afee962d&fp=firefox&sni=ee1.mycloud1.org&type=tcp&headerType=none&host=ee1.mycloud1.org&path=%2F#%F0%9F%87%AA%F0%9F%87%AA%20Estonia%20%E2%80%94%20%23185
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@103.85.25.226:8443?&security=tls&fp=chrome&sni=snip.edgeoneai.cc.cd&type=ws&headerType=none&host=snip.edgeoneai.cc.cd&path=%2F#%F0%9F%87%A8%F0%9F%87%B3%20China%20%E2%80%94%20%23190
vless://3cd95e58-9f0a-47e1-9937-64a58e949aa5@148.113.179.73:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=6eN2NciEaZis5J4muRRqpfLQ1OglI3A8lNSTmAGo6Do&security=reality&sid=3c6fc84d&sni=stats.vk-portal.net&type=tcp#%F0%9F%87%A8%F0%9F%87%A6%20Canada%20%E2%80%94%20%23642
vless://1af36694-b548-4b18-89a0-bc076eab4ed7@178.172.227.124:10444?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=0oTkcqwLTUNLnSOP-VUWErmy6usAIg-biBE6ioZO-Vo&security=reality&sid=8debcf36f1cc69ff&sni=ads.x5.ru&type=tcp#%F0%9F%87%A7%F0%9F%87%BE%20Belarus%20%E2%80%94%20%23543
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@13.140.29.253:443?encryption=none&security=tls&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffp%3Dchrome&sni=snip.edgeoneai.cc.cd#%F0%9F%87%A7%F0%9F%87%AC%20Bulgaria%20%E2%80%94%20%23205
vless://36e89875-9c53-482b-bc41-d3890e9da176@51.161.204.244:443?flow=xtls-rprx-vision&fp=firefox&pbk=gCAazs5uxNuMZIxfDdw8wPE0nwKY4QfBfBkQveKAkEk&security=reality&sid=0ad08b47f498efd2&sni=www.cloudflare.com&spx=%2F&type=tcp#%F0%9F%87%A6%F0%9F%87%BA%20Australia%20%E2%80%94%20%23344
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@103.114.201.154:443?encryption=none&fp=firefox&host=snip.edgeoneai.cc.cd&security=tls&sni=snip.edgeoneai.cc.cd&type=ws#%F0%9F%87%B9%F0%9F%87%AD%20Thailand%20%E2%80%94%20%23661
vless://b9bfa54d-bc44-4592-a6d6-89a9665d286f@163.245.42.48:443?security=reality&encryption=none&pbk=SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc&headerType=none&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=mother-earth.fyi#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%20%E2%80%94%20%231161
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
