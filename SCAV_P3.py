import os

"""Create a script which it will invoke FFMPEG to create a HLS transport stream container with one video you already 
have. No DRM needed. """


def createHLS(input_file):
    # Get file information
    # os.system('ffmpeg -i {0} -hide_banner'.format(input_file))
    os.system('ffmpeg -y -i {0} -preset slow -g 120 -sc_threshold 0 '
              '-map 0:0 -map 0:1 -map 0:0 -map 0:1 '
              '-s:v:0 640x360 -c:v:0 libx264 -b:v:0 365k '
              '-s:v:1 960x540 -c:v:1 libx264 -b:v:1 2000k '
              '-c:a copy '
              '-var_stream_map "v:0,a:0 v:1,a:1" '
              '-master_pl_name master.m3u8 '
              '-f hls -hls_time 6 -hls_list_size 0 '
              '-hls_segment_filename "v%v/fileSequence%d.ts" '
              'v%v/prog_index.m3u8'.format(input_file))


"""Download the bento4 tools and use them to create a MPD video file with any encryption you want.
You’ll need to fragment, encrypt and dash the file."""


def createMPD(input_file):
    # Get info of the file
    # os.system('mp4info BBB_frag.mp4')
    # Fragment the file
    os.system('mp4fragment --fragment-duration 6000 {0} BBB_frag.mp4'.format(input_file))
    # Encrypt the file
    os.system('mp4encrypt --method MPEG-CENC '
              '--key 1:a0a1a2a3a4a5a6a7a8a9aaabacadaeaf:0123456789abcdef '
              '--property 1:KID:121a0fca0f1b475b8910297fa8e0a07e '
              '--key 2:a0a1a2a3a4a5a6a7a8a9aaabacadaeaf:aaaaaaaabbbbbbbb '
              '--property 2:KID:121a0fca0f1b475b8910297fa8e0a07e '
              'BBB_frag.mp4 '
              'BBB_frag-cenc.mp4')
    # Dash the file
    os.system('mp4dash --mpd-name BBB_mpd.mpd BBB_frag-cenc.mp4')


"""Create a script to livestream with ffmpeg (any protocol you want) and open it from 
mobile or any other device in the same network."""


def videoStreaming(input_file):
    input_file = 'BBB_CUT.mp4'
    os.system('ffmpeg -re -i {0} -f mpegts udp://224.1.1.1:1234'.format(input_file))


if __name__ == '__main__':
    video = 'BBB_1minute.mp4'
    # createHLS(video)
    # createMPD(video)
    # videoStreaming(video)
