from ShazamAPI import Shazam

def recognize_song_info(song_path):
    with open(song_path, 'rb') as fp:
        mp3_file_content_to_recognize = fp.read()

    recognize_generator = Shazam().recognize_song(mp3_file_content_to_recognize)
        # or just:
        # recognize_generator = Shazam().recognize_song('filename.mp3')

    flag = True

    for (offset, resp) in recognize_generator:
        if flag:
                if "track" in resp:
                    print(f"歌名: {resp['track']['title']}, 歌手: {resp['track']['subtitle']}")
                    flag = False
                else:
                    print("抱歉，没有找到你的歌曲(╯︵╰,)")
                break
        if not flag:
            break

song_path = r"wav\music_2.mp3"
recognize_song_info(song_path)