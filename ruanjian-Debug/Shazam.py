from ShazamAPI import Shazam

def recognize_song_info(song_path):
    with open(song_path, 'rb') as fp:
        mp3_file_content_to_recognize = fp.read()

    recognize_generator = Shazam().recognize_song(mp3_file_content_to_recognize)
        # or just:
        # recognize_generator = Shazam().recognize_song('filename.mp3')

    flag = True
    count=0

    for (offset, resp) in recognize_generator:
        if flag:
            # 找到歌手和歌名
            if "track" in resp:
                track = resp['track']
                print(f"歌名: {track['title']}, 歌手: {track['subtitle']}")

                # 找到歌曲的专辑
                album_info = '未知专辑'
                for section in track.get('sections', []):
                    for meta in section.get('metadata', []):
                        if meta.get('title') == 'Альбом':
                            album_info = meta.get('text', '未知专辑')
                            print(f"所属专辑: {album_info}")

                # 输出歌曲的跳转链接
                share_href = resp["track"].get("share", {}).get("href", "")
                if share_href:
                    print("歌曲链接:", share_href)
                    count+=1
                return f"歌名: {track['title']}, 歌手: {track['subtitle']},所属专辑: {album_info},歌曲链接:{share_href}"

            else:
                return "库中没找到哦"
                break
        if(count==5):
            break
        if not flag:
            break
