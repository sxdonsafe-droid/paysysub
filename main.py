from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import base64

app = FastAPI()

# ⚠️ ВСТАВЬ СЮДА СВОИ СЕРВЕРА (VLESS/VMess), каждый с новой строки
RAW_SERVERS = """
vless://afbd410e-1663-4f40-9d3b-df5117aa23ca@92.246.138.68:443?encryption=none&flow=xtls-rprx-vision&pbk=g--okRGkuStMgPF1OoFz9xoJEQMEWD6KAKzvUUA2GHI&security=reality&sid=3d41300b11960f87&sni=ru17.oshost.network&type=tcp&fp=chrome#%F0%9F%87%A6%F0%9F%87%B2%20Armenia%20%E2%80%94%20%2363
vless://36e89875-9c53-482b-bc41-d3890e9da176@51.161.204.244:443?flow=xtls-rprx-vision&fp=chrome&pbk=gCAazs5uxNuMZIxfDdw8wPE0nwKY4QfBfBkQveKAkEk&security=reality&sid=0ad08b47f498efd2&sni=www.cloudflare.com&type=tcp#%F0%9F%87%A6%F0%9F%87%BA%20Australia%20%E2%80%94%20%2393
vless://b6e5dc56-836f-48c1-9163-b0b0b43b647d@178.172.227.228:10444?security=reality&type=tcp&packetEncoding=xudp&sni=ads.x5.ru&fp=safari&flow=xtls-rprx-vision&sid=8debcf36f1cc69ff&pbk=0oTkcqwLTUNLnSOP-VUWErmy6usAIg-biBE6ioZO-Vo&encryption=none#%F0%9F%87%A7%F0%9F%87%BE%20Belarus%20%E2%80%94%20%23155
vless://e9a8144e-5237-488a-afb1-9ca3d8d54c80@216.128.169.78:15040?security=tls&type=tcp&sni=br.zestapp778.com&fp=firefox&encryption=none#%F0%9F%87%A7%F0%9F%87%B7%20Brazil%20%E2%80%94%20%23216
vless://a0fa7e19-70ec-41e0-b0cc-bcc984d4201a@94.26.41.47:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=eGTeI8aqjoea2v_vEHimFxEuC1IA42r2tg7IcP5oq1U&security=reality&sid=8e72c89e1adf4dc4&sni=ded.bsh-net.ru&type=tcp#%F0%9F%87%A7%F0%9F%87%AC%20Bulgaria%20%E2%80%94%20%23201
vless://d4001352-dc64-48b8-b786-5860b284ad3d@66.163.113.238:443?encryption=none&flow=xtls-rprx-vision&type=tcp&security=reality&sni=steamcommunity.com&fp=edge&pbk=DNCphTaL7BtXj1HybzMFir0ki_IiM62kr6ddIZYxagw&sid=5c56a4cfea5866c0#%F0%9F%87%A8%F0%9F%87%A6%20Canada%20%E2%80%94%20%23420
vless://48d9a277-776b-4ab8-a357-88a1958beed8@78.17.27.137:8443?encryption=none&fp=firefox&pbk=DZ0BYEIHEe9KmJzM_j5EAN0t3_BTcfO63P7x6SRCeQM&security=reality&sid=a05ccbf2edb5ebd1&sni=www.aalto.fi&type=tcp#%F0%9F%87%AB%F0%9F%87%AE%20Finland%20%E2%80%94%20%23186
vless://9ff5db63-88ff-4276-ab71-ac2b5cb2a740@45.92.218.130:443?security=reality&encryption=none&pbk=I0vZxWIjZYvtzlcvGaW01Q1U3M-vHD8iI8BM5KTuuiM&headerType=none&fp=chrome&spx=%2Fa38e5cd3c84c243&type=tcp&sni=delivery.mp.microsoft.com&sid=d3feff5d570d6b#%F0%9F%87%AB%F0%9F%87%B7%20France%20%E2%80%94%20%2344
vless://047466dd-05aa-4331-abf7-322c5aaecf97@45.142.106.121:443?encryption=none&flow=xtls-rprx-vision&pbk=HLKQ0JvyaZ16JNdl0pbEPkiVRYJDiZNzGz9prDMiw2s&security=reality&sid=a1b2c3d4b5&sni=dlx.viralforge.ru&type=tcp&fp=chrome#%F0%9F%87%A9%F0%9F%87%AA%20Germany%20%E2%80%94%20%23131
vless://0d607d84-0ae0-4b9c-a4f3-1766ab456e02@212.116.232.153:10443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=aNu3oMtcBnoDdRyef5zveVGswCkJow71NBiJ9GrGfSQ&security=reality&sid=10&sni=tengrinews.kz&type=tcp#%F0%9F%87%B0%F0%9F%87%BF%20Kazakhstan%20%E2%80%94%20%23172
vless://7072eeba-94fd-4fb3-92f2-a4506dd84cd8@31.76.91.70:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=ejx56dFtS4LK_Th6HSLFFdm7v7zqRpv8KfjrWAw4Sjg&security=reality&sid=bd6f67b6b2152b45&sni=fuji.etherhub.cc&type=tcp#%F0%9F%87%AF%F0%9F%87%B5%20Japan%20%E2%80%94%20%23240
vless://e0216964-ffa1-4d39-82c4-0e40879a470d@31.58.46.154:443?flow=xtls-rprx-vision&fp=firefox&pbk=vxYWiWJ0B-IrAyUGMwS8agSnEzvuDX0q1BplBdaiDBs&security=reality&sid=70a92a6138856c55&sni=ee.lamibeauty.site&type=raw#%F0%9F%87%B1%F0%9F%87%BB%20Latvia%20%E2%80%94%20%23342
vless://e9a8144e-5237-488a-afb1-9ca3d8d54c80@mx001.zestapp778.com:19167?security=tls&sni=mx001.zestapp778.com&type=tcp#%F0%9F%87%B2%F0%9F%87%BD%20Mexico%20%E2%80%94%20%23792
vless://cd3bb7d9-7df3-4644-ac05-c260990ac277@50.7.249.163:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&security=tls&sni=poland-new-new.failspace.top&type=tcp#%F0%9F%87%B5%F0%9F%87%B1%20Poland%20%E2%80%94%20%23193
vless://2f35965a-9a9b-45fd-ba32-987296dfb6be@150.40.126.21:443?encryption=none&fp=firefox&pbk=gHDoSWGWMVZKWNKONWHw-Cpl0-bdI6GaKusgJIQ-vWQ&security=reality&serviceName=edge.v2.FeedService&sid=35d05b666e2c6cdf&sni=rs3.univesalsrv.com&type=grpc#%F0%9F%87%B7%F0%9F%87%B8%20Serbia%20%E2%80%94%20%23198
vless://5de0c218-0138-45d8-94d2-c2c3f37a1a6d@83.147.18.75:443?flow=xtls-rprx-vision&fp=qq&pbk=tfFzmbVByvoZxxIEUiHMv22_k0-nQz00L0XjU0bd_Fc&security=reality&sid=7f1e29593aa94ad1&sni=www.bing.com&type=tcp#%F0%9F%87%AA%F0%9F%87%B8%20Spain%20%E2%80%94%20%2386
vless://48ff2b70-e180-582f-8866-d9a2edeed5f5@51.158.206.19:23576?encryption=none&flow=xtls-rprx-vision&type=tcp&security=reality&sni=fuck.rkn&pbk=1y5h2FGWKXTJ9xLPCqPo6Mw7RxoZzh6fGkEQKNxpZ3s&sid=01#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%E2%80%94%20%2327
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
