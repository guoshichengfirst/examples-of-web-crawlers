# -*- coding:utf-8 -*-

from wxpy import *
from platform import system
import os
import subprocess
import shutil
from tqdm import tqdm
from pyecharts import Pie
from pyecharts import Map

# 分析好友性别比例
def sex_ratio():

    # 初始化
    male, female, other = 0, 0, 0

    # 遍历
    for i in friends_dict.keys():
        if(friends_dict[i][2] == 1):
            male += 1
        elif(friends_dict[i][2] == 2):
            female += 1
        else:
            other += 1

    name_list = ['男性', '女性', '未设置']
    num_list = [male, female, other]

    pie = Pie("微信好友性别比例")
    pie.add("", name_list, num_list, is_label_show=True)
    pie.render('data/好友性别比例.html')




# 分析好友地区分布
def region_distribution():

    # 使用一个字典统计好友地区分布数量
    province_dict = {'北京': 0, '上海': 0, '天津': 0, '重庆': 0,
                     '河北': 0, '山西': 0, '吉林': 0, '辽宁': 0, '黑龙江': 0,
                     '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
                     '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0,
                     '江西': 0, '江苏': 0, '安徽': 0, '广东': 0, '海南': 0,
                     '四川': 0, '贵州': 0, '云南': 0, '内蒙古': 0, '新疆': 0,
                     '宁夏': 0, '广西': 0, '西藏': 0, '香港': 0, '澳门': 0}

    # 遍历
    for i in friends_dict.keys():
        # 判断省份是否存在，有可能是外国的，这种情况不考虑
        if (friends_dict[i][3] in province_dict):
            key = friends_dict[i][3]
            province_dict[key] += 1

    provice = list(province_dict.keys())
    values = list(province_dict.values())


    # maptype='china' 只显示全国直辖市和省级，数据只能是省名和直辖市的名称
    map = Map("微信好友地区分布")
    map.add("", provice, values, visual_range=[0, 50], maptype='china', is_visualmap=True, visual_text_color='#000')
    map.render(path="data/好友地区分布.html")




# 调用系统方式自动打开某个html文件
def open_html(file_name):
    if('Windows' in system()):
        # Windows
        os.startfile(file_name)
    elif('Darwin' in system()):
        # MacOSX
        subprocess.call(["open", file_name])
    elif('Linux' in system()):
        # Linux
        subprocess.call(["xdg-open", file_name])
    else:
        # 自行确定
        print("打开微信个人数据报告文件失败，请手动打开")
        exit()




# 生成一个html文件，并保存到文件file_name中
def generate_html(file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        data = '''
            <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
            <meta charset="UTF-8">
            <title>一键生成微信个人专属数据报告(了解你的微信社交历史)</title>
            <meta name='keywords' content='微信个人数据'>
            <meta name='description' content=''> 

            <iframe name="iframe1" marginwidth=0 marginheight=0 width=100% height=60% src="data/好友性别比例.html" frameborder=0></iframe>
            <iframe name="iframe2" marginwidth=0 marginheight=0 width=100% height=60% src="data/好友地区分布.html" frameborder=0></iframe>
        '''
        f.write(data)


# 运行前，请先确保安装了所需库文件
# 若没安装，请执行以下命令:pip install -r requirement.txt
if __name__ == '__main__':

    # 生成一些所需的目录
    if(not (os.path.exists('image'))):
        os.makedirs('image')
    else:
        shutil.rmtree('image')
        os.makedirs('image')

    if(not (os.path.exists('data'))):
        os.makedirs('data')
    else:
        shutil.rmtree('data')
        os.makedirs('data')




    # 启动微信机器人，自动根据操作系统执行不同的指令
    print(u'请扫描二维码以登录微信')
    if('Windows' in system()):
        # Windows
        bot = Bot()
    elif('Darwin' in system()):
        # MacOSX
        bot = Bot()
    elif('Linux' in system()):
        # Linux
        bot = Bot(console_qr=2,cache_path=True)
    else:
        # 自行确定
        print("无法识别你的操作系统类型，请自己设置")
        exit()


    # 获取好友数据
    print(u'正在获取微信好友数据信息，请耐心等待……')
    friends = bot.friends(update=False)
    # 好友信息字典
    friends_dict = {}
    count = 0

    # 将好友信息(除了头像)插入字典，方便后续处理数据，key:count，value:list
    for i in friends:
        friend_data_list = [i.nick_name, i.remark_name, i.sex, i.province, i.city, i.signature]
        friends_dict.update({count : friend_data_list})
        count += 1
    print(u'微信好友数据信息获取完毕')


    print(u'正在分析好友性别比例，请耐心等待……')
    sex_ratio()
    print(u'分析好友性别比例完毕')


    print(u'正在分析好友地区分布，请耐心等待……')
    region_distribution()
    print(u'分析好友地区分布完毕')



    # 获取好友头像，此步骤消耗时间比较长，故用采用tqdm进度条模块显示进度
    # tqdm为进度条模块，可以用来显示进度条，封装程度高，使用方式简单
    # 在测试的时候，为了节省时间，可以先使用friends[1:10]的方式来指定下载若干个好友头像数据
    print(u'正在获取微信好友头像信息，请耐心等待……')
    for i in tqdm(friends[1:10], desc=u'正在处理好友头像信息', unit=u'个'):
        i.get_avatar(save_path='image/' + i.nick_name + '.jpg')
    print(u'\n微信好友头像信息获取完毕')



    # 生成一份最终的html文件
    print(u'所有数据获取完毕，正在生成微信个人数据报告，请耐心等待……')
    generate_html('微信个人数据报告.html')
    print(u'生成微信个人数据报告，该文件为当前目录下的[微信个人数据报告.html]')


    # 调用系统方式自动打开这个html文件
    print(u'已为你自动打开 微信个人数据报告.html')
    open_html('微信个人数据报告.html')