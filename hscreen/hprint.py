# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python 2
        python 3
        请使用英文字符，否则格式可能不对称

    Content:

        @star(len=81):
            return a string with len's '*' (default 105)
        @pstar(len=81):
            print a string with len's '*' (default 105)
        @line(string1):
            return a string such as '*** string1 ***'
        @pline(string1):
            print a string such as '*** string1 ***'
        @point(string1,string2):
            return a string such as '*** string1 ==> string2 ***'
        @ppoint(string1,string2):
            print a string such as '*** string1 ==> string2 ***'
        @pointbox(dict[string1]=string2):
            return a string box such as '*** string1 ==> string2 ***'
        @ppointbox(dict[string1]=string2):
            print a string box such as '*** string1 ==> string2 ***'
'''


def star(len=105):
    "return a string with len's '*' (default 105)"
    onestar = '*'
    output = ''
    for i in range(len):
        output += onestar
    return output


def pstar(len=105):
    "print a string with len's '*' (default 105)"
    print(star(len))


def line(string1):
    "return a string such as '*** string1 ***'"
    output = '***  '
    output += '{:<95}'.format(string1)
    output += '  ***'
    return output


def pline(string1):
    "print a string such as '*** string1 ***'"
    print(line(string1))


def point(string1, string2):
    "return a string such as '*** string1 ==> string2 ***'"
    return '***  {:<30} ==> {:<60}  ***'.format(string1, string2)


def ppoint(string1, string2):
    "print a string such as '** string1 ==> string2 **'"
    print(point(string1, string2))


def pointbox(stringlist):
    "return a string box such as '*** string1 ==> string2 ***'"
    output = ''
    output += star() + '\n'
    for i in stringlist:
        output += point(i, stringlist[i]) + '\n'
    output += star()
    return output


def ppointbox(stringlist):
    "print a string box such as '*** string1 ==> string2 ***'"
    print(pointbox(stringlist))


def pika():
    '''
    输出一个皮卡丘\n
    输出一个皮卡丘
    '''
    output = ''' 　　
　 　/＼　  　  ／|     皮~~~~~~卡~~~~~~~！！！
　  /　│　　 ／　／
　 │　Z ＿,＜　／ 　   /`ヽ
　 │　　　　　ヽ　    /　　〉
　  Y　　　　　ヽ　  /　　/
　 ｲ●　､　●　　 |  〈　　/
　()　 へ　 ()　|　  ＼〈
　　>ｰ ､_　 ィ　 │   ／／
　 / へ　　 /　ﾉ＜|  ＼＼
　 ヽ_ﾉ　　(_／　 │ ／／
　　7　　　　　　　|／
　　＞―r￣￣`ｰ―＿―|
    '''
    return output


def ppika():
    '输出一个皮卡丘\n输出一个皮卡丘'
    print(pika())
