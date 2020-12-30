# -*- coding: UTF-8 -*-
# Public package
# Private package


# region Point star


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

# endregion
# region Picture


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

# endregion
# region Table


class TABLE:
    def __init__(self):
        self.content = []
        self.width = []

    def table(self):
        output = ''
        total_width = sum(self.width) + 3 * len(self.width) + 1
        for i in range(total_width):
            output += '*'
        output += '\n'
        for count1, i1 in enumerate(self.content):
            output += '* '
            for count2, i2 in enumerate(i1):
                exec("output += '{:<%d}'.format(self.content[count1][count2])" % (self.width[count2]))
                output += ' * '
            output += '\n'
        for i in range(total_width):
            output += '*'
        return output

    def ptable(self):
        print(self.table())

    def add_line(self, line):
        if(len(self.content) == 0):
            self.add_first_line(line)
        elif(len(self.width) != len(line)):
            print('Info from hprint.TABLE.add_line(): wrong input line length')
            exit(0)
        else:
            temp = []
            for count, i in enumerate(line):
                temp.append(i)
                if(len(str(i)) > self.width[count]):
                    self.width[count] = len(str(i))
            self.content.append(temp)
        return 1

    def add_first_line(self, line):
        temp = []
        for i in line:
            temp.append(i)
            self.width.append(len(str(i)))
        self.content.append(temp)
        return 1

    def add_dict(self, dict_in, keys1_use=[], keys2_use=[], key1=''):
        keys1 = dict_in.keys()
        keys1.sort()
        keys2 = dict_in[keys1[0]].keys()
        keys2.sort()
        temp = []
        temp.append(key1)
        for key2 in keys2:
            if(len(keys2_use) != 0 and key2 not in keys2_use): continue
            temp.append(key2)
        self.add_line(temp)
        for key1 in keys1:
            if(len(keys1_use) != 0 and key1 not in keys1_use): continue
            temp = [key1]
            for key2 in keys2:
                if(len(keys2_use) != 0 and key2 not in keys2_use): continue
                temp.append(dict_in[key1][key2])
            self.add_line(temp)
        return 1


# endregion
