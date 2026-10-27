from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import base64

app = FastAPI()

# ⚠️ ВСТАВЬ СЮДА СВОИ СЕРВЕРА (VLESS/VMess), каждый с новой строки
RAW_SERVERS = """
vless://afbd410e-1663-4f40-9d3b-df5117aa23ca@92.246.138.68:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=g--okRGkuStMgPF1OoFz9xoJEQMEWD6KAKzvUUA2GHI&security=reality&sid=3d41300b11960f87&sni=ru17.oshost.network&type=tcp#%F0%9F%87%A6%F0%9F%87%B2%20Armenia%20%E2%80%94%20%23149
vless://ef328563-cda1-4530-9b0a-988cc5a74d78@188.137.158.189:443?type=raw&security=tls&flow=xtls-rprx-vision&fp=chrome&sni=softice.net#%F0%9F%87%A6%F0%9F%87%B9%20Austria%20%E2%80%94%20%23130
vless://e0216964-ffa1-4d39-82c4-0e40879a470d@2.59.218.23:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=Nvv8Dl8Ep7mVDOwYn5fiirUIRglzJmbMMhuMdKNAOUo&security=reality&sid=0c911aba142876ed&sni=sof.lamibeauty.site&type=tcp#%F0%9F%87%A7%F0%9F%87%AC%20Bulgaria%20%E2%80%94%20%23624
vless://dc620cd6-a9d8-4a0f-8f18-006b895db77e@66.70.179.198:2053?encryption=none&fp=firefox&pbk=k4l6TxwkBbx9DhZAFpByq5rfCWFSgyOex3f_eFe9CWU&security=reality&sid=83f8317a948bb769&sni=www.cloudflare.com&type=tcp#%F0%9F%87%A8%F0%9F%87%A6%20Canada%20%E2%80%94%20%23210
vless://5bb82f6f-e5b1-2bcf-6584-1abc8a3ec21f@122.8.46.3:443?encryption=none&fp=firefox&pbk=iVDh09Vm2DqZMNQoUdf-LCZ6TqVGb9mLXnClAK2LRj4&security=reality&sni=www.canon.com&type=xhttp#%F0%9F%87%A8%F0%9F%87%B3%20China%20%E2%80%94%20%23159
vless://e0216964-ffa1-4d39-82c4-0e40879a470d@45.83.182.199:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=vxYWiWJ0B-IrAyUGMwS8agSnEzvuDX0q1BplBdaiDBs&security=reality&sid=70a92a6138856c55&sni=ee.lamibeauty.site&type=tcp#%F0%9F%87%AA%F0%9F%87%AA%20Estonia%20%E2%80%94%20%23161
vless://056405e8-de9f-4d0d-8145-956f13cc34da@196.196.204.174:443?encryption=none&fp=firefox&pbk=nNe5Y8_G7L0_VO5lqlee3h5UmRH4RXjaRYGCDUkbQz4&security=reality&sid=2892e611785bafd1&sni=263651t.fi3.h1clayd.click&type=tcp#%F0%9F%87%AB%F0%9F%87%AE%20Finland%20%E2%80%94%20%23248
vless://047466dd-05aa-4331-abf7-322c5aaecf97@83.136.209.31:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=HLKQ0JvyaZ16JNdl0pbEPkiVRYJDiZNzGz9prDMiw2s&security=reality&sid=a1b2c3d4b5&sni=fra.viralforge.ru&type=tcp#%F0%9F%87%AB%F0%9F%87%B7%20France%20%E2%80%94%20%23142
vless://f4d859eb-abc6-4c57-9eee-8fe9e2ef0f94@80.240.18.227:10051?encryption=none&fp=firefox&host=d-l28t5-65-b.pbe40wmcujaw726h7cpqernzmawz4stwtrnqve0n1s5reht.workers.dev&path=/@Marisa_kristi&security=tls&sni=d-l28t5-65-b.pbe40wmcujaw726h7cpqernzmawz4stwtrnqve0n1s5reht.workers.dev&type=ws#%F0%9F%87%A9%F0%9F%87%AA%20Germany%20%E2%80%94%20%23175
vless://f259a2e5-fd8d-4db9-a3ac-6b26322cffa9@31.59.143.242:34451?encryption=none&fp=chrome&host=pl-cfe6b10b7f.shamanapp.online&mode=auto&path=/ShamanXHTTP2026&security=tls&sni=pl-cfe6b10b7f.shamanapp.online&type=xhttp#%F0%9F%87%B5%F0%9F%87%B1%20Poland%20%E2%80%94%20%23489
vless://689a62e4-37e7-41de-9e6a-f2a56368c9e2@185.105.108.176:443?encryption=none&flow=xtls-rprx-vision&headerType=none&pbk=U9O1sbuPwoTowF3Ka7CIgUZlRjokulxSwsYohEGCLA8&security=reality&sid=0d87fec579&sni=www.google.co.uk&type=tcp&fp=safari#%F0%9F%87%B7%F0%9F%87%B8%20Serbia%20%E2%80%94%20%23293
vless://bc058e69-0444-4c7b-98da-bd67f0b143da@130.12.242.106:443?flow=xtls-rprx-vision&fp=random&pbk=vnjp7zIK2H3CGdjSis_79KXqS6IG-opmpbETPUD-EC8&security=reality&sid=15affa0af66dfc79&sni=deepl.com&type=tcp#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%E2%80%94%20%23139
vless://4ee88ef0-8922-48ce-9cd4-5f67ef201b35@31.76.252.113:51593?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=bnA5VC6PhGD2cYZyoZPr8Ah43WgQtzHuZbpywgoZH2k&security=reality&sid=167afe9a97a1&sni=intel.com&type=tcp#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%20%E2%80%94%20%23145
vless://09c10f40-6992-4b33-8d4a-6d8feb01323e@57.131.21.102:8080?security=reality&encryption=mlkem768x25519plus.native.0rtt.I8cgpaz5mHJF9FbDB6uFHSmJM7gWe39FURKzBjAqaVc&pbk=Lew0Y0hNzQyEeLxBpBxC2QnshUrtPvSdkLykPZcqLHs&headerType=none&type=tcp&flow=xtls-rprx-vision&sni=icloud.com&sid=b10dd5#%F0%9F%87%AE%F0%9F%87%B9%20Italy%20%E2%80%94%20%23450
vless://57beeeb0-03fc-4fc9-94da-7604488a7134@funagfrdfs.alixxplay.com:35544?security=reality&type=tcp&sni=iosapps.itunes.apple.com&fp=ios&flow=xtls-rprx-vision&sid=25c79e5856c7&pbk=HrcXRHtsitc_AVlN-_8fZuRgaP-Mqa_9JJotI9OnkVc#%F0%9F%87%AF%F0%9F%87%B5%20Japan%20%E2%80%94%20%23572
vless://2f35965a-9a9b-45fd-ba32-987296dfb6be@89.35.14.30:443?encryption=none&type=grpc&security=reality&sni=md1.univesalsrv.com&fp=chrome&pbk=xWejOQUn2koOUorUPSrHMLM-lyHlZ441KzxKc9bLmkY&sid=221ba6174224ca5b&spx=%2FHesarWeb&authority=TELEGRAM@MARAMBASHI_MARAMBASHI&serviceName=hub.v1.RelayService&mode=gun#%F0%9F%87%B2%F0%9F%87%A9%20Moldova%20%E2%80%94%20%23562
vless://4b1be712-774c-4b65-8491-a3339e124a70@136.148.211.243:443?encryption=none&fp=firefox&pbk=qJja_3vaCxm3As6alnqjpIIThwGm4e4m_MOluQBNFgo&security=reality&serviceName=grpc-se-3&sid=11d37dd92940329e&sni=se1-cl3.vless-fiberstasis.top&type=grpc#%F0%9F%87%B8%F0%9F%87%AA%20Sweden%20%E2%80%94%20%23132
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
