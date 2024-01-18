import requests
import time

current_timestamp = int(time.time())
url = 'https://api.live.bilibili.com/msg/send'
data = {
    'bubble': '0',
    'msg': '昊龙你大限将至，速速来阴曹地府报道！',
    'color': '4546550',
    'mode': '1',
    'room_type': '0',
    'jumpfrom': '85001',
    'fontsize': '25',
    'rnd': current_timestamp,
    'roomid': '14709735',
    'csrf': 'f158364dff63d78330c7312cf919f705',
    'csrf_token': 'f158364dff63d78330c7312cf919f705',
}

headers = {
    'Cookie': 'buvid3=2D826576-70C1-5449-304B-285FB6709D6F48423infoc; b_nut=100; _uuid=C88BB945-684D-EC29-38F9-E88F2310C8E5548460infoc; buvid4=E6D26568-06F9-A3E7-A3C3-E17A78D9051D49300-023033115-kmv57zbod91Iizxn9LVC9w%3D%3D; CURRENT_PID=0028eb90-cf92-11ed-95d9-8de27a04dd54; rpdid=|(k|Yk|kJll~0J\'uY)|kRYul|; buvid_fp_plain=undefined; i-wanna-go-back=-1; header_theme_version=CLOSE; home_feed_column=4; DedeUserID=392297010; DedeUserID__ckMd5=777989099fea981f; b_ut=5; FEED_LIVE_VERSION=V8; nostalgia_conf=-1; fingerprint=00d93b8d794da3edf1f7e212829d02e0; browser_resolution=1280-619; LIVE_BUVID=AUTO7316884572552257; hit-new-style-dyn=1; hit-dyn-v2=1; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; enable_web_push=DISABLE; buvid_fp=00d93b8d794da3edf1f7e212829d02e0; innersign=0; b_lsid=74EF1110D_18C1F4CE2D7; SESSDATA=22e75e26%2C1716884185%2Ccf8bd%2Ab1CjD7vYrHXfHssffAMt9l_rXp-6y77wn21n_igGx-6hFI6iCDFp9ny4fAfmOa01raX38SVnhvMmdDUHJGUi1MUUhCNEF1OHQyVWY2bXh0UWQyXzNMdF9xbC03enFBeGdmaHZYVEFWVGtUWkJpUFA4OWZ6WnRJOXpZMmhqV21CYjE3Vm9yWE1xUnNBIIEC; bili_jct=f158364dff63d78330c7312cf919f705; sid=gduy0sfj; bp_video_offset_392297010=869701066339385351; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE1OTEzODcsImlhdCI6MTcwMTMzMjEyNywicGx0IjotMX0.t_c8t-WraqJURYaVH207WCSFwlO9kdjCLa6RGHRuulk; bili_ticket_expires=1701591327; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1701332193; PVID=2; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1701332204',
    'Origin': 'https//live.bilibili.com',
    'Referer': 'https://live.bilibili.com/84074?live_from=85001&spm_id_from=444.41.live_users.item.click',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
while True:
    response = requests.post(url=url, data=data, headers=headers)
    print(response.status_code)
    time.sleep(5)
