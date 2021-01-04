# -*- coding: UTF-8 -*-
# Public package
import configpars

# Private package




api_key = ''
actor_dict = {}

	
if quiet_flag:
    for filename,pic_path in pic_path_dict.items():
        proc_md5 = md5((filename+'+3').encode('UTF-8')).hexdigest()[14:-14]
        if (proc_flag and not proc_md5 in proc_list) or not proc_flag:
            with open(pic_path, 'rb') as pic_bit:
                b6_pic = b64encode(pic_bit.read())
            if emby_flag:
                url_post_img = host_url + 'emby/Items/' + actor_dict[filename.replace('.jpg','')] + '/Images/Primary?api_key=' + api_key
            else:
                url_post_img = host_url + 'jellyfin/Items/' + actor_dict[filename.replace('.jpg','')] + '/Images/Primary?api_key=' + api_key
            input_avatar(url_post_img,b6_pic)
        proc_log.write(proc_md5+'\n')
        while True:
            if threading.activeCount() > max_upload_connect + 1:
                time.sleep(0.01)
            else:
                break
        num_suc += 1